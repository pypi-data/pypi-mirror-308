import asyncio
import datetime
import json
import logging
import os
from typing import Any, Callable, List, Optional

import aiohttp

from khoj.database.adapters import ais_user_subscribed
from khoj.database.models import Agent, KhojUser
from khoj.processor.conversation import prompts
from khoj.processor.conversation.utils import (
    ChatEvent,
    clean_code_python,
    clean_json,
    construct_chat_history,
)
from khoj.routers.helpers import send_message_to_model_wrapper
from khoj.utils.helpers import timer
from khoj.utils.rawconfig import LocationData

logger = logging.getLogger(__name__)


SANDBOX_URL = os.getenv("KHOJ_TERRARIUM_URL", "http://localhost:8080")


async def run_code(
    query: str,
    conversation_history: dict,
    context: str,
    location_data: LocationData,
    user: KhojUser,
    send_status_func: Optional[Callable] = None,
    query_images: List[str] = None,
    agent: Agent = None,
    sandbox_url: str = SANDBOX_URL,
    query_files: str = None,
    tracer: dict = {},
):
    # Generate Code
    if send_status_func:
        async for event in send_status_func(f"**Generate code snippets** for {query}"):
            yield {ChatEvent.STATUS: event}
    try:
        with timer("Chat actor: Generate programs to execute", logger):
            codes = await generate_python_code(
                query,
                conversation_history,
                context,
                location_data,
                user,
                query_images,
                agent,
                tracer,
                query_files,
            )
    except Exception as e:
        raise ValueError(f"Failed to generate code for {query} with error: {e}")

    # Run Code
    if send_status_func:
        async for event in send_status_func(f"**Running {len(codes)} code snippets**"):
            yield {ChatEvent.STATUS: event}
    try:
        tasks = [execute_sandboxed_python(code, sandbox_url) for code in codes]
        with timer("Chat actor: Execute generated programs", logger):
            results = await asyncio.gather(*tasks)
        for result in results:
            code = result.pop("code")
            logger.info(f"Executed Code:\n--@@--\n{code}\n--@@--Result:\n--@@--\n{result}\n--@@--")
            yield {query: {"code": code, "results": result}}
    except Exception as e:
        raise ValueError(f"Failed to run code for {query} with error: {e}")


async def generate_python_code(
    q: str,
    conversation_history: dict,
    context: str,
    location_data: LocationData,
    user: KhojUser,
    query_images: List[str] = None,
    agent: Agent = None,
    tracer: dict = {},
    query_files: str = None,
) -> List[str]:
    location = f"{location_data}" if location_data else "Unknown"
    username = prompts.user_name.format(name=user.get_full_name()) if user.get_full_name() else ""
    subscribed = await ais_user_subscribed(user)
    chat_history = construct_chat_history(conversation_history)

    utc_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    personality_context = (
        prompts.personality_context.format(personality=agent.personality) if agent and agent.personality else ""
    )

    code_generation_prompt = prompts.python_code_generation_prompt.format(
        current_date=utc_date,
        query=q,
        chat_history=chat_history,
        context=context,
        location=location,
        username=username,
        personality_context=personality_context,
    )

    response = await send_message_to_model_wrapper(
        code_generation_prompt,
        query_images=query_images,
        response_type="json_object",
        user=user,
        tracer=tracer,
        query_files=query_files,
    )

    # Validate that the response is a non-empty, JSON-serializable list
    response = clean_json(response)
    response = json.loads(response)
    codes = [code.strip() for code in response["codes"] if code.strip()]

    if not isinstance(codes, list) or not codes or len(codes) == 0:
        raise ValueError
    return codes


async def execute_sandboxed_python(code: str, sandbox_url: str = SANDBOX_URL) -> dict[str, Any]:
    """
    Takes code to run as a string and calls the terrarium API to execute it.
    Returns the result of the code execution as a dictionary.
    """
    headers = {"Content-Type": "application/json"}
    cleaned_code = clean_code_python(code)
    data = {"code": cleaned_code}

    async with aiohttp.ClientSession() as session:
        async with session.post(sandbox_url, json=data, headers=headers) as response:
            if response.status == 200:
                result: dict[str, Any] = await response.json()
                result["code"] = cleaned_code
                return result
            else:
                return {
                    "code": cleaned_code,
                    "success": False,
                    "std_err": f"Failed to execute code with {response.status}",
                }

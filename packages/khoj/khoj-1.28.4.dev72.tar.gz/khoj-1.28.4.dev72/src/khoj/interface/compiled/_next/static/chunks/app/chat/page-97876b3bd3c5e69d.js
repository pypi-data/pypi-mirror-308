(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[1929],{39929:function(e,t,s){Promise.resolve().then(s.bind(s,38874))},38874:function(e,t,s){"use strict";s.r(t),s.d(t,{default:function(){return p}});var a=s(57437),o=s(65104),n=s.n(o),i=s(2265),r=s(48861),c=s(55538),l=s(16463),d=s(58485),u=s(9557);s(7395);var h=s(69591),m=s(38423),g=s(79306);function f(e){let t=(0,l.useSearchParams)().get("conversationId"),[s,o]=(0,i.useState)(""),[r,d]=(0,i.useState)([]),[u,h]=(0,i.useState)(!1),[g,f]=(0,i.useState)(null),[p,_]=(0,i.useState)(!1),x=(0,i.useRef)(null),y=e.setQueryToProcess,w=e.onConversationIdChange,S=e.isMobileWidth?"w-full":"w-4/6";if((0,i.useEffect)(()=>{if(r.length>0){let t=r.map(e=>encodeURIComponent(e));e.setImages(t)}},[r,e.setImages]),(0,i.useEffect)(()=>{let t=localStorage.getItem("images");if(t){let s=JSON.parse(t);d(s);let a=s.map(e=>encodeURIComponent(e));e.setImages(a),localStorage.removeItem("images")}let s=localStorage.getItem("message");s&&(h(!0),y(s),s.trim().startsWith("/research")&&_(!0));let a=localStorage.getItem("uploadedFiles");if(a){let t=a?JSON.parse(a):[],s=[];for(let e of t)s.push({name:e.name,file_type:e.file_type,content:e.content,size:e.size});localStorage.removeItem("uploadedFiles"),e.setUploadedFiles(s)}},[y,e.setImages,t]),(0,i.useEffect)(()=>{s&&(h(!0),y(s))},[s,y]),(0,i.useEffect)(()=>{t&&(null==w||w(t))},[t,w]),(0,i.useEffect)(()=>{e.streamedMessages&&e.streamedMessages.length>0&&e.streamedMessages[e.streamedMessages.length-1].completed?(h(!1),d([]),e.setUploadedFiles(void 0)):o("")},[e.streamedMessages]),!t){window.location.href="/";return}return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)("div",{className:n().chatBodyFull,children:(0,a.jsx)(c.Z,{conversationId:t,setTitle:e.setTitle,setAgent:f,pendingMessage:u?s:"",incomingMessages:e.streamedMessages,setIncomingMessages:e.setStreamedMessages,customClassName:S})}),(0,a.jsx)("div",{className:"".concat(n().inputBox," p-1 md:px-2 shadow-md bg-background align-middle items-center justify-center dark:bg-neutral-700 dark:border-0 dark:shadow-sm rounded-t-2xl rounded-b-none md:rounded-xl h-fit ").concat(S," mr-auto ml-auto"),children:(0,a.jsx)(m.a,{agentColor:null==g?void 0:g.color,isLoggedIn:e.isLoggedIn,sendMessage:e=>o(e),sendImage:e=>d(t=>[...t,e]),sendDisabled:u,chatOptionsData:e.chatOptionsData,conversationId:t,isMobileWidth:e.isMobileWidth,setUploadedFiles:e.setUploadedFiles,ref:x,isResearchModeEnabled:p})})]})}function p(){let e="Khoj AI - Chat",[t,s]=(0,i.useState)(null),[o,c]=(0,i.useState)(!0),[l,m]=(0,i.useState)(e),[p,_]=(0,i.useState)(null),[x,y]=(0,i.useState)([]),[w,S]=(0,i.useState)(""),[I,v]=(0,i.useState)(!1),[b,j]=(0,i.useState)(void 0),[B,C]=(0,i.useState)([]),M=(0,h.k6)()||{timezone:Intl.DateTimeFormat().resolvedOptions().timeZone},E=(0,g.GW)(),F=(0,h.IC)();async function T(e){if(!e.ok)throw Error(e.statusText);if(!e.body)throw Error("Response body is null");let t=e.body.getReader(),s=new TextDecoder,a="␃\uD83D\uDD1A␗",o="",n=[],i={},r={};for(;;){let e;let{done:c,value:l}=await t.read();if(c){S(""),v(!1),C([]),p&&(0,u.tQ)(p,m);break}for(o+=s.decode(l,{stream:!0});-1!==(e=o.indexOf(a));){let t=o.slice(0,e);if(o=o.slice(e+a.length),t){let e=x.find(e=>!e.completed);if(!e){console.error("No current message found");return}({context:n,onlineContext:i,codeContext:r}=(0,u.VK)(t,e,n,i,r)),y([...x])}}}}async function k(){if(localStorage.removeItem("message"),!w||!p)return;let e={q:w,conversation_id:p,stream:!0,...M&&{city:M.city,region:M.region,country:M.country,country_code:M.countryCode,timezone:M.timezone},...B.length>0&&{images:B},...b&&{files:b}},t=await fetch("/api/chat?client=web",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)});try{await T(t)}catch(o){let e=await t.json();console.error(e);let s=x.find(e=>!e.completed);if(!s)return;let a=o.message;a.includes("Error in input stream")?s.rawResponse="Woops! The connection broke while I was writing my thoughts down. Maybe try again in a bit or dislike this message if the issue persists?":429===t.status?"detail"in e?s.rawResponse="".concat(e.detail):s.rawResponse="I'm a bit overwhelmed at the moment. Could you try again in a bit or dislike this message if the issue persists?":s.rawResponse="Umm, not sure what just happened. I see this error message: ".concat(a,". Could you try again or dislike this message if the issue persists?"),s.completed=!0,y([...x]),S(""),v(!1)}}return((0,i.useEffect)(()=>{fetch("/api/chat/options").then(e=>e.json()).then(e=>{c(!1),e&&s(e)}).catch(e=>{console.error(e)}),(0,h.EK)()},[]),(0,i.useEffect)(()=>{if(w){let e={rawResponse:"",trainOfThought:[],context:[],onlineContext:{},codeContext:{},completed:!1,timestamp:new Date().toISOString(),rawQuery:w||"",images:B,queryFiles:b};y(t=>[...t,e]),v(!0)}},[w]),(0,i.useEffect)(()=>{I&&k()},[I]),o)?(0,a.jsx)(d.Z,{}):(0,a.jsxs)("div",{className:"".concat(n().main," ").concat(n().chatLayout),children:[(0,a.jsx)("title",{children:"".concat(e).concat(l&&l!==e?": ".concat(l):"")}),(0,a.jsx)("div",{children:(0,a.jsx)(r.ZP,{conversationId:p,uploadedFiles:[],isMobileWidth:F})}),(0,a.jsx)("div",{className:n().chatBox,children:(0,a.jsxs)("div",{className:n().chatBoxBody,children:[!F&&p&&(0,a.jsxs)("div",{className:"".concat(n().chatTitleWrapper," text-nowrap text-ellipsis overflow-hidden max-w-screen-md grid items-top font-bold mr-8 pt-6 col-auto h-fit"),children:[l&&(0,a.jsx)("h2",{className:"text-lg text-ellipsis whitespace-nowrap overflow-x-hidden",children:l}),(0,a.jsx)(r.En,{conversationId:p,setTitle:m,sizing:"md"})]}),(0,a.jsx)(i.Suspense,{fallback:(0,a.jsx)(d.Z,{}),children:(0,a.jsx)(f,{isLoggedIn:null!==E,streamedMessages:x,setStreamedMessages:y,chatOptionsData:t,setTitle:m,setQueryToProcess:S,setUploadedFiles:j,isMobileWidth:F,onConversationIdChange:e=>{_(e)},setImages:C})})]})})]})}},16463:function(e,t,s){"use strict";var a=s(71169);s.o(a,"useRouter")&&s.d(t,{useRouter:function(){return a.useRouter}}),s.o(a,"useSearchParams")&&s.d(t,{useSearchParams:function(){return a.useSearchParams}})},65104:function(e){e.exports={main:"chat_main__8xQu5",suggestions:"chat_suggestions__m8n2t",inputBox:"chat_inputBox__LOFws",chatBodyFull:"chat_chatBodyFull__FfKEK",chatBody:"chat_chatBody__sS1LX",chatLayout:"chat_chatLayout__pR203",chatBox:"chat_chatBox__FBct_",titleBar:"chat_titleBar__R5QlK",chatBoxBody:"chat_chatBoxBody__qT_SC",agentIndicator:"chat_agentIndicator__8V55w",chatTitleWrapper:"chat_chatTitleWrapper__6ChWq"}}},function(e){e.O(0,[7812,9448,4836,3954,9001,3062,3124,3803,2261,9434,1603,9417,8423,5538,2971,7023,1744],function(){return e(e.s=39929)}),_N_E=e.O()}]);
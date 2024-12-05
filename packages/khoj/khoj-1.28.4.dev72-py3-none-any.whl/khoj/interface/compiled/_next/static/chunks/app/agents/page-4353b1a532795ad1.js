(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9718],{1813:function(e,t,n){Promise.resolve().then(n.bind(n,89915))},89915:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return O}});var a=n(57437),l=n(15283),o=n.n(l),s=n(29039),i=n(2265),r=n(79306),d=n(35418),c=n(64945),u=n(90837),p=n(66820),m=n(58485),f=n(48861),h=n(47412),g=n(69591),x=n(81970),v=n(39343),j=n(31014);let b=()=>window.fetch("/api/agents").then(e=>e.json()).catch(e=>console.log(e)),_=e=>fetch(e).then(e=>e.json());function y(e){let[t,n]=(0,i.useState)(!1),[l,o]=(0,i.useState)(null),[s,r]=(0,i.useState)(!0),c=(0,v.cI)({resolver:(0,j.F)(x.bc),defaultValues:{name:e.data.name,persona:e.data.persona,color:e.data.color,icon:e.data.icon,privacy_level:e.data.privacy_level,chat_model:e.selectedChatModelOption,files:[]}});return(0,i.useEffect)(()=>{c.reset({name:e.data.name,persona:e.data.persona,color:e.data.color,icon:e.data.icon,privacy_level:e.data.privacy_level,chat_model:e.selectedChatModelOption,files:[]})},[e.selectedChatModelOption,e.data]),(0,a.jsxs)(u.Vq,{open:t,onOpenChange:n,children:[(0,a.jsx)(u.hg,{children:(0,a.jsxs)("div",{className:"flex items-center text-md gap-2",children:[(0,a.jsx)(d.v,{}),"Create Agent"]})}),(0,a.jsxs)(u.cZ,{className:"lg:max-w-screen-lg overflow-y-scroll max-h-screen",children:[(0,a.jsx)(u.fK,{children:"Create Agent"}),!e.userProfile&&s&&(0,a.jsx)(p.Z,{loginRedirectMessage:"Sign in to start chatting with a specialized agent",onOpenChange:r}),(0,a.jsx)(x.ks,{form:c,onSubmit:t=>{fetch("/api/agents",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)}).then(t=>{200===t.status?(c.reset(),n(!1),o(null),e.setAgentChangeTriggered(!0)):t.json().then(e=>{console.error(e),e.error&&o(e.error)})}).catch(e=>{console.error("Error:",e),o(e)})},create:!0,errors:l,filesOptions:e.filesOptions,modelOptions:e.modelOptions,inputToolOptions:e.inputToolOptions,outputModeOptions:e.outputModeOptions,isSubscribed:e.isSubscribed})]})]})}function O(){let{data:e,error:t,mutate:n}=(0,s.ZP)("agents",b,{revalidateOnFocus:!1}),l=(0,r.GW)(),{userConfig:d}=(0,r.h2)(!0),[u,v]=(0,i.useState)(!1),j=(0,g.IC)(),[O,w]=(0,i.useState)([]),[N,L]=(0,i.useState)([]),[M,C]=(0,i.useState)(null),{data:E,error:S}=(0,s.ZP)(d?"/api/content/computer":null,_),{data:Z,error:P}=(0,s.ZP)("/api/agents/options",_),[A,T]=(0,i.useState)(!1);if((0,i.useEffect)(()=>{A&&(n(),T(!1))},[A]),(0,i.useEffect)(()=>{if(e){w(e.filter(e=>e.creator===(null==l?void 0:l.username)));let t=e.filter(e=>"private"!==e.privacy_level&&e.creator!==(null==l?void 0:l.username));L(t);{let n=new URLSearchParams(window.location.search).get("agent");if(n){C(n);let a=e.find(e=>e.slug===n);a||(a=t.find(e=>e.slug===n)),a||fetch("/api/agents/".concat(n)).then(e=>{if(404===e.status)throw Error("Agent not found");return e.json()}).then(e=>{"protected"===e.privacy_level&&L(t=>[...t,e])})}}}},[e,l]),t)return(0,a.jsxs)("main",{className:o().main,children:[(0,a.jsx)("div",{className:"".concat(o().titleBar," text-5xl"),children:"Agents"}),(0,a.jsx)("div",{className:o().agentList,children:"Error loading agents"})]});if(!e)return(0,a.jsx)("main",{className:o().main,children:(0,a.jsxs)("div",{className:o().agentList,children:[(0,a.jsx)(m.l,{})," booting up your agents"]})});let R=(null==d?void 0:d.chat_model_options)||[],k=(null==d?void 0:d.selected_chat_model_config)||0,z=(0,r.T8)(d),F=R.find(e=>e.id===k);return(0,a.jsx)("main",{className:"w-full mx-auto",children:(0,a.jsxs)("div",{className:"grid w-full mx-auto",children:[(0,a.jsx)("div",{className:"".concat(o().sidePanel," top-0"),children:(0,a.jsx)(f.ZP,{conversationId:null,uploadedFiles:[],isMobileWidth:j})}),(0,a.jsxs)("div",{className:"".concat(o().pageLayout," w-full"),children:[(0,a.jsxs)("div",{className:"pt-6 md:pt-8 flex justify-between",children:[(0,a.jsx)("h1",{className:"text-3xl flex items-center",children:"Agents"}),(0,a.jsx)("div",{className:"ml-auto float-right border p-2 pt-3 rounded-xl font-bold hover:bg-stone-100 dark:hover:bg-neutral-900",children:(0,a.jsx)(y,{data:{slug:"",name:"",persona:"",color:"",icon:"",privacy_level:"private",managed_by_admin:!1,chat_model:"",input_tools:[],output_modes:[]},userProfile:l,isMobileWidth:j,filesOptions:E||[],modelOptions:(null==d?void 0:d.chat_model_options)||[],selectedChatModelOption:(null==F?void 0:F.name)||"",isSubscribed:z,setAgentChangeTriggered:T,inputToolOptions:(null==Z?void 0:Z.input_tools)||{},outputModeOptions:(null==Z?void 0:Z.output_modes)||{}})})]}),u&&(0,a.jsx)(p.Z,{loginRedirectMessage:"Sign in to start chatting with a specialized agent",onOpenChange:v}),(0,a.jsx)(h.bZ,{className:"bg-secondary border-none my-4",children:(0,a.jsxs)(h.X,{children:[(0,a.jsx)(c.B,{weight:"fill",className:"h-4 w-4 text-purple-400 inline"}),(0,a.jsx)("span",{className:"font-bold",children:"How it works"})," Use any of these specialized personas to tune your conversation to your needs."]})}),(0,a.jsx)("div",{className:"pt-6 md:pt-8",children:(0,a.jsx)("div",{className:"".concat(o().agentList),children:O.map(e=>(0,a.jsx)(x.EY,{data:e,userProfile:l,isMobileWidth:j,filesOptions:null!=E?E:[],selectedChatModelOption:(null==F?void 0:F.name)||"",isSubscribed:z,setAgentChangeTriggered:T,modelOptions:(null==d?void 0:d.chat_model_options)||[],editCard:!0,agentSlug:M||"",inputToolOptions:(null==Z?void 0:Z.input_tools)||{},outputModeOptions:(null==Z?void 0:Z.output_modes)||{}},e.slug))})}),(0,a.jsxs)("div",{className:"pt-6 md:pt-8",children:[(0,a.jsx)("h2",{className:"text-2xl",children:"Explore"}),(0,a.jsx)("div",{className:"".concat(o().agentList),children:N.map(e=>(0,a.jsx)(x.EY,{data:e,userProfile:l,isMobileWidth:j,editCard:!1,filesOptions:null!=E?E:[],selectedChatModelOption:(null==F?void 0:F.name)||"",isSubscribed:z,setAgentChangeTriggered:T,modelOptions:(null==d?void 0:d.chat_model_options)||[],agentSlug:M||"",inputToolOptions:(null==Z?void 0:Z.input_tools)||{},outputModeOptions:(null==Z?void 0:Z.output_modes)||{}},e.slug))})]})]})]})})}},66820:function(e,t,n){"use strict";n.d(t,{Z:function(){return s}});var a=n(57437),l=n(6780),o=n(87138);function s(e){return(0,a.jsx)(l.aR,{open:!0,onOpenChange:e.onOpenChange,children:(0,a.jsxs)(l._T,{children:[(0,a.jsx)(l.fY,{children:(0,a.jsx)(l.f$,{children:"Sign in to Khoj to continue"})}),(0,a.jsxs)(l.yT,{children:[e.loginRedirectMessage,". By logging in, you agree to our"," ",(0,a.jsx)(o.default,{href:"https://khoj.dev/terms-of-service",children:"Terms of Service."})]}),(0,a.jsxs)(l.xo,{children:[(0,a.jsx)(l.le,{children:"Dismiss"}),(0,a.jsx)(l.OL,{className:"bg-slate-400 hover:bg-slate-500",onClick:()=>{window.location.href="/login?next=".concat(encodeURIComponent(window.location.pathname))},children:(0,a.jsxs)(o.default,{href:"/login?next=".concat(encodeURIComponent(window.location.pathname)),children:[" ","Login"]})})]})]})})}},70571:function(e,t,n){"use strict";n.d(t,{E:function(){return i}});var a=n(57437),l=n(2265),o=n(52431),s=n(37440);let i=l.forwardRef((e,t)=>{let{className:n,value:l,indicatorColor:i,...r}=e;return(0,a.jsx)(o.fC,{ref:t,className:(0,s.cn)("relative h-4 w-full overflow-hidden rounded-full bg-secondary",n),...r,children:(0,a.jsx)(o.z$,{className:"h-full w-full flex-1 bg-primary transition-all ".concat(i),style:{transform:"translateX(-".concat(100-(l||0),"%)")}})})});i.displayName=o.fC.displayName},93146:function(e,t,n){"use strict";n.d(t,{g:function(){return s}});var a=n(57437),l=n(2265),o=n(37440);let s=l.forwardRef((e,t)=>{let{className:n,...l}=e;return(0,a.jsx)("textarea",{className:(0,o.cn)("flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",n),ref:t,...l})});s.displayName="Textarea"},19666:function(e,t,n){"use strict";n.d(t,{_v:function(){return c},aJ:function(){return d},pn:function(){return i},u:function(){return r}});var a=n(57437),l=n(2265),o=n(27071),s=n(37440);let i=o.zt,r=o.fC,d=o.xz,c=l.forwardRef((e,t)=>{let{className:n,sideOffset:l=4,...i}=e;return(0,a.jsx)(o.VY,{ref:t,sideOffset:l,className:(0,s.cn)("z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",n),...i})});c.displayName=o.VY.displayName},15283:function(e){e.exports={titleBar:"agents_titleBar__FzYbY",agentPersonality:"agents_agentPersonality__o0Ysz",pageLayout:"agents_pageLayout__gR3S3",sidePanel:"agents_sidePanel__wGVGc",infoButton:"agents_infoButton__NqI7E",agentList:"agents_agentList__XVx4A"}},64945:function(e,t,n){"use strict";n.d(t,{B:function(){return h}});var a=n(2265),l=n(52195);let o=new Map([["bold",a.createElement(a.Fragment,null,a.createElement("path",{d:"M219.71,117.38a12,12,0,0,0-7.25-8.52L161.28,88.39l10.59-70.61a12,12,0,0,0-20.64-10l-112,120a12,12,0,0,0,4.31,19.33l51.18,20.47L84.13,238.22a12,12,0,0,0,20.64,10l112-120A12,12,0,0,0,219.71,117.38ZM113.6,203.55l6.27-41.77a12,12,0,0,0-7.41-12.92L68.74,131.37,142.4,52.45l-6.27,41.77a12,12,0,0,0,7.41,12.92l43.72,17.49Z"}))],["duotone",a.createElement(a.Fragment,null,a.createElement("path",{d:"M96,240l16-80L48,136,160,16,144,96l64,24Z",opacity:"0.2"}),a.createElement("path",{d:"M215.79,118.17a8,8,0,0,0-5-5.66L153.18,90.9l14.66-73.33a8,8,0,0,0-13.69-7l-112,120a8,8,0,0,0,3,13l57.63,21.61L88.16,238.43a8,8,0,0,0,13.69,7l112-120A8,8,0,0,0,215.79,118.17ZM109.37,214l10.47-52.38a8,8,0,0,0-5-9.06L62,132.71l84.62-90.66L136.16,94.43a8,8,0,0,0,5,9.06l52.8,19.8Z"}))],["fill",a.createElement(a.Fragment,null,a.createElement("path",{d:"M213.85,125.46l-112,120a8,8,0,0,1-13.69-7l14.66-73.33L45.19,143.49a8,8,0,0,1-3-13l112-120a8,8,0,0,1,13.69,7L153.18,90.9l57.63,21.61a8,8,0,0,1,3,12.95Z"}))],["light",a.createElement(a.Fragment,null,a.createElement("path",{d:"M213.84,118.63a6,6,0,0,0-3.73-4.25L150.88,92.17l15-75a6,6,0,0,0-10.27-5.27l-112,120a6,6,0,0,0,2.28,9.71l59.23,22.21-15,75a6,6,0,0,0,3.14,6.52A6.07,6.07,0,0,0,96,246a6,6,0,0,0,4.39-1.91l112-120A6,6,0,0,0,213.84,118.63ZM106,220.46l11.85-59.28a6,6,0,0,0-3.77-6.8l-55.6-20.85,91.46-98L138.12,94.82a6,6,0,0,0,3.77,6.8l55.6,20.85Z"}))],["regular",a.createElement(a.Fragment,null,a.createElement("path",{d:"M215.79,118.17a8,8,0,0,0-5-5.66L153.18,90.9l14.66-73.33a8,8,0,0,0-13.69-7l-112,120a8,8,0,0,0,3,13l57.63,21.61L88.16,238.43a8,8,0,0,0,13.69,7l112-120A8,8,0,0,0,215.79,118.17ZM109.37,214l10.47-52.38a8,8,0,0,0-5-9.06L62,132.71l84.62-90.66L136.16,94.43a8,8,0,0,0,5,9.06l52.8,19.8Z"}))],["thin",a.createElement(a.Fragment,null,a.createElement("path",{d:"M211.89,119.09a4,4,0,0,0-2.49-2.84l-60.81-22.8,15.33-76.67a4,4,0,0,0-6.84-3.51l-112,120a4,4,0,0,0-1,3.64,4,4,0,0,0,2.49,2.84l60.81,22.8L92.08,239.22a4,4,0,0,0,6.84,3.51l112-120A4,4,0,0,0,211.89,119.09ZM102.68,227l13.24-66.2a4,4,0,0,0-2.52-4.53L55,134.36,153.32,29l-13.24,66.2a4,4,0,0,0,2.52,4.53L201,121.64Z"}))]]);var s=Object.defineProperty,i=Object.defineProperties,r=Object.getOwnPropertyDescriptors,d=Object.getOwnPropertySymbols,c=Object.prototype.hasOwnProperty,u=Object.prototype.propertyIsEnumerable,p=(e,t,n)=>t in e?s(e,t,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[t]=n,m=(e,t)=>{for(var n in t||(t={}))c.call(t,n)&&p(e,n,t[n]);if(d)for(var n of d(t))u.call(t,n)&&p(e,n,t[n]);return e},f=(e,t)=>i(e,r(t));let h=(0,a.forwardRef)((e,t)=>a.createElement(l.Z,f(m({ref:t},e),{weights:o})));h.displayName="Lightning"}},function(e){e.O(0,[9460,9448,9001,3062,3124,3803,5512,4602,1603,9417,1970,2971,7023,1744],function(){return e(e.s=1813)}),_N_E=e.O()}]);
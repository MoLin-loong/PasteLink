"""手机快速输入 — 手机当电脑键盘/鼠标，扫码即用"""
import asyncio, os, socket, sys, threading, time, ctypes

if sys.platform == "win32":
    sys.stdout.reconfigure(errors="replace") if hasattr(sys.stdout, "reconfigure") else None
    os.environ["PYTHONIOENCODING"] = "utf-8"
from http.server import HTTPServer, BaseHTTPRequestHandler
import qrcode, websockets, pyperclip, pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0  # 去掉默认 0.1s 间隔，降低按键延迟

user32 = ctypes.windll.user32

HTML = r"""<!DOCTYPE html>
<html lang=zh-CN>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1,user-scalable=no">
<title>手机键盘</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#0f1226;--surface:#1a1f3a;--surface2:#242b4d;--line:#2d3563;--accent:#4ecca3;--accent2:#5b8def;--danger:#e94560;--text:#e8eaf2;--muted:#8892b0}
html,body{height:100%}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);display:flex;flex-direction:column;height:100vh;overflow:hidden;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
button{font-family:inherit}
/* header */
.header{padding:10px 14px;background:var(--surface);display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}
.left-h{display:flex;align-items:center;gap:9px;min-width:0}
.dot{width:9px;height:9px;border-radius:50%;background:var(--danger);flex-shrink:0}
.dot.on{background:var(--accent);box-shadow:0 0 8px rgba(78,204,163,.6)}
.status{font-size:13px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.h-actions{display:flex;align-items:center;gap:8px}
.icon-btn{width:40px;height:40px;border:none;border-radius:11px;background:var(--surface2);color:var(--accent);display:flex;align-items:center;justify-content:center;cursor:pointer;transition:transform .1s,background .15s}
.icon-btn:active{transform:scale(.92);background:var(--line)}
.icon-btn svg{width:22px;height:22px}
#ic-ms{transform:rotate(-90deg)}
/* combined input + trackpad view */
.kb-view{flex:1;display:flex;flex-direction:column;padding:12px;gap:10px;min-height:0;transition:padding-bottom .2s}
textarea{flex:6 1 74px;min-height:64px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px;color:var(--text);font-size:16px;line-height:1.5;resize:none;outline:none;transition:border-color .15s,flex-grow .24s ease}
textarea:focus{border-color:var(--accent)}
.trackpad-zone{flex:1 1 74px;min-height:72px;display:flex;transition:flex-grow .24s ease}
.kb-view.mouse-active textarea{flex-grow:1}
.kb-view.mouse-active .trackpad-zone{flex-grow:6;min-height:140px}
.kb-tools{display:flex;flex-direction:column;gap:8px;flex-shrink:0}
.kb-nav{display:flex;gap:8px;align-items:stretch}
.kb-nav>.kb-key{flex:1;min-width:0}
.dpad{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:8px;flex:1;min-width:0}
.kb-nav>.kb-key[data-k="Enter"]{font-size:22px}
.dpad .mouse-left{grid-column:1;grid-row:1}
.dpad .up{grid-column:2;grid-row:1}
.dpad .mouse-right{grid-column:3;grid-row:1}
.dpad .left{grid-column:1;grid-row:2}
.dpad .down{grid-column:2;grid-row:2}
.dpad .right{grid-column:3;grid-row:2}
button.kb-key{background:var(--surface2);color:var(--text);border:1px solid var(--line);border-radius:12px;font-size:17px;font-weight:600;cursor:pointer;user-select:none;-webkit-touch-callout:none;-webkit-user-select:none;padding:14px 0;transition:background .12s,transform .08s;display:flex;align-items:center;justify-content:center}
button.mouse-key{background:var(--surface2);color:var(--accent);border:1px solid var(--line);border-radius:12px;font-size:12px;font-weight:700;cursor:pointer;user-select:none;-webkit-touch-callout:none;-webkit-user-select:none;padding:0;transition:background .12s,transform .08s;display:flex;align-items:center;justify-content:center;touch-action:manipulation}
.kb-pressed{background:var(--accent)!important;color:var(--bg)!important;transform:scale(.96)}
.kb-bottom{display:flex;gap:8px}
.kb-bottom .kb-key{flex:1}
#send{flex:1;padding:13px;border:none;border-radius:12px;font-size:15px;font-weight:700;background:var(--accent);color:var(--bg);cursor:pointer;transition:transform .08s,filter .12s}
#send:active{transform:scale(.97);filter:brightness(.92)}
/* settings overlay */
.overlay{position:fixed;inset:0;background:rgba(5,7,20,.66);display:flex;align-items:center;justify-content:center;z-index:50;backdrop-filter:blur(3px)}
.overlay.hidden{display:none}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:22px;width:84%;max-width:340px;color:var(--text);box-shadow:0 20px 50px rgba(0,0,0,.5)}
.panel h3{margin-bottom:18px;font-size:18px;font-weight:700}
.row{margin-bottom:18px}
.row label{display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px;color:var(--muted)}
.row label span{color:var(--accent);font-weight:600}
.row input[type=range]{width:100%;accent-color:var(--accent)}
.panel .close{width:100%;padding:12px;background:var(--accent);color:var(--bg);border:none;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer}
/* trackpad */
#pad{width:100%;height:100%;background:var(--surface);border:1px solid var(--line);border-radius:16px;position:relative;overflow:hidden;touch-action:none;outline:none;box-shadow:inset 0 2px 12px rgba(0,0,0,.28);min-height:0;transition:border-color .2s,box-shadow .2s}
.kb-view.mouse-active #pad{border-color:var(--accent);box-shadow:inset 0 2px 12px rgba(0,0,0,.28),0 0 0 1px rgba(78,204,163,.18)}
#pad .hint{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#3d4670;font-size:13px;pointer-events:none;text-align:center;line-height:1.7}
.hidden{display:none!important}
/* full keyboard view */
.fullkb{flex:1;display:flex;flex-direction:column;gap:5px;padding:10px;min-height:0}
.fk-row{display:flex;gap:5px;justify-content:center}
.fk{flex:1;min-width:0;height:38px;background:var(--surface2);color:var(--text);border:1px solid var(--line);border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;transition:background .04s,transform .08s;-webkit-user-select:none;user-select:none;touch-action:manipulation;padding:0;display:flex;align-items:center;justify-content:center}
.fk.kb-pressed{background:var(--accent)!important;color:var(--bg)!important;transform:scale(.94)}
.fk.wide{flex:2}
.fk.space{flex:6}
.fk.ctrl{flex:1.4}
</style>
<div class=header>
  <div class=left-h><div class=dot id=dot></div><span class=status id=status>正在连接...</span></div>
  <div class=h-actions>
    <button class="icon-btn" id=setBtn title="设置">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
    </button>
    <button class="icon-btn" id=fullKbBtn title="完整键盘">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 9h.01M10 9h.01M14 9h.01M18 9h.01M6 13h.01M10 13h.01M14 13h.01M18 13h.01M7 16h10"/></svg>
    </button>
    <button class="icon-btn" id=toggle title="聚焦输入框/触控板">
      <svg id=ic-kb viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M8 14h8"/></svg>
      <svg id=ic-ms viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="hidden"><rect x="6" y="3" width="12" height="18" rx="2"/><path d="M12 3v18M6 8h6M6 12h6M6 16h6"/></svg>
    </button>
  </div>
</div>

<!-- settings -->
<div class="overlay hidden" id=overlay>
  <div class=panel>
    <h3>设置</h3>
    <div class=row>
      <label>鼠标灵敏度 <span id=senVal>1.0</span></label>
      <input type=range id=sen min="1" max="10" step="0.1" value="1">
    </div>
    <div class=row>
      <label>滚轮速度 <span id=scrVal>1.0</span></label>
      <input type=range id=scr min="0.1" max="5" step="0.1" value="1">
    </div>
    <div class=row>
      <label>退格连发速度(ms) <span id=repVal>150</span></label>
      <input type=range id=rep min="30" max="500" step="10" value="150">
    </div>
    <div class=row>
      <label>底部黑边(px) <span id=padHVal>0</span></label>
      <input type=range id=padH min="0" max="400" step="10" value="0">
    </div>
    <button class=close id=setClose>完成</button>
  </div>
</div>

<!-- keyboard -->
<div class=kb-view id=kbView>
  <textarea id=msg placeholder="输入文字，回车发送…" autofocus></textarea>
  <div class=trackpad-zone>
    <div id=pad tabindex=0><div class=hint>单指拖动移动 · 轻点左键<br>双指上下滑滚轮</div></div>
  </div>
  <div class=kb-tools>
    <div class=kb-nav>
      <button class=kb-key data-k="Enter">↵</button>
      <div class=dpad>
        <button class="mouse-key mouse-left" data-m="left">左键</button>
        <button class="kb-key up" data-k="Up">↑</button>
        <button class="mouse-key mouse-right" data-m="right">右键</button>
        <button class="kb-key left" data-k="Left">←</button>
        <button class="kb-key down" data-k="Down">↓</button>
        <button class="kb-key right" data-k="Right">→</button>
      </div>
      <button class=kb-key data-k="Backspace">⌫</button>
    </div>
    <div class=kb-bottom>
      <button class=kb-key data-k="WinV">剪贴板</button>
      <button id=send>发送</button>
    </div>
  </div>
</div>

<!-- full keyboard -->
<div class="fullkb hidden" id=fullKbView>
  <div class=fk-row>
    <button class="fk" data-k="F1">F1</button><button class="fk" data-k="F2">F2</button><button class="fk" data-k="F3">F3</button><button class="fk" data-k="F4">F4</button><button class="fk" data-k="F5">F5</button><button class="fk" data-k="F6">F6</button><button class="fk" data-k="F7">F7</button><button class="fk" data-k="F8">F8</button><button class="fk" data-k="F9">F9</button><button class="fk" data-k="F10">F10</button><button class="fk" data-k="F11">F11</button><button class="fk" data-k="F12">F12</button>
  </div>
  <div class=fk-row>
    <button class="fk" data-k="Esc">Esc</button><button class="fk" data-k="Tab">Tab</button><button class="fk" data-k="CapsLock">Caps</button><button class="fk" data-k="Win">Win</button><button class="fk" data-k="Menu">Menu</button>
  </div>
  <div class=fk-row>
    <button class="fk" data-k="1">1</button><button class="fk" data-k="2">2</button><button class="fk" data-k="3">3</button><button class="fk" data-k="4">4</button><button class="fk" data-k="5">5</button><button class="fk" data-k="6">6</button><button class="fk" data-k="7">7</button><button class="fk" data-k="8">8</button><button class="fk" data-k="9">9</button><button class="fk" data-k="0">0</button><button class="fk" data-k="-">-</button><button class="fk" data-k="=">=</button><button class="fk wide" data-k="Backspace">⌫</button>
  </div>
  <div class=fk-row>
    <button class="fk" data-k="q">Q</button><button class="fk" data-k="w">W</button><button class="fk" data-k="e">E</button><button class="fk" data-k="r">R</button><button class="fk" data-k="t">T</button><button class="fk" data-k="y">Y</button><button class="fk" data-k="u">U</button><button class="fk" data-k="i">I</button><button class="fk" data-k="o">O</button><button class="fk" data-k="p">P</button><button class="fk" data-k="[">[</button><button class="fk" data-k="]">]</button>
  </div>
  <div class=fk-row>
    <button class="fk" data-k="a">A</button><button class="fk" data-k="s">S</button><button class="fk" data-k="d">D</button><button class="fk" data-k="f">F</button><button class="fk" data-k="g">G</button><button class="fk" data-k="h">H</button><button class="fk" data-k="j">J</button><button class="fk" data-k="k">K</button><button class="fk" data-k="l">L</button><button class="fk" data-k=";">;</button><button class="fk" data-k="'">'</button><button class="fk wide" data-k="Enter">↵</button>
  </div>
  <div class=fk-row>
    <button class="fk wide" data-k="Shift">⇧</button><button class="fk" data-k="z">Z</button><button class="fk" data-k="x">X</button><button class="fk" data-k="c">C</button><button class="fk" data-k="v">V</button><button class="fk" data-k="b">B</button><button class="fk" data-k="n">N</button><button class="fk" data-k="m">M</button><button class="fk" data-k=",">,</button><button class="fk" data-k=".">.</button><button class="fk" data-k="/">/</button><button class="fk wide" data-k="Shift">⇧</button>
  </div>
  <div class=fk-row>
    <button class="fk ctrl" data-k="Ctrl">Ctrl</button><button class="fk" data-k="Alt">Alt</button><button class="fk space" data-k="Space">Space</button><button class="fk" data-k="Alt">Alt</button><button class="fk ctrl" data-k="Ctrl">Ctrl</button><button class="fk" data-k="Left">←</button><button class="fk" data-k="Down">↓</button><button class="fk" data-k="Up">↑</button><button class="fk" data-k="Right">→</button>
  </div>
</div>

<script>
var ws,rt,h=location.hostname,mode="kb";
/* settings (persisted) */
var SET={sen:1,scr:1,rep:150,pad:0};
try{var s=JSON.parse(localStorage.getItem("pastelink_set"));if(s)SET=Object.assign(SET,s);}catch(e){}
function saveSet(){try{localStorage.setItem("pastelink_set",JSON.stringify(SET));}catch(e){}}

function conn(){
 ws=new WebSocket("ws://"+h+":8765");
 ws.onopen=function(){document.getElementById("dot").className="dot on";document.getElementById("status").textContent="已连接"};
 ws.onclose=function(){document.getElementById("dot").className="dot";document.getElementById("status").textContent="已断开，重连中...";clearTimeout(rt);rt=setTimeout(conn,3000)};
 ws.onerror=function(){ws.close()};
}
function sendRaw(t){if(ws&&ws.readyState===1)ws.send(t);}

/* block long-press context menu / text selection on all buttons */
document.addEventListener("contextmenu",function(e){e.preventDefault();});

/* ===== keyboard ===== */
var msg=document.getElementById("msg");
function send(){
 var t=msg.value;
 if(!t)return;
 sendRaw(t);msg.value="";msg.focus();
}
document.getElementById("send").onclick=send;
document.getElementById("send").addEventListener("touchstart",function(e){this.classList.add("kb-pressed");},{passive:true});
document.getElementById("send").addEventListener("touchend",function(){this.classList.remove("kb-pressed");});
document.getElementById("send").addEventListener("touchcancel",function(){this.classList.remove("kb-pressed");});

/* keys (Backspace / arrows / Enter / WinV / PrtSc / Delete):
   - 轻点 = 1 次触发
   - 按住 >=500ms 才开始连发, 连发速度设下限避免过快
   - touchUsed 屏蔽触摸后合成的 mouse 事件(会在 touchend 之后才到达) */
var kbTouch=false,kbTT=null;
function markKbTouch(){kbTouch=true;clearTimeout(kbTT);kbTT=setTimeout(function(){kbTouch=false;},700);}

function bindHold(b){
 var k=b.dataset.k, combo=(k==="WinV"||k==="PrtSc"||k==="CtrlC");
 if(combo){
   /* 组合键: 一次完整触发 */
   function fire(){sendRaw("KEY "+k);}
   b.addEventListener("touchstart",function(e){e.preventDefault();markKbTouch();fire();},{passive:false});
   b.addEventListener("mousedown",function(e){if(kbTouch)return;fire();});
   return;
 }
 if(k==="Backspace"){
   /* 退格键: 长按连发(间隔看设置), 按下有绿反馈 */
   var timer=null,lp=null;
   function fire(){sendRaw("KEY Backspace");}
   function dnBs(e,isTouch){
    if(isTouch)markKbTouch(); else if(kbTouch)return;
    if(e.cancelable)e.preventDefault();
    b.classList.add("kb-pressed");
    fire();                                                      // 先删一个
    lp=setTimeout(function(){timer=setInterval(fire,Math.max(SET.rep,30));},300);
   }
   function upBs(){
    b.classList.remove("kb-pressed");
    clearTimeout(lp); if(timer){clearInterval(timer);timer=null;}
   }
   b.addEventListener("touchstart",function(e){dnBs(e,true);},{passive:false});
   b.addEventListener("touchend",upBs);
   b.addEventListener("touchcancel",upBs);
   b.addEventListener("mousedown",function(e){dnBs(e,false);});
   b.addEventListener("mouseup",upBs);
   b.addEventListener("mouseleave",upBs);
   return;
 }
 /* 普通键: 分离式 按下=keybd_event down, 松开=keybd_event up */
 function dn(e,isTouch){
  if(isTouch)markKbTouch(); else if(kbTouch)return;
  if(e.cancelable)e.preventDefault();
  b.classList.add("kb-pressed");
  sendRaw("KEYDN "+k);
 }
 function upk(){
  b.classList.remove("kb-pressed");
  sendRaw("KEYUP "+k);
 }
 b.addEventListener("touchstart",function(e){dn(e,true);},{passive:false});
 b.addEventListener("touchend",upk);
 b.addEventListener("touchcancel",upk);
 b.addEventListener("mousedown",function(e){dn(e,false);});
 b.addEventListener("mouseup",upk);
 b.addEventListener("mouseleave",upk);
}
/* 输入区与完整键盘按键统一用同一套逻辑 */
document.querySelectorAll("#kbView .kb-key, #fullKbView .fk").forEach(bindHold);

/* ===== combined input / trackpad focus ===== */
function showMode(){
 var kb=document.getElementById("kbView"),combined=mode!=="full";
 kb.classList.toggle("hidden",!combined);
 kb.classList.toggle("mouse-active",mode==="ms");
 document.getElementById("fullKbView").classList.toggle("hidden",mode!=="full");
 document.getElementById("ic-kb").classList.toggle("hidden",mode==="ms");
 document.getElementById("ic-ms").classList.toggle("hidden",mode!=="ms");
 if(mode==="ms")document.getElementById("pad").focus();
}
function activateInput(){mode="kb";showMode();}
function activateMouse(){mode="ms";msg.blur();showMode();}
msg.addEventListener("focus",activateInput);
document.getElementById("toggle").onclick=function(){
 if(mode==="kb")activateMouse();
 else{mode="kb";showMode();msg.focus();}
};
document.getElementById("fullKbBtn").onclick=function(){
 mode = mode==="full" ? "kb" : "full";
 showMode();
};

/* ===== settings ===== */
var overlay=document.getElementById("overlay");
document.getElementById("setBtn").onclick=function(){
 document.getElementById("sen").value=SET.sen;document.getElementById("senVal").textContent=SET.sen.toFixed(1);
 document.getElementById("scr").value=SET.scr;document.getElementById("scrVal").textContent=SET.scr.toFixed(1);
 document.getElementById("rep").value=SET.rep;document.getElementById("repVal").textContent=SET.rep;
 document.getElementById("padH").value=SET.pad;document.getElementById("padHVal").textContent=SET.pad;
 overlay.classList.remove("hidden");
};
document.getElementById("setClose").onclick=function(){overlay.classList.add("hidden");};
overlay.addEventListener("click",function(e){if(e.target===overlay)overlay.classList.add("hidden");});
document.getElementById("sen").oninput=function(){SET.sen=parseFloat(this.value);document.getElementById("senVal").textContent=SET.sen.toFixed(1);saveSet();};
document.getElementById("scr").oninput=function(){SET.scr=parseFloat(this.value);document.getElementById("scrVal").textContent=SET.scr.toFixed(1);saveSet();};
document.getElementById("rep").oninput=function(){SET.rep=parseInt(this.value);document.getElementById("repVal").textContent=SET.rep;saveSet();};
document.getElementById("padH").oninput=function(){SET.pad=parseInt(this.value);document.getElementById("padHVal").textContent=SET.pad;saveSet();fitKb();};

/* ===== keyboard: avoid soft-keyboard covering buttons ===== */
function fitKb(){
 var v=window.visualViewport;
 var base=SET.pad||0, extra=0;
 if(v){
  var ov=Math.max(0,window.innerHeight-v.height-v.offsetTop);
  if(ov>0)extra=ov+12;   // 软键盘弹起时动态避让, 叠加在黑边之上
 }
 var pb=(base+extra)+"px";
 document.getElementById("kbView").style.paddingBottom=pb;
 document.getElementById("fullKbView").style.paddingBottom=pb;
}
if(window.visualViewport){window.visualViewport.addEventListener("resize",fitKb);window.visualViewport.addEventListener("scroll",fitKb);}
window.addEventListener("resize",fitKb);fitKb();

/* ===== mouse: trackpad (gestures) =====
   - 1 finger drag  -> move mouse (relative, x sensitivity)
   - 1 finger tap   -> left click
   - 2 fingers swipe up/down -> wheel scroll
*/
var pad=document.getElementById("pad");
var st={active:false,single:false,moved:false,fresh:false,sx:0,sy:0,lx:0,ly:0,t0:0,twoY:0,ax:0,ay:0,raf:0,scroll:0,scrollRaf:0};
function midY(e){var a=e.targetTouches[0],b=e.targetTouches[1];return (a.clientY+b.clientY)/2;}
function local(e){var r=pad.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}
function resetScroll(){
 if(st.scrollRaf){cancelAnimationFrame(st.scrollRaf);st.scrollRaf=0;}
 st.scroll=0;
}
function queueScroll(dy){
 /* 120 是一个完整滚轮刻度；发送更小的增量可模拟高分辨率滚轮。 */
 var unitsPerPixel=120/Math.max(2,8/SET.scr);
 st.scroll+=dy*unitsPerPixel;
 if(!st.scrollRaf)st.scrollRaf=requestAnimationFrame(flushScroll);
}
function flushScroll(){
 st.scrollRaf=0;
 var delta=Math.trunc(st.scroll);
 if(delta){sendRaw("MSCROLL "+(delta/120));st.scroll-=delta;}
}
pad.addEventListener("touchstart",function(e){
 activateMouse();
 if(e.targetTouches.length===1){
   var p=local(e.targetTouches[0]);
   st.active=true;st.single=true;st.moved=false;st.fresh=true;
   st.sx=p.x;st.sy=p.y;st.lx=p.x;st.ly=p.y;st.t0=Date.now();st.ax=0;st.ay=0;
}else if(e.targetTouches.length===2){
  st.active=true;st.single=false;            // cancel tap/drag, switch to scroll
  if(st.raf){cancelAnimationFrame(st.raf);st.raf=0;}st.ax=0;st.ay=0;
  st.twoY=midY(e);resetScroll();
}
},{passive:true});
pad.addEventListener("touchmove",function(e){
 e.preventDefault();
 if(!st.active){
   /* 手指从相邻元素滑入pad: 没有touchstart, 在此补初始化 */
   if(e.targetTouches.length===2){
     st.active=true;st.single=false;st.twoY=midY(e);resetScroll();return;
   }
   var p=local(e.targetTouches[0]);
   st.active=true;st.single=true;st.moved=false;
   st.sx=p.x;st.sy=p.y;st.lx=p.x;st.ly=p.y;st.ax=0;st.ay=0;st.t0=Date.now();
   return;
 }
 if(e.targetTouches.length===1 && st.single){
   var p=local(e.targetTouches[0]);
   if(st.fresh){st.fresh=false;st.lx=p.x;st.ly=p.y;st.sx=p.x;st.sy=p.y;return;} // 首帧只校准, 不发移动, 消除瞬移
   if(Math.abs(p.x-st.sx)>10||Math.abs(p.y-st.sy)>10)st.moved=true;
   st.ax+=(p.x-st.lx)*SET.sen; st.ay+=(p.y-st.ly)*SET.sen;   // 累加亚像素位移, 小数不丢
   st.lx=p.x;st.ly=p.y;
   if(!st.raf)st.raf=requestAnimationFrame(flushMove);        // rAF节流: 一帧只发一条, 抗网络抖动
 }else if(e.targetTouches.length===2){
   var y=midY(e);
   queueScroll(y-st.twoY);st.twoY=y;    // 每帧合并成一个高分辨率滚轮事件
 }
},{passive:false});
function flushMove(){                                          // rAF回调: 把累加的亚像素位移凑成整数发出
 st.raf=0;
 var ix=Math.trunc(st.ax),iy=Math.trunc(st.ay);
 if(ix||iy){sendRaw("MMOVE "+ix+" "+iy);st.ax-=ix;st.ay-=iy;}
}
pad.addEventListener("touchend",function(e){
 if(st.raf){cancelAnimationFrame(st.raf);st.raf=0;}           // 抬手取消未发的rAF, 残留<1px忽略
 if(st.single && !st.moved && (Date.now()-st.t0)<250)sendRaw("MCLICK left");
 if(e.targetTouches.length===0)st.active=false;
 st.single=false;
});
/* mouse (desktop debug only): real mouse drag=move, click without move=left click.
   Touch events already handle taps; suppress synthesized mouse events on touch devices. */
var touchUsed=false;
var mDown=false,mmoved=false,mx=0,my=0;
pad.addEventListener("touchstart",function(){touchUsed=true;setTimeout(function(){touchUsed=false;},600);},{passive:true});
pad.addEventListener("mousedown",function(e){if(touchUsed)return;activateMouse();mDown=true;mmoved=false;var p=local(e);mx=p.x;my=p.y;});
pad.addEventListener("mousemove",function(e){if(touchUsed||!mDown)return;e.preventDefault();var p=local(e);var dx=(p.x-mx)*SET.sen,dy=(p.y-my)*SET.sen;mx=p.x;my=p.y;if(Math.abs(dx)+Math.abs(dy)>2)mmoved=true;st.ax+=dx;st.ay+=dy;if(!st.raf)st.raf=requestAnimationFrame(flushMove);});
pad.addEventListener("mouseup",function(){if(touchUsed)return;if(mDown&&!mmoved)sendRaw("MCLICK left");mDown=false;});
pad.addEventListener("click",function(e){if(touchUsed)e.preventDefault();});

/* ===== mouse buttons beside the up arrow ===== */
document.querySelectorAll(".mouse-key").forEach(function(b){
 var btn=b.dataset.m,pressed=false;
 function down(e,isTouch){
  if(isTouch)markKbTouch(); else if(kbTouch)return;
  if(e.cancelable)e.preventDefault();
  activateMouse();
  if(!pressed){sendRaw("MCLICK "+btn+":down");pressed=true;}
  b.classList.add("kb-pressed");
 }
 function up(){
  if(pressed){sendRaw("MCLICK "+btn+":up");pressed=false;}
  b.classList.remove("kb-pressed");
 }
 b.addEventListener("touchstart",function(e){down(e,true);},{passive:false});
 b.addEventListener("touchend",up);
 b.addEventListener("touchcancel",up);
 b.addEventListener("mousedown",function(e){down(e,false);});
 b.addEventListener("mouseup",up);
 b.addEventListener("mouseleave",up);
});

setInterval(function(){if(ws&&ws.readyState===1)ws.send("__PING__")},15000);
conn();
</script>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, fmt, *args):
        pass


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()


def type_text(text):
    """粘贴到鼠标所指窗口的当前光标处"""
    pyperclip.copy(text)
    try:
        point = ctypes.wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(point))
        hwnd = user32.WindowFromPoint(point)
        hwnd = user32.GetAncestor(hwnd, 2)
        user32.SwitchToThisWindow(hwnd, True)
        time.sleep(0.05)
        user32.keybd_event(0x11, 0, 0, 0)
        user32.keybd_event(0x56, 0, 0, 0)
        time.sleep(0.01)
        user32.keybd_event(0x56, 0, 2, 0)
        user32.keybd_event(0x11, 0, 2, 0)
    except Exception as e:
        print(f"粘贴失败: {e}")
        pyautogui.hotkey("ctrl", "v")


def mouse_move(dx, dy):
    """相对移动: mouse_event 是Windows唯一不受UIPI限制的API, 可穿透管理员窗口"""
    try:
        user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)  # MOUSEEVENTF_MOVE
    except Exception as e:
        print(f"移动失败: {e}")


def mouse_click(button):
    try:
        if button.endswith(":down"):
            btn, a = button[:-5], 0   # 只按下, 不释放(拖拽用)
        elif button.endswith(":up"):
            btn, a = button[:-3], 1   # 只释放
        else:
            btn, a = button, -1       # 完整点击(down+up)
        act = {"left": (0x0002, 0x0004), "right": (0x0008, 0x0010), "middle": (0x0020, 0x0040)}
        if btn in act:
            d, u = act[btn]
            if a == -1:
                user32.mouse_event(d, 0, 0, 0, 0); user32.mouse_event(u, 0, 0, 0, 0)
            elif a == 0:
                user32.mouse_event(d, 0, 0, 0, 0)
            else:
                user32.mouse_event(u, 0, 0, 0, 0)
    except Exception as e:
        print(f"点击失败: {e}")


def mouse_scroll(delta):
    """delta: 滚轮刻度，支持小于 1 的高分辨率增量。"""
    try:
        wheel_delta = round(delta * 120)
        if wheel_delta:
            user32.mouse_event(0x0800, 0, 0, wheel_delta, 0)  # WHEEL_DELTA = 120
    except Exception as e:
        print(f"滚轮失败: {e}")


# 所有按键统一用 keybd_event(即时, 无 pyautogui 的 PAUSE 延迟)
# 普通键: 虚拟键码(vk) + 扫描码(scan) + 是否扩展键(0xE0前缀)
KEY_MAP = {
    "Backspace": (0x08, 0x0E, False),
    "Enter":     (0x0D, 0x1C, False),
    "Delete":    (0x2E, 0x53, True),
    "Up":    (0x26, 0x48, False),
    "Down":  (0x28, 0x50, False),
    "Left":  (0x25, 0x4B, False),
    "Right": (0x27, 0x4D, False),
    "Esc":      (0x1B, 0x01, False),
    "Tab":      (0x09, 0x0F, False),
    "CapsLock": (0x14, 0x3A, False),
    "Space":    (0x20, 0x39, False),
    "Shift":    (0x10, 0x2A, False),
    "Ctrl":     (0x11, 0x1D, False),
    "Alt":      (0x12, 0x38, False),
    "Win":      (0x5B, 0x5B, True),
    "Menu":     (0x5D, 0x5D, True),
    "F1":  (0x70, 0x3B, False), "F2":  (0x71, 0x3C, False),
    "F3":  (0x72, 0x3D, False), "F4":  (0x73, 0x3E, False),
    "F5":  (0x74, 0x3F, False), "F6":  (0x75, 0x40, False),
    "F7":  (0x76, 0x41, False), "F8":  (0x77, 0x42, False),
    "F9":  (0x78, 0x43, False), "F10": (0x79, 0x44, False),
    "F11": (0x7A, 0x45, False), "F12": (0x7B, 0x58, False),
}

# 系统/多媒体键走专用扫描码
SPECIAL_KEYS = {
    "PrtSc":   (0x2C, 0x37, True),
    "VolUp":   (0xAF, 0x30, True),
    "VolDown": (0xAE, 0x2E, True),
    "BriUp":   (0xA6, 0x26, True),
    "BriDown": (0xA7, 0x25, True),
}


def _tap(vk, scan, ext):
    flags = 0x0001 if ext else 0  # KEYEVENTF_EXTENDEDKEY
    user32.keybd_event(vk, scan, flags, 0)
    user32.keybd_event(vk, scan, flags | 0x0002, 0)  # KEYUP


def key_down(key):
    if key in KEY_MAP:
        vk, scan, ext = KEY_MAP[key]
        try:
            user32.keybd_event(vk, scan, 0x0001 if ext else 0, 0)
        except Exception as e:
            print(f"按键失败 {key}: {e}")
        return
    if len(key) == 1:
        try:
            res = user32.VkKeyScanW(ord(key))
            vk = res & 0xFF
            sh = (res >> 8) & 0x01
            scan = user32.MapVirtualKeyW(vk, 0)
            if sh:
                user32.keybd_event(0x10, 0x2A, 0, 0)
            user32.keybd_event(vk, scan, 0, 0)
        except Exception as e:
            print(f"字符键失败 {key}: {e}")
        return

def key_up(key):
    if key in KEY_MAP:
        vk, scan, ext = KEY_MAP[key]
        try:
            user32.keybd_event(vk, scan, (0x0001 if ext else 0) | 0x0002, 0)
        except Exception as e:
            print(f"按键失败 {key}: {e}")
        return
    if len(key) == 1:
        try:
            res = user32.VkKeyScanW(ord(key))
            vk = res & 0xFF
            sh = (res >> 8) & 0x01
            scan = user32.MapVirtualKeyW(vk, 0)
            user32.keybd_event(vk, scan, 0x0002, 0)
            if sh:
                user32.keybd_event(0x10, 0x2A, 0x0002, 0)
        except Exception as e:
            print(f"字符键失败 {key}: {e}")
        return

def send_special(key):
    if key == "WinV":
        try:
            # Win 按下 -> V 单击 -> Win 抬起 (vk 0x5B = VK_LWIN)
            user32.keybd_event(0x5B, 0x5B, 0, 0)
            _tap(0x56, 0x2F, False)
            user32.keybd_event(0x5B, 0x5B, 0x0002, 0)
        except Exception as e:
            print(f"组合键失败 {key}: {e}")
        return
    if key == "PrtSc":
        try:
            # Win+Shift+S 调出截图工具 (比 PrtSc 复制全屏更直观可靠)
            user32.keybd_event(0x5B, 0x5B, 0, 0)
            user32.keybd_event(0x10, 0x2A, 0, 0)
            _tap(0x53, 0x1F, False)
            user32.keybd_event(0x10, 0x2A, 0x0002, 0)
            user32.keybd_event(0x5B, 0x5B, 0x0002, 0)
        except Exception as e:
            print(f"截图失败: {e}")
        return
    if key == "CtrlC":
        try:
            user32.keybd_event(0x11, 0x1D, 0, 0)       # Ctrl down
            _tap(0x43, 0x2E, False)                    # C
            user32.keybd_event(0x11, 0x1D, 0x0002, 0)  # Ctrl up
        except Exception as e:
            print(f"复制失败: {e}")
        return
    if key in KEY_MAP:
        vk, scan, ext = KEY_MAP[key]
        try:
            _tap(vk, scan, ext)
        except Exception as e:
            print(f"按键失败 {key}: {e}")
        return
    # 单字符键 (字母/数字/符号): VkKeyScanW 解析 vk + shift 状态
    if len(key) == 1:
        try:
            res = user32.VkKeyScanW(ord(key))
            vk = res & 0xFF
            sh = (res >> 8) & 0x01
            scan = user32.MapVirtualKeyW(vk, 0)  # MAPVK_VK_TO_VSC
            if sh:
                user32.keybd_event(0x10, 0x2A, 0, 0)        # Shift down
            _tap(vk, scan, False)
            if sh:
                user32.keybd_event(0x10, 0x2A, 0x0002, 0)    # Shift up
        except Exception as e:
            print(f"字符键失败 {key}: {e}")
        return
    info = SPECIAL_KEYS.get(key)
    if not info:
        return
    vk, scan, ext = info
    try:
        _tap(vk, scan, ext)
    except Exception as e:
        print(f"按键失败 {key}: {e}")


def handle_command(msg):
    if msg.startswith("MMOVE "):
        parts = msg.split()
        if len(parts) == 3:
            mouse_move(float(parts[1]), float(parts[2]))
    elif msg.startswith("MCLICK "):
        mouse_click(msg.split()[1])
    elif msg.startswith("MSCROLL "):
        try:
            mouse_scroll(float(msg.split()[1]))
        except (ValueError, IndexError):
            pass
    elif msg.startswith("KEYDN "):
        key_down(msg.split(" ", 1)[1].strip())
    elif msg.startswith("KEYUP "):
        key_up(msg.split(" ", 1)[1].strip())
    elif msg.startswith("KEY "):
        send_special(msg.split(" ", 1)[1].strip())
    else:
        type_text(msg)


async def ws_handler(ws):
    print(f"已连接: {ws.remote_address}")
    loop = asyncio.get_running_loop()
    try:
        async for msg in ws:
            if msg == "__PING__":
                await ws.send("__PONG__")
                continue
            try:
                await loop.run_in_executor(None, handle_command, str(msg))  # 线程池执行, 不阻塞 event loop
            except Exception as e:
                print(str(e))
    except:
        pass
    finally:
        print("已断开")


async def main():
    ip = get_ip()
    if ip == "127.0.0.1":
        print("无法获取局域网 IP"); sys.exit(1)

    hp, wp = 8766, 8765
    url = f"http://{ip}:{hp}"

    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=1)
    qr.add_data(url); qr.make(fit=True)
    qr.print_ascii(invert=True)
    print(f"\n  手机键盘 → {url}")
    print("  鼠标放到目标窗口，发送即粘贴\n")

    httpd = HTTPServer(("0.0.0.0", hp), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    async with websockets.serve(ws_handler, "0.0.0.0", wp, ping_interval=15, ping_timeout=10):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n已退出")
    except OSError as e:
        print(f"\n启动失败: {e}")

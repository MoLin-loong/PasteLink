"""手机快速输入 — 手机当电脑键盘，扫码即用"""
import asyncio, os, socket, sys, threading, time, ctypes

if sys.platform == "win32":
    sys.stdout.reconfigure(errors="replace") if hasattr(sys.stdout, "reconfigure") else None
    os.environ["PYTHONIOENCODING"] = "utf-8"
from http.server import HTTPServer, BaseHTTPRequestHandler
import qrcode, websockets, pyperclip, pyautogui

pyautogui.FAILSAFE = True

HTML = r"""<!DOCTYPE html>
<html lang=zh-CN>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1,user-scalable=no">
<title>手机键盘</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,sans-serif;background:#1a1a2e;color:#eee;display:flex;flex-direction:column;height:100vh}
.header{padding:12px 16px;background:#16213e;display:flex;align-items:center;gap:10px}
.dot{width:10px;height:10px;border-radius:50%;background:#e94560}
.dot.on{background:#4ecca3}
.status{font-size:14px;color:#aaa}
.input-area{flex:1;display:flex;flex-direction:row;padding:12px;gap:12px}
textarea{flex:1;background:#16213e;border:1px solid #0f3460;border-radius:12px;padding:14px;color:#eee;font-size:16px;resize:none;outline:none}
textarea:focus{border-color:#4ecca3}
.btn-row{display:flex;flex-direction:column;gap:8px;width:90px}
button{flex:1;padding:14px;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer}
#send{background:#4ecca3;color:#1a1a2e}
#clear{background:#0f3460;color:#aaa}
</style>
<div class=header><div class=dot id=dot></div><span class=status id=status>正在连接...</span></div>
<div class=input-area>
<textarea id=msg placeholder="输入文字..." autofocus></textarea>
<div class=btn-row><button id=clear>清空</button><button id=send>发送</button></div>
</div>
<script>
var ws,rt,h=location.hostname;
function conn(){
 ws=new WebSocket("ws://"+h+":8765");
 ws.onopen=function(){document.getElementById("dot").className="dot on";document.getElementById("status").textContent="已连接"};
 ws.onclose=function(){document.getElementById("dot").className="dot";document.getElementById("status").textContent="已断开，重连中...";clearTimeout(rt);rt=setTimeout(conn,3000)};
 ws.onerror=function(){ws.close()};
}
function send(){
 var t=document.getElementById("msg").value;
 if(!t||!ws||ws.readyState!==1)return;
 ws.send(t);document.getElementById("msg").value="";document.getElementById("msg").focus();
}
document.getElementById("send").onclick=send;
document.getElementById("clear").onclick=function(){document.getElementById("msg").value="";document.getElementById("msg").focus()};
document.getElementById("msg").onkeydown=function(e){if(e.key=="Enter"&&!e.shiftKey){e.preventDefault();send()}};
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
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        hwnd = ctypes.windll.user32.WindowFromPoint(point)
        hwnd = ctypes.windll.user32.GetAncestor(hwnd, 2)
        ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.keybd_event(0x56, 0, 2, 0)
        ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)
    except Exception as e:
        print(f"粘贴失败: {e}")
        pyautogui.hotkey("ctrl", "v")


async def ws_handler(ws):
    print(f"已连接: {ws.remote_address}")
    try:
        async for msg in ws:
            if msg == "__PING__":
                await ws.send("__PONG__")
                continue
            print(f"收到: {msg}")
            try:
                type_text(str(msg))
                await ws.send("ok")
            except Exception as e:
                print(str(e))
                await ws.send("err")
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

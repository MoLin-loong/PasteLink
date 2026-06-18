#!/usr/bin/env python3
import asyncio, socket, subprocess, sys, signal, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import qrcode, qrcode.constants
import websockets

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
.input-area{flex:1;display:flex;flex-direction:column;padding:12px;gap:12px}
textarea{flex:1;background:#16213e;border:1px solid #0f3460;border-radius:12px;padding:14px;color:#eee;font-size:16px;resize:none;outline:none}
textarea:focus{border-color:#4ecca3}
.btn-row{display:flex;gap:10px}
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


USE_WAYLAND = subprocess.run(["which", "wl-copy"], capture_output=True).returncode == 0 and \
              subprocess.run(["which", "ydotool"], capture_output=True).returncode == 0
USE_XDOTOOL = subprocess.run(["which", "xdotool"], capture_output=True).returncode == 0


def type_text(text):
    if USE_WAYLAND:
        subprocess.run(["wl-copy"], input=text.encode(), timeout=5)
        subprocess.run(["ydotool", "key", "ctrl+shift+v"], timeout=5)
        subprocess.run(["ydotool", "key", "ctrl+v"], timeout=5)
    elif USE_XDOTOOL:
        subprocess.run(["xdotool", "type", "--clearmodifiers", text], timeout=5)
    else:
        raise RuntimeError("请安装 wl-copy+ydotool 或 xdotool")


async def ws_handler(ws):
    print(f"[+] 已连接: {ws.remote_address}")
    try:
        async for msg in ws:
            print(f"[*] {msg}")
            try:
                type_text(str(msg))
                await ws.send("ok")
            except Exception as e:
                print(f"[-] {e}")
                await ws.send("err")
    except:
        pass
    finally:
        print("[-] 已断开")


async def main():
    ip = get_ip()
    if ip == "127.0.0.1":
        print("无法获取局域网 IP"); sys.exit(1)

    hp, wp = 8766, 8765
    url = f"http://{ip}:{hp}"

    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=1)
    qr.add_data(url); qr.make(fit=True)
    qr.print_ascii(invert=True)
    print()

    print("=" * 50)
    print("  Phone Keyboard")
    print(f"\n  {url}\n")
    print("  手机输入 → 发送 → 出现在光标处")
    print("  Ctrl+C 退出")
    print("=" * 50)

    httpd = HTTPServer(("0.0.0.0", hp), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    stop = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_running_loop().add_signal_handler(sig, stop.set)

    async with websockets.serve(ws_handler, "0.0.0.0", wp):
        await stop.wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n已退出")
    except OSError as e:
        print(f"\n启动失败: {e}")

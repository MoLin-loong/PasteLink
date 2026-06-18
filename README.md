# PasteLink

Paste text from your phone directly to your PC cursor. Zero app install on the phone, just scan and type.

---

# PasteLink —— 为氛围编程而生的懒人打字工具

想象一下：你正瘫在沙发里跟 AI 一起写代码，整个人处于那种“随口一说，代码就出来了”的轻松状态。可每次还得爬起来敲键盘、把一大段提示词一个字一个字打进去——气氛瞬间就碎了。

PasteLink 就是为这个瞬间准备的。  
你只需要对着手机说话，语音识别后的文字就会直接「粘」到电脑光标闪动的地方。  
整个过程你的手甚至不用碰键盘，保持那种慵懒又专注的节奏，让 AI 自己干活去。

要用起来也很简单：
- 📱 手机和电脑连着同一个 Wi-Fi（同一局域网）
- 🖥️ 电脑上运行 PasteLink，屏幕上会出现一个二维码
- 📷 手机扫一下码，浏览器就打开了连接页面
- 🎤 在手机上说话（或用输入法打字），点一下发送，文字立刻出现在电脑光标处

手机上不用装任何 App，有浏览器就够了。

---

## Features / 特点

- **Zero Installation**: No app needed on phone, just scan QR code
- **Instant Use**: Open web keyboard in phone browser, type and send
- **Precise Placement**: Text pastes exactly where your mouse cursor is
- **Cross-Platform**: Supports both Windows and Linux
- **Portable Version**: Windows portable (.exe) available, no Python required
- **Real-time Connection**: WebSocket for low-latency communication
- **Auto-Reconnect**: Automatic reconnection on network interruptions

- **专为氛围编程设计** —— 语音输入 → 电脑光标，不打断思路
- **零摩擦连接** —— 扫码即连，无需注册、配对、输入 IP
- **支持中文** —— 基于剪贴板粘贴，完美兼容中文、符号、换行
- **两种形态，任你选择**：
  - 原始 Python 脚本（`pastelink.py`）
  - 打包好的 Windows `.exe`（双击即用，无需安装 Python 环境）
- **极简安全** —— 服务仅在局域网内可访问

---

## 📦 File Description / 文件说明

| File / 文件 | Usage / 用途 |
|-------------|--------------|
| `pastelink.py` | Python 源码，适合开发者或定制使用 |
| `PasteLink.exe` | Windows 打包版本，无需 Python 环境 |

> 注：`ps1` 为可选的快速启动方式，并非必需。

---

## 🚀 Quick Start / 快速开始

### Option 1: Direct Run (Recommended) / 方式一：使用 Windows `.exe`（推荐，最简单）

1. Download `PasteLink.exe` to your computer / 下载 `PasteLink.exe` 到你的电脑
2. Double-click to run / 双击运行
3. Ensure phone and PC are on the same Wi-Fi / 确保手机和电脑连接同一个 Wi-Fi
4. Scan QR code in the command window / 在电脑弹出的命令行窗口中，用手机扫描二维码
5. Start typing after "Connected" / 手机页面显示“已连接”后，开始发送文字

### Option 2: Run from Source / 方式二：运行 Python 脚本

**Requires Python 3.7+ / 需要 Python 3.7+ 环境**

1. Install dependencies / 安装依赖：
   ```bash
   pip install qrcode websockets pyperclip pyautogui
   ```

2. Run script / 运行脚本：
   ```bash
   python PasteLink.py
   ```

### Linux

```bash
# Install dependencies / 安装依赖
pip install qrcode websockets

# Install system tools / 安装系统工具
sudo apt install xdotool          # X11 desktop / X11 桌面
# or / 或
sudo apt install wl-clipboard ydotool  # Wayland desktop / Wayland 桌面

# Run script / 运行脚本
python Linux/PasteLink_Linux.py
```

---

## Usage / 使用说明

1. After running the script, terminal shows QR code and access URL / 运行脚本后，终端会显示二维码和访问地址
2. Scan QR code with phone or manually enter address / 手机扫描二维码或手动输入地址
3. Phone browser opens a simple input interface / 手机浏览器会打开一个简洁的输入界面
4. Type text on phone, click "Send" button / 在手机上输入文字，点击"发送"按钮
5. Text immediately pastes at PC mouse cursor position / 文字会立即粘贴到电脑鼠标光标所在位置

---

## System Requirements / 系统要求

### Windows
- Windows 10 or later / Windows 10 或更高版本
- Portable version doesn't require Python / 便携版无需 Python 环境

### Linux
- Python 3.7+
- X11 or Wayland desktop environment / X11 或 Wayland 桌面环境
- System tools: `xdotool` (X11) or `wl-clipboard` + `ydotool` (Wayland) / 系统工具：`xdotool`（X11）或 `wl-clipboard` + `ydotool`（Wayland）

---

## Dependencies / 依赖项

- `qrcode` - QR code generation / 生成二维码
- `websockets` - WebSocket communication / WebSocket 通信
- `pyperclip` - Clipboard operations (Windows only) / 剪贴板操作（仅 Windows）
- `pyautogui` - Keyboard simulation (Windows only, fallback) / 模拟键盘输入（仅 Windows，备用方案）

---

## Network Configuration / 网络配置

- Default ports / 默认端口：
  - HTTP server: 8766 (phone web access) / HTTP 服务：8766（手机网页访问）
  - WebSocket: 8765 (real-time communication) / WebSocket：8765（实时通信）
- Ensure phone and PC are on the same local network / 确保手机和电脑在同一局域网内
- If firewall issues occur, allow traffic on these ports / 如遇防火墙问题，请放行上述端口

---

## Exiting / 退出程序

Press `Ctrl+C` to exit the program. / 按 `Ctrl+C` 退出程序。

---

## License / 许可证

MIT License - See [LICENSE](LICENSE) file for details. / MIT License - 详见 [LICENSE](LICENSE) 文件

---

## Contributing / 贡献

Issues and Pull Requests are welcome! / 欢迎提交 Issue 和 Pull Request！

---

## Author / 作者

MoLin-loong
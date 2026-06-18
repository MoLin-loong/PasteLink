# PasteLink

手机打字，直接"粘贴"到电脑光标处。

## 功能特点

- **零安装**：手机无需安装任何应用，扫描二维码即可使用
- **即扫即用**：手机浏览器打开网页，输入文字后发送
- **精准定位**：文字直接粘贴到电脑鼠标光标所在位置
- **跨平台支持**：支持 Windows 和 Linux 系统
- **便携版**：提供 Windows 便携版（.exe），无需 Python 环境
- **实时连接**：WebSocket 实现低延迟实时通信
- **自动重连**：网络中断后自动重连机制

## 工作原理

1. 电脑运行脚本，显示二维码
2. 手机扫描二维码，打开网页键盘
3. 手机输入文字，点击发送
4. 文字直接粘贴到电脑当前光标位置

## 快速开始

### Windows 版本

#### 方式一：直接运行（推荐）

双击 `PasteLink.exe` 即可启动，无需安装 Python。

#### 方式二：从源码运行

```bash
# 安装依赖
pip install qrcode websockets pyperclip pyautogui

# 运行脚本
python PasteLink.py
```

### Linux 版本

```bash
# 安装依赖
pip install qrcode websockets

# 安装系统工具
sudo apt install xdotool          # X11 桌面
# 或
sudo apt install wl-clipboard ydotool  # Wayland 桌面

# 运行脚本
python Linux/PasteLink_Linux.py
```

## 使用说明

1. 运行脚本后，终端会显示二维码和访问地址
2. 手机扫描二维码或手动输入地址（如 `http://192.168.1.100:8766`）
3. 手机浏览器会打开一个简洁的输入界面
4. 在手机上输入文字，点击"发送"按钮
5. 文字会立即粘贴到电脑鼠标光标所在位置

## 系统要求

### Windows
- Windows 10 或更高版本
- 便携版无需 Python 环境

### Linux
- Python 3.7+
- X11 或 Wayland 桌面环境
- 系统工具：`xdotool`（X11）或 `wl-clipboard` + `ydotool`（Wayland）

## 依赖项

- `qrcode` - 生成二维码
- `websockets` - WebSocket 通信
- `pyperclip` - 剪贴板操作（仅 Windows）
- `pyautogui` - 模拟键盘输入（仅 Windows，备用方案）

## 网络配置

- 默认端口：
  - HTTP 服务：8766（手机网页访问）
  - WebSocket：8765（实时通信）
- 确保手机和电脑在同一局域网内
- 如遇防火墙问题，请放行上述端口

## 退出程序

按 `Ctrl+C` 退出程序。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

MoLin-loong

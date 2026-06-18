# PasteLink

[![中文](https://img.shields.io/badge/语言-中文-blue)](README_CN.md) | [![English](https://img.shields.io/badge/Language-English-green)](README.md)

Paste text from your phone directly to your PC cursor. Zero app install on the phone, just scan and type.

## Features

- **Zero Installation**: No app needed on phone, just scan QR code
- **Instant Use**: Open web keyboard in phone browser, type and send
- **Precise Placement**: Text pastes exactly where your mouse cursor is
- **Cross-Platform**: Supports both Windows and Linux
- **Portable Version**: Windows portable (.exe) available, no Python required
- **Real-time Connection**: WebSocket for low-latency communication
- **Auto-Reconnect**: Automatic reconnection on network interruptions

## How It Works

1. Run script on PC, displays QR code
2. Scan QR code with phone to open web keyboard
3. Type on phone, click send
4. Text pastes directly at PC cursor position

## Quick Start

### Windows

#### Option 1: Direct Run (Recommended)

Double-click `PasteLink.exe` to start. No Python installation needed.

#### Option 2: Run from Source

```bash
# Install dependencies
pip install qrcode websockets pyperclip pyautogui

# Run script
python PasteLink.py
```

### Linux

```bash
# Install dependencies
pip install qrcode websockets

# Install system tools
sudo apt install xdotool          # X11 desktop
# or
sudo apt install wl-clipboard ydotool  # Wayland desktop

# Run script
python Linux/PasteLink_Linux.py
```

## Usage

1. After running the script, terminal shows QR code and access URL
2. Scan QR code with phone or manually enter address (e.g., `http://192.168.1.100:8766`)
3. Phone browser opens a simple input interface
4. Type text on phone, click "Send" button
5. Text immediately pastes at PC mouse cursor position

## System Requirements

### Windows
- Windows 10 or later
- Portable version doesn't require Python

### Linux
- Python 3.7+
- X11 or Wayland desktop environment
- System tools: `xdotool` (X11) or `wl-clipboard` + `ydotool` (Wayland)

## Dependencies

- `qrcode` - QR code generation
- `websockets` - WebSocket communication
- `pyperclip` - Clipboard operations (Windows only)
- `pyautogui` - Keyboard simulation (Windows only, fallback)

## Network Configuration

- Default ports:
  - HTTP server: 8766 (phone web access)
  - WebSocket: 8765 (real-time communication)
- Ensure phone and PC are on the same local network
- If firewall issues occur, allow traffic on these ports

## Exiting

Press `Ctrl+C` to exit the program.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Issues and Pull Requests are welcome!

## Author

MoLin-loong
# PasteLink

<p align="center">
  <img src="ABB_rounded.png" alt="PasteLink icon" width="96">
</p>

<p align="center">
  <a href="README_CN.md">中文</a> · <strong>English</strong>
</p>

Use a phone browser as a low-latency keyboard and touchpad for your computer. The phone needs no app: run PasteLink on the computer, scan the QR code, and start using it on the same local network.

## Highlights

- **No phone installation** — the controller runs entirely in the mobile browser.
- **Combined input and touchpad view** — the text area and trackpad stay on one screen.
- **Adaptive layout** — focusing the text area enlarges it; touching the trackpad enlarges the trackpad and dismisses the phone keyboard.
- **Responsive mouse control** — one-finger relative movement, tap-to-left-click, and frame-coalesced two-finger smooth scrolling.
- **Convenient mouse buttons** — left and right mouse buttons sit beside the up-arrow key.
- **Keyboard controls** — Enter, Backspace, arrow keys, clipboard history, and a full keyboard layout.
- **Adjustable behavior** — mouse sensitivity, scroll speed, Backspace repeat rate, and bottom safe-area padding are persisted in the browser.
- **Portable Windows build** — `PasteLink.exe` runs without a local Python installation.

## Quick Start

### Windows portable version

1. Download or clone this repository.
2. Double-click `PasteLink.exe`.
3. Scan the terminal QR code with the phone, or open the displayed address manually.
4. Keep the phone and computer on the same local network.

### Run from source on Windows

```powershell
pip install qrcode websockets pyperclip pyautogui
python PasteLink.py
```

### Run from source on Linux

```bash
pip install qrcode websockets

# X11
sudo apt install xdotool

# Wayland alternative
sudo apt install wl-clipboard ydotool

python Linux/PasteLink_Linux.py
```

The Linux implementation currently focuses on remote text input. The combined touchpad, simulated mouse buttons, and extended keyboard controls are provided by the Windows implementation.

## Using the Mobile Interface

### Text input

1. Tap the text area. It expands while the trackpad compresses.
2. Type on the phone and tap **Send**.
3. PasteLink copies the text to the computer and pastes it into the active target window.

The quick-key area also provides Enter, Backspace, arrow keys, and Windows clipboard history (`Win+V`). Backspace supports press-and-hold repeat.

### Touchpad

Tap or touch the trackpad below the text area. It expands while the text area compresses and the mobile software keyboard closes.

- **One-finger drag:** move the computer pointer relatively.
- **One-finger tap:** left-click.
- **Two-finger vertical swipe:** smooth high-resolution scrolling.
- **Left / Right buttons beside `↑`:** press and release the corresponding mouse button; holding a button can be used for drag operations.

The top-right keyboard/mouse button switches focus between the two areas. The neighboring full-keyboard button opens the complete keyboard layout.

### Settings

Use the gear button to adjust:

- Mouse sensitivity
- Scroll speed
- Backspace repeat interval
- Bottom padding for phones with a large safe area or black navigation bar

Settings are stored locally in the phone browser.

## Network and Security

PasteLink listens on all local interfaces and does not provide authentication or transport encryption. Use it only on a trusted private network, and close the program when it is not needed.

- HTTP interface: `8766`
- WebSocket control channel: `8765`
- Phone and computer must be able to reach each other on the LAN.
- If startup reports `WinError 10048`, another PasteLink process is already using the ports. Close the earlier process before starting a new one.

## Development

Run the regression tests with:

```powershell
python -m unittest discover -s tests -v
```

Important project files:

- `PasteLink.py` — Windows server and embedded mobile interface
- `PasteLink.exe` — portable Windows executable
- `Linux/PasteLink_Linux.py` — Linux text-input implementation
- `tests/` — layout and high-resolution scrolling regression tests

## License

[MIT](LICENSE)

## Contributing

Issues and pull requests are welcome.

## Author

MoLin-loong

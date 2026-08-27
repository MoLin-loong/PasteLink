# PasteLink

<p align="center">
  <img src="ABB_rounded.png" alt="PasteLink 图标" width="96">
</p>

<p align="center">
  <strong>中文</strong> · <a href="README.md">English</a>
</p>

把手机浏览器变成电脑的低延迟键盘和触控板。手机无需安装 App：在电脑运行 PasteLink，扫描二维码后即可在同一局域网内使用。

## 功能亮点

- **手机零安装**：全部操作都在手机浏览器中完成。
- **输入框与触控板同屏**：不再进入两个互相独立的页面。
- **自适应布局**：点击输入框时输入区展开；触摸触控板时触控板展开，并自动收起手机软键盘。
- **跟手的鼠标控制**：单指相对移动、轻点左键，以及按帧合并的双指高分辨率平滑滚动。
- **鼠标按键顺手可用**：鼠标左键和右键位于上箭头两侧。
- **丰富的键盘控制**：回车、退格、方向键、剪贴板历史以及完整键盘布局。
- **可调节手感**：鼠标灵敏度、滚轮速度、退格连发间隔和底部安全区均可设置，并保存在手机浏览器中。
- **Windows 便携版**：直接运行 `PasteLink.exe`，电脑无需安装 Python。

## 快速开始

### Windows 便携版

1. 下载或克隆本仓库。
2. 双击 `PasteLink.exe`。
3. 用手机扫描终端中的二维码，或手动打开终端显示的地址。
4. 确保手机与电脑连接到同一局域网。

### Windows 源码运行

```powershell
pip install qrcode websockets pyperclip pyautogui
python PasteLink.py
```

### Linux 源码运行

```bash
pip install qrcode websockets

# X11
sudo apt install xdotool

# Wayland 可选方案
sudo apt install wl-clipboard ydotool

python Linux/PasteLink_Linux.py
```

Linux 版本目前主要提供远程文字输入；组合触控板、模拟鼠标按键和扩展键盘控制由 Windows 版本提供。

## 手机界面使用方法

### 文字输入

1. 点击输入框，输入区域会展开，触控板会压缩。
2. 在手机输入文字后点击 **发送**。
3. PasteLink 会在电脑端复制文字，并粘贴到当前目标窗口。

快捷键区域还提供回车、退格、方向键和 Windows 剪贴板历史（`Win+V`）。退格键支持长按连发。

### 触控板

点击或触摸输入框下方的触控板。触控板会展开，输入框会压缩，同时手机软键盘会自动收起。

- **单指拖动**：相对移动电脑鼠标。
- **单指轻点**：鼠标左键单击。
- **双指上下滑动**：高分辨率平滑滚动。
- **`↑` 两侧的左键 / 右键**：按下和松开对应鼠标键；长按后移动可用于拖拽。

右上角的键盘/鼠标按钮用于在输入区与触控板之间切换焦点；旁边的完整键盘按钮可打开完整键盘布局。

### 设置

点击齿轮按钮可以调节：

- 鼠标灵敏度
- 滚轮速度
- 退格连发间隔
- 针对手机底部安全区或黑色导航栏的额外留白

设置会保存在手机浏览器本地。

## 网络与安全

PasteLink 会监听电脑的全部本地网络接口，目前不提供身份验证或传输加密。请仅在可信的私人网络中使用，并在不需要时关闭程序。

- HTTP 手机界面：`8766`
- WebSocket 控制通道：`8765`
- 手机与电脑必须能够在局域网内互相访问。
- 如果启动时出现 `WinError 10048`，表示已有 PasteLink 进程占用了端口，请先关闭旧进程。

## 开发与测试

运行回归测试：

```powershell
python -m unittest discover -s tests -v
```

主要文件：

- `PasteLink.py`：Windows 服务端与内嵌手机界面
- `PasteLink.exe`：Windows 便携版
- `Linux/PasteLink_Linux.py`：Linux 文字输入实现
- `tests/`：组合布局与高分辨率滚动回归测试

## 许可证

[MIT](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request。

## 作者

MoLin-loong

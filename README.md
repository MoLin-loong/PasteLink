# PasteLink（粘贴即连）

## PasteLink – stay in the flow of vibe coding.

When you're vibe coding with AI, typing long prompts breaks the spell. Instead, just speak to your phone — the text instantly appears right where your cursor is on the PC. Both devices just need to be on the same local network. Scan a QR code shown on your PC, and you're connected. No app to install on the phone.

Comes as a raw Python script, plus a portable Windows `.exe` for those who don't want to touch Python at all.

---

## PasteLink —— 为氛围编程而生的懒人打字工具

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

## ✨ 特点

- **专为氛围编程设计** —— 语音输入 → 电脑光标，不打断思路
- **零摩擦连接** —— 扫码即连，无需注册、配对、输入 IP
- **支持中文** —— 基于剪贴板粘贴，完美兼容中文、符号、换行
- **两种形态，任你选择**：
  - 原始 Python 脚本（`pastelink.py`）
  - 打包好的 Windows `.exe`（双击即用，无需安装 Python 环境）
- **极简安全** —— 服务仅在局域网内可访问

---

## 📦 文件说明

| 文件 | 用途 |
|------|------|
| `pastelink.py` | Python 源码，适合开发者或定制使用 |
| `pastelink.ps1` | PowerShell 一键启动脚本（可选） |
| `PasteLink.exe` | Windows 打包版本，无需 Python 环境 |

> 注：`ps1` 为可选的快速启动方式，并非必需。

---

## 🚀 快速开始

### 方式一：使用 Windows `.exe`（推荐，最简单）
1. 下载 `PasteLink.exe` 到你的电脑
2. 双击运行
3. 确保手机和电脑连接同一个 Wi-Fi
4. 在电脑弹出的命令行窗口中，用手机扫描二维码
5. 手机页面显示“已连接”后，开始发送文字

### 方式二：运行 Python 脚本
**需要 Python 3.7+ 环境**

1. 安装依赖：
   ```bash
   pip install flask qrcode[pil] xdotool  # Linux 需加 xclip

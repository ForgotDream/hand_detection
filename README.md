# AI 虚拟鼠标

手势检测应用，使用 MediaPipe 实现基于手势的鼠标控制。

## 功能特性

- 实时手势检测
- 鼠标移动和点击控制
- 多平台支持（Windows、Linux、macOS）
- GPU 加速（在支持的平台上自动启用）

## 安装

### 要求

- Python 3.12
- 摄像头

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/ForgotDream/hand_detection.git
   cd hand_detection
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv .venv
   ```

3. 激活虚拟环境：
   - Windows: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`

4. 安装依赖：
   ```bash
   pip install -e .
   ```


## 运行

```bash
python main.py
```

## 平台支持

- **Windows**: CPU 模式（GPU 不支持）
- **Linux**: 支持 GPU 加速（如果有兼容的 GPU）
- **macOS**: 支持 GPU 加速

应用会自动检测平台并启用最佳的处理模式。

## 控制说明

- 食指控制鼠标移动
- 食指和中指靠近时按住鼠标

## 注意事项

- `Mediapipe` 仅支持到 Python 3.12!
- `MediaPipe` 0.10.14 以上的版本在 Windows 环境下会[运行失败](https://github.com/google-ai-edge/mediapipe/issues/5838)。
- Linux 系统在 Wayland 环境下运行需要设置 Qt 的平台为 Wayland：`export QT_QPA_PLATFORM=wayland`。

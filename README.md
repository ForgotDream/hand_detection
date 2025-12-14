# AI 虚拟鼠标

手势检测应用，使用MediaPipe实现基于手势的鼠标控制。

## 功能特性

- 实时手势检测
- 鼠标移动和点击控制
- 多平台支持（Windows、Linux、macOS）
- GPU加速（在支持的平台上自动启用）

## 安装

### 要求

- Python 3.12+
- 摄像头

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone github.com/ForgotDream/hand_detection.git
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

- **Windows**: CPU模式（GPU不支持）
- **Linux**: 支持GPU加速（如果有兼容的GPU）
- **macOS**: 支持GPU加速

应用会自动检测平台并启用最佳的处理模式。

## 控制说明

- 食指控制鼠标移动
- 食指和中指靠近时按住鼠标
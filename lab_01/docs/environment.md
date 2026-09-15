# 实验环境记录

## 基本信息

- 安装与验证日期：2026-09-15
- 操作系统：Microsoft Windows 11 家庭版 中文版
- 系统版本：10.0.26200
- 系统架构：64 位
- 开发工具：Visual Studio Code
- 虚拟环境：Conda 环境 `opencv`
- 环境路径：`C:\Users\w\.conda\envs\opencv`

## 软件版本

- Python：3.12.14
- OpenCV：5.0.0
- NumPy：2.5.3
- Matplotlib：3.11.2

## 验证命令

```powershell
conda activate opencv
python -c "import sys, cv2, numpy, matplotlib; print('Python:', sys.version); print('OpenCV:', cv2.__version__); print('NumPy:', numpy.__version__); print('Matplotlib:', matplotlib.__version__)"
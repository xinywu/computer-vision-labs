# computer-vision-labs

数字图像处理与计算机视觉课程实验。

## 实验列表

### 实验一 需求分析与 OpenCV 环境基线

实验一完成了图像读取、属性检查、灰度转换和结果保存的基础处理流程。

主要内容：

- 使用 Python、NumPy 和 OpenCV 处理静态图像
- 通过命令行参数传入输入和输出路径
- 支持彩色、灰度、RGBA 和中文路径图像
- 处理文件不存在、文件损坏和输出目录不存在等情况
- 完成需求分析、环境记录和 10 个测试用例
- 保存运行日志、输出图像和截图证据

实验目录：[lab_01](./lab_01)

运行示例：

```powershell
conda activate opencv
python lab_01\src\baseline_pipeline.py --input lab_01\data\input\color.png --output lab_01\data\output\t01_color_gray.png
```

执行全部测试：

```powershell
python lab_01\src\run_tests.py
```
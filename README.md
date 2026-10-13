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

## 实验二 图像基本运算与直方图均衡化

实验二完成了灰度变换、图像代数运算、直方图统计和直方图均衡化。

主要内容：

- 实现线性灰度变换和两种伽马校正
- 对比 NumPy 加法与 OpenCV 饱和加法
- 实现图像加权混合和绝对差值
- 比较暗图、正常图和低对比度图的直方图
- 手写 CDF 直方图均衡化
- 将手写结果与 `cv2.equalizeHist` 进行对比
- 完成需求评审、MVP 范围确定和 OpenCV API 调研
- 保存分类结果、实验报告和运行证据

实验目录：[lab_02](./lab_02)

运行实验二全部程序：

```powershell
conda activate opencv
python lab_02\src\transform.py
python lab_02\src\arith.py
python lab_02\src\hist_equalize.py
```

实验文档：

- [实验报告](./lab_02/docs/report.md)
- [需求评审与 MVP 范围](./lab_02/docs/mvp_review.md)
- [OpenCV API 调研](./lab_02/docs/api_notes.md)

## 实验三 空间滤波与图像增强

实验三完成了高斯噪声与椒盐噪声生成、空间滤波、图像锐化以及 PSNR/SSIM 质量评价。

主要内容：

- 生成高斯噪声和椒盐噪声图像
- 对比均值滤波、高斯滤波和中值滤波
- 验证高斯滤波更适合处理高斯噪声
- 验证中值滤波更适合处理椒盐噪声
- 实现拉普拉斯锐化和 USM 锐化
- 使用 PSNR 和 SSIM 定量评价处理结果
- 绘制 SFM 系统数据流图并标注预处理模块边界
- 定义统一的 `uint8 BGR` 预处理接口
- 保存实验结果、评分表、报告和运行证据

实验目录：[lab_03](./lab_03)

运行实验三：

```powershell
conda activate opencv
python lab_03\src\spatial_filtering.py
```

实验文档：

- [实验报告](./lab_03/docs/report.md)
- [SFM 系统架构](./lab_03/docs/architecture.md)
- [预处理接口约定](./lab_03/docs/interface_agreement.md)


## 实验四 边缘检测与图像分割

实验四完成了 Sobel 梯度、Canny 边缘检测、固定阈值、Otsu 自动阈值和自适应阈值实验。

主要内容：

- 比较大小为 3 和 5 的 Sobel 卷积核
- 比较三组 Canny 双阈值
- 比较固定阈值与 Otsu 自动阈值
- 验证自适应阈值对光照不均图像的处理效果
- 编写详细设计和编码规范文档

实验目录：[lab_04](./lab_04)

运行实验四：

```powershell
python lab_04\src\edge_segmentation.py
```

实验文档：

- [实验说明](./lab_04/README.md)
- [详细设计](./lab_04/docs/detailed_design.md)
- [编码规范](./lab_04/docs/coding_standards.md)

## 实验五 角点检测与尺度空间

实验五完成了 Harris 角点检测、Shi-Tomasi 角点检测、图像金字塔和 DoG 尺度空间实验。

主要内容：

- 比较不同参数下的 Harris 角点检测结果
- 提取 Shi-Tomasi 角点并与 Harris 结果对比
- 构建四层图像金字塔
- 计算相邻尺度的 DoG 图像
- 编写并运行自动化测试

实验目录：[lab_05](./lab_05)

运行实验五：

```powershell
python lab_05\src\run_experiment.py
python -m pytest lab_05\tests -v
```

实验文档：

- [实验说明](./lab_05/README.md)
- [实验报告](./lab_05/docs/report.md)

## 实验六 SIFT 特征提取与描述

实验六完成了 SIFT 关键点检测、128 维描述子提取、参数实验，以及旋转和尺度不变性验证。

主要内容：

- 提取并可视化 SIFT 关键点
- 比较 `nfeatures`、`contrastThreshold` 和 `edgeThreshold`
- 验证 SIFT 对 30° 旋转和 0.6 倍缩放的鲁棒性
- 使用 BFMatcher 和 Lowe ratio test 完成特征匹配
- 将提取功能封装为 `extract_sift(img, cfg)`
- 完成 3 项自动化测试

实验目录：[lab_06](./lab_06)

运行实验六：

```powershell
python lab_06\src\sift_experiment.py
python lab_06\src\parameter_experiment.py
python lab_06\src\invariance_experiment.py
python -m unittest discover -s lab_06\tests -v
```

实验文档：

- [实验说明](./lab_06/README.md)
- [实验报告](./lab_06/docs/report.md)
# 实验二 图像基本运算与直方图均衡化

本实验使用 Python、NumPy、OpenCV 和 Matplotlib 完成图像灰度变换、代数运算、直方图统计及直方图均衡化，并对实验一的需求清单进行 MVP 范围评审。

## 1. 实验内容

- 灰度线性变换
- `gamma=2.2` 与 `gamma=0.5` 的伽马校正
- NumPy 加法与 `cv2.add` 饱和加法对比
- `cv2.addWeighted` 图像加权混合
- 图像绝对差值
- 暗图、正常图和低对比度图的直方图比较
- 手写 CDF 直方图均衡化
- 手写均衡化与 `cv2.equalizeHist` 对比
- 实验一需求评审与 MVP 范围确定
- OpenCV API 调研

## 2. 实验环境

- Python
- OpenCV 5.0.0
- NumPy 2.5.3
- Matplotlib 3.11.2
- Conda 环境：`opencv`

项目依赖记录在仓库根目录的 `requirements.txt` 中。

## 3. 目录结构

```text
lab_02
├─ data
│  ├─ photo01.jpg
│  └─ photo02.jpg
├─ docs
│  ├─ api_notes.md
│  ├─ mvp_review.md
│  └─ report.md
├─ evidence
├─ results
│  ├─ arithmetic
│  ├─ equalization
│  ├─ histogram
│  └─ transform
├─ src
│  ├─ arith.py
│  ├─ hist_equalize.py
│  └─ transform.py
└─ README.md
```

其中：

- `data`：保存两张原始实验图片。
- `src`：保存 Python 源代码。
- `results`：按实验任务分类保存处理结果。
- `docs`：保存实验报告、MVP 评审和 API 调研。
- `evidence`：保存终端运行截图等实验过程证据。

## 4. 运行方法

以下命令均在仓库根目录 `C:\develop\Python\Labs` 中运行。

首先激活 OpenCV 环境：

```powershell
conda activate opencv
```

### 4.1 灰度变换

```powershell
python lab_02\src\transform.py
```

结果保存在：

```text
lab_02\results\transform
```

### 4.2 图像代数运算

```powershell
python lab_02\src\arith.py
```

结果保存在：

```text
lab_02\results\arithmetic
```

### 4.3 直方图统计与均衡化

```powershell
python lab_02\src\hist_equalize.py
```

直方图结果保存在：

```text
lab_02\results\histogram
```

均衡化结果保存在：

```text
lab_02\results\equalization
```

## 5. 主要实验结果

### 5.1 灰度变换

- 线性变换提高了亮度和对比度，但部分高亮区域出现饱和。
- 按照本实验公式，`gamma=2.2` 提亮暗部，`gamma=0.5` 压暗图像。

### 5.2 代数运算

NumPy 加法与 `cv2.add` 不同的通道值占比为 `22.66%`。

NumPy 的 `uint8` 加法发生模 256 回绕，亮区出现异常颜色；`cv2.add` 使用饱和运算，将超过 255 的结果截断为 255。

### 5.3 直方图

- 暗图的像素更多分布在低灰度区域。
- 正常图的灰度分布范围较宽。
- 低对比度图的灰度值集中在较窄范围。

### 5.4 直方图均衡化

均衡化扩大了图像的灰度分布范围，提高了整体对比度。手写 CDF 均衡化结果与 `cv2.equalizeHist` 保存结果逐像素一致。

## 6. 实验文档

- [实验报告](docs/report.md)
- [需求评审与 MVP 范围](docs/mvp_review.md)
- [OpenCV API 调研](docs/api_notes.md)

课堂小组互评后，还需要在 `mvp_review.md` 中补充至少三条真实评审意见。

## 7. 原始数据说明

`data` 中的照片只作为实验输入，程序生成的结果统一保存在 `results` 中，不覆盖原始图片。
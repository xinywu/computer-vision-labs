# 实验三：空间滤波与图像增强

## 1. 实验内容

本实验使用 OpenCV 完成以下任务：

1. 为原图添加高斯噪声和椒盐噪声。
2. 使用均值滤波、高斯滤波和中值滤波处理两类噪声。
3. 使用拉普拉斯和 USM 方法进行图像锐化。
4. 使用 PSNR 和 SSIM 定量评价滤波结果。
5. 绘制 SFM 系统数据流图。
6. 定义统一的预处理模块接口。

## 2. 实验环境

- Windows
- Python 3.12.14
- OpenCV 5.0.0
- NumPy 2.5.3
- scikit-image 0.26.0
- Conda 环境：`opencv`

## 3. 目录结构

```text
lab_03/
├── data/
│   └── photo01.jpg
├── docs/
│   ├── architecture.md
│   ├── interface_agreement.md
│   └── report.md
├── evidence/
├── results/
│   ├── gaussian_noise.jpg
│   ├── salt_pepper.jpg
│   ├── blur.jpg
│   ├── gauss.jpg
│   ├── median.jpg
│   ├── sp_blur.jpg
│   ├── sp_gauss.jpg
│   ├── sp_median.jpg
│   ├── sharp_laplacian.jpg
│   ├── sharp_usm.jpg
│   ├── gaussian_comparison.jpg
│   ├── salt_pepper_comparison.jpg
│   ├── sharpen_comparison.jpg
│   ├── preprocessed_bgr.jpg
│   └── metrics.csv
├── src/
│   ├── preprocess.py
│   └── spatial_filtering.py
└── README.md
```

## 4. 运行方法

首先进入统一实验仓库：

```powershell
cd C:\develop\Python\Labs
```

激活 Conda 环境：

```powershell
conda activate opencv
```

运行实验三程序：

```powershell
python lab_03\src\spatial_filtering.py
```

程序会自动生成噪声图、滤波结果、锐化结果、对比图和质量评分表。

## 5. 主要参数

| 处理项目 | 参数 |
| --- | --- |
| 高斯噪声 | 均值 0，标准差 25 |
| 椒盐噪声 | 5% 黑点，5% 白点 |
| 均值滤波 | 5 × 5 核 |
| 高斯滤波 | σ = 1.5 |
| 中值滤波 | 核大小为 5 |
| 拉普拉斯锐化 | 增强系数 0.8 |
| USM 锐化 | 模糊 σ = 2.0，增强强度 0.6 |
| 随机数种子 | 0 |

## 6. 实验结果

高斯噪声实验中，高斯滤波取得最高的评价结果：

```text
PSNR：23.63 dB
SSIM：0.7287
```

椒盐噪声实验中，中值滤波取得最高的评价结果：

```text
PSNR：23.90 dB
SSIM：0.7976
```

实验结果说明：

- 高斯滤波更适合处理高斯噪声。
- 中值滤波更适合处理椒盐噪声。
- USM 锐化的整体效果比直接拉普拉斯锐化更自然。
- 去噪强度与边缘保留之间需要进行权衡。

## 7. 软件工程文档

- `docs/architecture.md`：SFM 系统数据流图和预处理模块边界。
- `docs/interface_agreement.md`：预处理函数签名、数据格式和异常约定。
- `docs/report.md`：完整实验报告和结果分析。

统一预处理接口为：

```python
def preprocess(
    img_bgr: np.ndarray,
    cfg: dict,
) -> np.ndarray:
```

接口输入和输出均为 `uint8 BGR` 图像，输出尺寸与输入保持一致。
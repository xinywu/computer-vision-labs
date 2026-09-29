# 实验四 边缘检测与图像分割

## 1 实验内容

本实验使用 OpenCV 完成以下任务：

1. 使用 Sobel 算子计算图像梯度幅值。
2. 比较大小为 3 和 5 的 Sobel 卷积核。
3. 使用三组双阈值进行 Canny 边缘检测。
4. 比较固定阈值和 Otsu 自动阈值分割。
5. 比较全局 Otsu 和自适应阈值在光照不均图像上的效果。
6. 完成详细设计、编码规范和设计走查记录。

## 2 目录结构

    lab_04
    ├─ data
    │  ├─ photo01.jpg
    │  └─ photo02.jpg
    ├─ docs
    │  ├─ coding_standards.md
    │  └─ detailed_design.md
    ├─ evidence
    ├─ results
    ├─ src
    │  └─ edge_segmentation.py
    └─ README.md

## 3 实验图片

`photo01.jpg` 是纹理和轮廓较清晰的建筑图片，用于 Sobel、Canny、固定阈值和 Otsu 实验。

`photo02.jpg` 是左右明暗差异明显的地铁站图片，用于比较全局 Otsu 和自适应阈值。

## 4 运行方法

在 Labs 仓库根目录运行：

    python lab_04\src\edge_segmentation.py

程序会自动读取 `data` 文件夹中的图片，并把处理结果保存到 `results` 文件夹。

## 5 实验结果

### 5.1 Sobel 梯度

程序分别使用大小为 3 和 5 的 Sobel 卷积核。

输出文件：

- `sobel_k3.jpg`
- `sobel_k5.jpg`
- `sobel_comparison.jpg`

大小为 3 的卷积核保留的局部细节较多；大小为 5 的卷积核计算范围更大，得到的主要边缘更加明显，但边缘也稍粗。

### 5.2 Canny 边缘检测

程序使用以下三组双阈值：

| 低阈值 | 高阈值 | 边缘密度 |
|---:|---:|---:|
| 50 | 150 | 19.06% |
| 100 | 200 | 17.65% |
| 150 | 250 | 16.06% |

输出文件：

- `canny_50_150.jpg`
- `canny_100_200.jpg`
- `canny_150_250.jpg`
- `canny_comparison.jpg`

随着阈值升高，检测出的边缘逐渐减少。`(50,150)` 保留的细节最多，但弱纹理也较多；`(150,250)` 的结果更加简洁，但会丢失一部分较弱边缘；`(100,200)` 在细节和简洁程度之间较为均衡。

### 5.3 固定阈值与 Otsu

固定阈值设置为 128，Otsu 自动计算出的阈值为 142。

输出文件：

- `threshold_fixed_128.jpg`
- `threshold_otsu.jpg`
- `threshold_comparison.jpg`

两种方法都能将图像划分为黑白区域。Otsu 根据当前图像的灰度分布自动选择阈值，不需要手工指定，但其效果仍取决于图像的灰度直方图是否接近双峰分布。

### 5.4 自适应阈值

光照不均图片的 Otsu 自动阈值为 89。

输出文件：

- `uneven_otsu.jpg`
- `uneven_adaptive.jpg`
- `adaptive_comparison.jpg`

全局 Otsu 对整张图使用同一个阈值，使较暗的左侧区域大量变黑，部分轨道和墙面细节丢失。自适应阈值根据局部区域的亮度计算阈值，因此能保留明暗区域中的更多结构。

## 6 文档说明

- `docs/detailed_design.md`：记录各函数的输入、输出、算法和异常处理。
- `docs/coding_standards.md`：记录编码规范和设计走查意见。

## 7 主要结论

1. Sobel 梯度幅值较大的位置通常对应明显边缘。
2. Sobel 卷积核越大，结果越平滑，但边缘可能变粗。
3. Canny 双阈值越高，保留的边缘越少。
4. Otsu 能根据灰度分布自动选择全局阈值。
5. 自适应阈值更适合处理局部亮度差异明显的图像。
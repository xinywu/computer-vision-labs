# OpenCV API 调研记录

## 1. cv2.calcHist

函数签名：

```python
cv2.calcHist(
    images,
    channels,
    mask,
    histSize,
    ranges[, hist[, accumulate]]
) -> hist
```

关键参数：

- `images`：输入图像列表，例如 `[gray]`。
- `channels`：需要统计的通道编号。灰度图只有一个通道，因此使用 `[0]`。
- `mask`：可选掩膜。设为 `None` 表示统计整张图像。
- `histSize`：直方图的区间数量。灰度图通常使用 `[256]`。
- `ranges`：统计范围。`[0, 256]` 表示统计灰度值 0 至 255。
- `hist`：可选的输出直方图。
- `accumulate`：是否在已有直方图上累加，默认值为 `False`。
- 返回值 `hist`：统计得到的直方图。单通道灰度图通常返回形状为 `(256, 1)` 的数组。

本实验中的用法：

```python
hist = cv2.calcHist(
    [image],
    [0],
    None,
    [256],
    [0, 256]
)
```

本实验使用该函数统计灰度图中每个灰度值对应的像素数量。

官方文档：

https://docs.opencv.org/4.13.0/d6/dc7/group__imgproc__hist.html

## 2. cv2.equalizeHist

函数签名：

```python
cv2.equalizeHist(src[, dst]) -> dst
```

关键参数：

- `src`：输入图像，必须是 8 位单通道图像，即常见的 `uint8` 灰度图。
- `dst`：可选的输出图像，尺寸和数据类型与输入图像相同。
- 返回值 `dst`：完成直方图均衡化后的灰度图像。

本实验中的用法：

```python
equalized = cv2.equalizeHist(gray)
```

该函数根据输入图像的累计灰度分布建立映射，用于扩大灰度范围并增强整体对比度。彩色图像需要先转换为灰度图，再调用该函数。

官方文档：

https://docs.opencv.org/4.13.0/d6/dc7/group__imgproc__hist.html

## 3. cv2.addWeighted

函数签名：

```python
cv2.addWeighted(
    src1,
    alpha,
    src2,
    beta,
    gamma[, dst[, dtype]]
) -> dst
```

计算公式：

```text
dst = saturate(src1 × alpha + src2 × beta + gamma)
```

关键参数：

- `src1`：第一张输入图像。
- `alpha`：第一张图像的权重。
- `src2`：第二张输入图像，应与第一张图像具有相同尺寸和通道数。
- `beta`：第二张图像的权重。
- `gamma`：加权相加后统一增加的亮度偏移量。
- `dst`：可选的输出图像。
- `dtype`：可选的输出数据深度。默认值 `-1` 表示沿用输入图像的数据深度。
- 返回值 `dst`：加权混合后的图像。

公式中的 `saturate` 表示饱和截断。对于 `uint8` 图像，小于 0 的结果截断为 0，大于 255 的结果截断为 255。

本实验中的用法：

```python
blend = cv2.addWeighted(
    image1,
    0.6,
    image2,
    0.4,
    0
)
```

这表示输出图像由第一张图像的 60% 和第二张图像的 40% 混合而成，不额外增加亮度偏移。

官方文档：

https://docs.opencv.org/4.13.0/d2/de8/group__core__array.html

## 4. 调研结论

- `cv2.calcHist` 用于统计图像的灰度分布。
- `cv2.equalizeHist` 使用累计分布映射增强灰度图的整体对比度。
- `cv2.addWeighted` 根据指定权重混合两张尺寸和通道数相同的图像。
- 本实验使用的三个函数均来自 OpenCV 官方 API，并已在实验代码中实际调用。
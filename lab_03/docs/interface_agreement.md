# 预处理模块接口约定

## 1. 接口目的

预处理模块位于图像读入与特征提取之间，用于根据配置完成图像去噪和锐化，并向后续模块提供格式统一的图像。

## 2. 统一函数签名

```python
def preprocess(
    img_bgr: np.ndarray,
    cfg: dict,
) -> np.ndarray:
    """根据配置对 BGR 图像进行去噪和锐化。"""
```

## 3. 输入约定

### `img_bgr`

- 类型：`numpy.ndarray`。
- 数据类型：`uint8`。
- 形状：`(height, width, 3)`。
- 通道顺序：OpenCV 使用的 BGR 顺序。
- 取值范围：`0～255`。
- 输入图像不能为空。

### `cfg`

`cfg` 为配置字典，支持以下字段：

| 字段 | 类型 | 可选值或范围 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `denoise` | `str` | `none`、`mean`、`gaussian`、`median` | `none` | 去噪方法 |
| `kernel_size` | `int` | 大于等于 3 的奇数 | `5` | 滤波核大小 |
| `sigma` | `float` | 大于 0 | `1.5` | 高斯滤波标准差 |
| `sharpen` | `str` | `none`、`laplacian`、`usm` | `none` | 锐化方法 |
| `laplacian_strength` | `float` | 大于等于 0 | `0.8` | 拉普拉斯增强系数 |
| `usm_sigma` | `float` | 大于 0 | `2.0` | USM 模糊阶段的标准差 |
| `usm_amount` | `float` | 大于等于 0 | `0.6` | USM 增强强度 |

未提供的字段使用默认值。无法识别的去噪或锐化方法视为配置错误。

## 4. 处理顺序

1. 检查输入图像的类型、数据类型和通道数。
2. 根据 `denoise` 执行去噪。
3. 根据 `sharpen` 对去噪结果执行锐化。
4. 将像素值限制在 `0～255`。
5. 返回与输入尺寸相同的 `uint8 BGR` 图像。

去噪先于锐化，避免锐化过程放大原图中的噪声。

## 5. 输出约定

- 返回类型：`numpy.ndarray`。
- 数据类型：`uint8`。
- 形状：与输入图像相同。
- 通道顺序：BGR。
- 函数不修改调用方传入的原始图像。

## 6. 异常约定

| 异常类型 | 触发条件 |
| --- | --- |
| `TypeError` | 输入不是 `numpy.ndarray`，或配置不是 `dict` |
| `ValueError` | 图像为空、不是 `uint8 BGR`、核大小不是有效奇数，或配置值不受支持 |

异常信息应明确指出出错字段和原因，便于调用模块定位问题。

## 7. 调用示例

```python
config = {
    "denoise": "gaussian",
    "kernel_size": 5,
    "sigma": 1.5,
    "sharpen": "usm",
    "usm_sigma": 2.0,
    "usm_amount": 0.6,
}

processed_bgr = preprocess(img_bgr, config)
```

此配置先进行高斯去噪，再进行 USM 锐化。输出图像可直接传给特征提取模块。

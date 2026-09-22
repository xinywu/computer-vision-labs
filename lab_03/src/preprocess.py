"""SFM 系统的图像预处理接口。"""

import cv2
import numpy as np


def preprocess(
    img_bgr: np.ndarray,
    cfg: dict,
) -> np.ndarray:
    """
    根据配置对 BGR 图像依次进行去噪和锐化。

    参数：
        img_bgr:
            输入的 uint8 BGR 图像，形状为
            (height, width, 3)。

        cfg:
            预处理配置字典，用于指定去噪方法、
            锐化方法及相关参数。

    返回：
        处理后的 uint8 BGR 图像。
        输出尺寸和通道数与输入图像保持一致。
    """

    # ==================== 1. 输入检查 ====================

    # 输入图像必须是 NumPy 数组
    if not isinstance(img_bgr, np.ndarray):
        raise TypeError("img_bgr 必须是 numpy.ndarray")

    # 空数组不能进行 OpenCV 图像处理
    if img_bgr.size == 0:
        raise ValueError("img_bgr 不能为空")

    # BGR 图像应具有“高度、宽度、3 个通道”
    if img_bgr.ndim != 3 or img_bgr.shape[2] != 3:
        raise ValueError(
            "img_bgr 必须是形状为 "
            "(height, width, 3) 的 BGR 图像"
        )

    # 统一要求使用 OpenCV 常用的 uint8 图像
    if img_bgr.dtype != np.uint8:
        raise ValueError(
            "img_bgr 的数据类型必须是 uint8"
        )

    # 配置必须使用字典
    if not isinstance(cfg, dict):
        raise TypeError("cfg 必须是 dict")

    # 复制输入图像，避免修改调用方传入的原图
    result = img_bgr.copy()

    # ==================== 2. 去噪处理 ====================

    # 未提供 denoise 时，默认不进行去噪
    denoise_method = cfg.get("denoise", "none")

    # 只有启用去噪时才读取并检查滤波核大小
    if denoise_method != "none":
        kernel_size = cfg.get("kernel_size", 5)

        # 均值、高斯和中值滤波使用奇数大小的滤波核
        if (
            not isinstance(kernel_size, int)
            or isinstance(kernel_size, bool)
            or kernel_size < 3
            or kernel_size % 2 == 0
        ):
            raise ValueError(
                "kernel_size 必须是大于等于 3 的奇数"
            )

        # 均值滤波：
        # 使用邻域像素的平均值替换中心像素
        if denoise_method == "mean":
            result = cv2.blur(
                result,
                (kernel_size, kernel_size),
            )

        # 高斯滤波：
        # 距离中心越近的像素具有越大的权重
        elif denoise_method == "gaussian":
            sigma = cfg.get("sigma", 1.5)

            if (
                not isinstance(sigma, (int, float))
                or isinstance(sigma, bool)
                or sigma <= 0
            ):
                raise ValueError(
                    "sigma 必须是大于 0 的数值"
                )

            result = cv2.GaussianBlur(
                result,
                (kernel_size, kernel_size),
                sigma,
            )

        # 中值滤波：
        # 使用邻域中值替换中心像素，
        # 特别适合处理椒盐噪声
        elif denoise_method == "median":
            result = cv2.medianBlur(
                result,
                kernel_size,
            )

        # 出现未知方法时主动报错
        else:
            raise ValueError(
                f"不支持的去噪方法：{denoise_method}"
            )

    # ==================== 3. 锐化处理 ====================

    # 未提供 sharpen 时，默认不进行锐化
    sharpen_method = cfg.get("sharpen", "none")

    # 拉普拉斯锐化：
    # 提取二阶导数信息并从原图中减去，
    # 从而突出灰度变化明显的边缘
    if sharpen_method == "laplacian":
        strength = cfg.get(
            "laplacian_strength",
            0.8,
        )

        if (
            not isinstance(strength, (int, float))
            or isinstance(strength, bool)
            or strength < 0
        ):
            raise ValueError(
                "laplacian_strength "
                "必须是大于等于 0 的数值"
            )

        # 使用浮点型保存拉普拉斯结果，
        # 避免负梯度被 uint8 截断
        laplacian = cv2.Laplacian(
            result,
            cv2.CV_64F,
        )

        # 增强后限制到 0～255，
        # 再转换回 uint8
        result = np.clip(
            result.astype(np.float64)
            - strength * laplacian,
            0,
            255,
        ).astype(np.uint8)

    # USM 锐化：
    # 先生成模糊图，再放大原图与模糊图的差异
    elif sharpen_method == "usm":
        usm_sigma = cfg.get(
            "usm_sigma",
            2.0,
        )
        usm_amount = cfg.get(
            "usm_amount",
            0.6,
        )

        if (
            not isinstance(usm_sigma, (int, float))
            or isinstance(usm_sigma, bool)
            or usm_sigma <= 0
        ):
            raise ValueError(
                "usm_sigma 必须是大于 0 的数值"
            )

        if (
            not isinstance(usm_amount, (int, float))
            or isinstance(usm_amount, bool)
            or usm_amount < 0
        ):
            raise ValueError(
                "usm_amount 必须是大于等于 0 的数值"
            )

        # 使用高斯滤波得到 USM 所需的模糊图
        blurred = cv2.GaussianBlur(
            result,
            (0, 0),
            usm_sigma,
        )

        # 等价于：
        # result + amount × (result - blurred)
        result = cv2.addWeighted(
            result,
            1.0 + usm_amount,
            blurred,
            -usm_amount,
            0,
        )

    # none 表示不进行锐化
    elif sharpen_method == "none":
        pass

    # 出现未知方法时主动报错
    else:
        raise ValueError(
            f"不支持的锐化方法：{sharpen_method}"
        )

    # ==================== 4. 输出检查 ====================

    # 正常情况下 OpenCV 已返回 uint8，
    # 这里再次转换以保证接口输出类型统一
    result = np.clip(
        result,
        0,
        255,
    ).astype(np.uint8)

    return result
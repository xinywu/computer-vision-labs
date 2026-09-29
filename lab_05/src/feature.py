"""实验五的角点检测与尺度空间函数。"""

from __future__ import annotations

import cv2
import numpy as np


def _as_gray_uint8(image: np.ndarray) -> np.ndarray:
    """校验图像并转换为 Harris 可处理的灰度 uint8 图像。"""
    if not isinstance(image, np.ndarray):
        raise TypeError("image 必须是 numpy.ndarray")
    if image.size == 0:
        raise ValueError("image 不能为空")

    if image.ndim == 2:
        gray = image
    elif image.ndim == 3 and image.shape[2] in (3, 4):
        code = cv2.COLOR_BGR2GRAY if image.shape[2] == 3 else cv2.COLOR_BGRA2GRAY
        gray = cv2.cvtColor(image, code)
    else:
        raise ValueError("image 必须是灰度图、BGR 图或 BGRA 图")

    if gray.dtype == np.uint8:
        return gray
    if not np.issubdtype(gray.dtype, np.number):
        raise TypeError("image 必须包含数值像素")
    if not np.isfinite(gray).all():
        raise ValueError("image 不能包含 NaN 或无穷值")
    if np.issubdtype(gray.dtype, np.floating) and gray.max(initial=0) <= 1.0:
        gray = gray * 255.0
    return np.clip(gray, 0, 255).astype(np.uint8)


def harris_response(
    image: np.ndarray, block_size: int = 2, ksize: int = 3, k: float = 0.04
) -> np.ndarray:
    """返回 Harris 浮点响应图。"""
    gray = _as_gray_uint8(image)
    if block_size < 2:
        raise ValueError("block_size 必须不小于 2")
    if ksize < 3 or ksize % 2 == 0:
        raise ValueError("ksize 必须是大于等于 3 的奇数")
    if not 0 < k < 0.25:
        raise ValueError("k 必须位于 (0, 0.25) 区间")
    return cv2.cornerHarris(np.float32(gray), block_size, ksize, k)


def harris_corners(
    image: np.ndarray,
    *,
    k: float = 0.04,
    threshold_ratio: float = 0.01,
    min_distance: int = 6,
) -> np.ndarray:
    """检测 Harris 局部极大值，返回形状为 (N, 2) 的整数 (x, y) 坐标。"""
    if not 0 < threshold_ratio <= 1:
        raise ValueError("threshold_ratio 必须位于 (0, 1] 区间")
    if min_distance < 1:
        raise ValueError("min_distance 必须不小于 1")

    gray = _as_gray_uint8(image)
    response = harris_response(gray, k=k)
    maximum = float(response.max(initial=0.0))
    if maximum <= 0:
        return np.empty((0, 2), dtype=np.int32)

    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=0,
        qualityLevel=threshold_ratio,
        minDistance=float(min_distance),
        blockSize=2,
        useHarrisDetector=True,
        k=k,
    )
    if corners is None:
        return np.empty((0, 2), dtype=np.int32)
    points = np.rint(corners.reshape(-1, 2)).astype(np.int32)
    height, width = response.shape
    points[:, 0] = np.clip(points[:, 0], 0, width - 1)
    points[:, 1] = np.clip(points[:, 1], 0, height - 1)
    return points


def shi_tomasi_corners(
    image: np.ndarray,
    max_corners: int = 100,
    quality_level: float = 0.01,
    min_distance: float = 10.0,
) -> np.ndarray:
    """返回 Shi-Tomasi 整数角点坐标。"""
    gray = _as_gray_uint8(image)
    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=max_corners,
        qualityLevel=quality_level,
        minDistance=min_distance,
    )
    if corners is None:
        return np.empty((0, 2), dtype=np.int32)
    return np.rint(corners.reshape(-1, 2)).astype(np.int32)


def build_pyramid(image: np.ndarray, levels: int = 4) -> list[np.ndarray]:
    """构造含原图在内的高斯金字塔。"""
    gray = _as_gray_uint8(image)
    if levels < 1:
        raise ValueError("levels 必须不小于 1")
    pyramid = [gray]
    for _ in range(levels - 1):
        if min(pyramid[-1].shape) < 2:
            raise ValueError("图像太小，无法继续降采样")
        pyramid.append(cv2.pyrDown(pyramid[-1]))
    return pyramid


def adjacent_dog(pyramid: list[np.ndarray]) -> list[np.ndarray]:
    """把相邻金字塔层对齐后取绝对差，得到便于观察的 DoG 近似图。"""
    if len(pyramid) < 2:
        raise ValueError("至少需要两层金字塔")
    dogs: list[np.ndarray] = []
    for current, smaller in zip(pyramid, pyramid[1:]):
        enlarged = cv2.resize(smaller, (current.shape[1], current.shape[0]), interpolation=cv2.INTER_LINEAR)
        difference = np.abs(current.astype(np.float32) - enlarged.astype(np.float32))
        dogs.append(cv2.normalize(difference, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))
    return dogs

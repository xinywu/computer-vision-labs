from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
HISTOGRAM_DIR = BASE_DIR / "results" / "histogram"
EQUALIZATION_DIR = BASE_DIR / "results" / "equalization"
HISTOGRAM_DIR.mkdir(parents=True, exist_ok=True)
EQUALIZATION_DIR.mkdir(parents=True, exist_ok=True)


def read_gray(filename):
    path = DATA_DIR / filename
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"无法读取图片：{path}")

    return image


def calc_hist(image):
    """计算灰度图的 256 级直方图。"""
    return cv2.calcHist(
        [image], [0], None, [256], [0, 256]
    ).ravel()


def manual_equalize(image):
    """根据累计分布函数 CDF 手写直方图均衡化。"""
    hist = calc_hist(image)
    cdf = hist.cumsum()

    nonzero_cdf = cdf[cdf > 0]
    if len(nonzero_cdf) == 0:
        return image.copy()

    cdf_min = nonzero_cdf[0]
    denominator = cdf[-1] - cdf_min

    if denominator == 0:
        return image.copy()

    lookup_table = np.rint(
        (cdf - cdf_min) * 255 / denominator
    )
    lookup_table = np.clip(
        lookup_table, 0, 255
    ).astype(np.uint8)

    return lookup_table[image]


dark = read_gray("photo01.jpg")
normal = read_gray("photo02.jpg")

# 人工生成低对比度图，用于观察直方图特征
low_contrast = np.clip(
    normal.astype(np.float32) * 0.35 + 90,
    0,
    255
).astype(np.uint8)

cv2.imwrite(
    str(HISTOGRAM_DIR / "low_contrast.jpg"),
    low_contrast
)

# 比较暗图、正常图和低对比度图的直方图
images = [dark, normal, low_contrast]
titles = ["Dark", "Normal", "Low Contrast"]

fig, axes = plt.subplots(2, 3, figsize=(16, 9))

for column, (image, title) in enumerate(zip(images, titles)):
    axes[0, column].imshow(
        image, cmap="gray", vmin=0, vmax=255
    )
    axes[0, column].set_title(title)
    axes[0, column].axis("off")

    axes[1, column].plot(calc_hist(image), color="black")
    axes[1, column].set_title(f"{title} Histogram")
    axes[1, column].set_xlim(0, 255)
    axes[1, column].set_xlabel("Gray Level")
    axes[1, column].set_ylabel("Pixel Count")

plt.tight_layout()
plt.savefig(
    HISTOGRAM_DIR / "hist_compare.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

# 手写均衡化与 OpenCV 均衡化
dark_manual = manual_equalize(dark)
dark_api = cv2.equalizeHist(dark)
normal_manual = manual_equalize(normal)
normal_api = cv2.equalizeHist(normal)

outputs = {
    "equalized_manual_photo01.jpg": dark_manual,
    "equalized_api_photo01.jpg": dark_api,
    "equalized_manual_photo02.jpg": normal_manual,
    "equalized_api_photo02.jpg": normal_api,
}

for filename, image in outputs.items():
    cv2.imwrite(str(EQUALIZATION_DIR / filename), image)

# 原图、手写均衡化、OpenCV 均衡化对比
rows = [
    ("Photo 01", dark, dark_manual, dark_api),
    ("Photo 02", normal, normal_manual, normal_api),
]

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

for row, (name, original, manual, api) in enumerate(rows):
    items = [
        (original, f"{name} Original"),
        (manual, "Manual Equalization"),
        (api, "cv2.equalizeHist"),
    ]

    for column, (image, title) in enumerate(items):
        axes[row, column].imshow(
            image, cmap="gray", vmin=0, vmax=255
        )
        axes[row, column].set_title(title)
        axes[row, column].axis("off")

plt.tight_layout()
plt.savefig(
    EQUALIZATION_DIR / "equalization_compare.jpg",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

# 展示均衡化前后的图像和直方图
fig, axes = plt.subplots(2, 4, figsize=(18, 9))

for row, (name, original, _, equalized) in enumerate(rows):
    axes[row, 0].imshow(
        original, cmap="gray", vmin=0, vmax=255
    )
    axes[row, 0].set_title(f"{name} Original")
    axes[row, 0].axis("off")

    axes[row, 1].plot(calc_hist(original), color="blue")
    axes[row, 1].set_title("Original Histogram")
    axes[row, 1].set_xlim(0, 255)

    axes[row, 2].imshow(
        equalized, cmap="gray", vmin=0, vmax=255
    )
    axes[row, 2].set_title(f"{name} Equalized")
    axes[row, 2].axis("off")

    axes[row, 3].plot(
        calc_hist(equalized), color="orange"
    )
    axes[row, 3].set_title("Equalized Histogram")
    axes[row, 3].set_xlim(0, 255)

plt.tight_layout()
plt.savefig(
    EQUALIZATION_DIR / "hist_equalization_compare.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

# 统计手写方法与 OpenCV 方法的差异
dark_diff = np.abs(
    dark_manual.astype(np.int16)
    - dark_api.astype(np.int16)
)
normal_diff = np.abs(
    normal_manual.astype(np.int16)
    - normal_api.astype(np.int16)
)

print("直方图统计与均衡化完成")
print(
    "photo01 最大差异：",
    dark_diff.max(),
    "；差异大于 1 的像素占比：",
    f"{np.mean(dark_diff > 1):.4%}"
)
print(
    "photo02 最大差异：",
    normal_diff.max(),
    "；差异大于 1 的像素占比：",
    f"{np.mean(normal_diff > 1):.4%}"
)
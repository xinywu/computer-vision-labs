from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


# 获取实验二目录，保证从不同位置运行程序时都能找到文件
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "photo01.jpg"
RESULTS_DIR = BASE_DIR / "results" / "transform"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 以灰度模式读取偏暗图片
img = cv2.imread(str(INPUT_PATH), cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError(f"无法读取图片：{INPUT_PATH}")

# 线性变换：alpha 控制对比度，beta 控制亮度
alpha = 1.5
beta = 30
linear = np.clip(
    alpha * img.astype(np.float32) + beta,
    0,
    255
).astype(np.uint8)


def gamma_correct(image, gamma):
    """按照实验指导书公式进行伽马校正。"""
    normalized = image.astype(np.float32) / 255.0
    corrected = 255 * (normalized ** (1 / gamma))
    return np.clip(corrected, 0, 255).astype(np.uint8)


gamma_22 = gamma_correct(img, 2.2)
gamma_05 = gamma_correct(img, 0.5)

# 保存单独的处理结果
cv2.imwrite(str(RESULTS_DIR / "linear.jpg"), linear)
cv2.imwrite(str(RESULTS_DIR / "gamma_22.jpg"), gamma_22)
cv2.imwrite(str(RESULTS_DIR / "gamma_05.jpg"), gamma_05)

# 绘制总对比图
images = [img, linear, gamma_22, gamma_05]
titles = [
    "Original",
    "Linear: alpha=1.5, beta=30",
    "Gamma=2.2",
    "Gamma=0.5",
]

fig, axes = plt.subplots(1, 4, figsize=(18, 5))

for axis, image, title in zip(axes, images, titles):
    axis.imshow(image, cmap="gray", vmin=0, vmax=255)
    axis.set_title(title)
    axis.axis("off")

plt.tight_layout()
plt.savefig(
    RESULTS_DIR / "transform_compare.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

print("灰度变换完成")
print(f"结果目录：{RESULTS_DIR}")
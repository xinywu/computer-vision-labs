from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results" / "arithmetic"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

a = cv2.imread(str(DATA_DIR / "photo01.jpg"))
b = cv2.imread(str(DATA_DIR / "photo02.jpg"))

if a is None or b is None:
    raise FileNotFoundError("无法读取 photo01.jpg 或 photo02.jpg")

# cv2 的图像运算要求两张图片尺寸一致
if a.shape != b.shape:
    b = cv2.resize(b, (a.shape[1], a.shape[0]))

# NumPy 的 uint8 加法：超过 255 后按模 256 回绕
add_np = np.add(a, b)

# OpenCV 加法：超过 255 后截断为 255
add_cv = cv2.add(a, b)

# 加权混合：60% 第一张图 + 40% 第二张图
blend = cv2.addWeighted(a, 0.6, b, 0.4, 0)

# 两张图逐像素求绝对差值
difference = cv2.absdiff(a, b)

cv2.imwrite(str(RESULTS_DIR / "add_np.jpg"), add_np)
cv2.imwrite(str(RESULTS_DIR / "add_cv.jpg"), add_cv)
cv2.imwrite(str(RESULTS_DIR / "blend.jpg"), blend)
cv2.imwrite(str(RESULTS_DIR / "difference.jpg"), difference)

# OpenCV 使用 BGR，matplotlib 显示时需要转换成 RGB
images = [a, b, add_np, add_cv, blend, difference]
titles = [
    "Photo 01",
    "Photo 02",
    "NumPy Add",
    "cv2.add",
    "Weighted Blend",
    "Absolute Difference",
]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

for axis, image, title in zip(axes.ravel(), images, titles):
    axis.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axis.set_title(title)
    axis.axis("off")

plt.tight_layout()
plt.savefig(
    RESULTS_DIR / "arith_compare.png",
    dpi=150,
    bbox_inches="tight"
)
plt.close()

different_ratio = np.mean(add_np != add_cv)

print("图像代数运算完成")
print(f"NumPy 加法与 cv2.add 不同的通道值占比：{different_ratio:.2%}")
print(f"结果目录：{RESULTS_DIR}")
import csv
import cv2
import numpy as np

from pathlib import Path
from skimage.metrics import structural_similarity as ssim
from preprocess import preprocess


# ==================== 1. 路径配置与图像读取 ====================

# 获取 lab_03 目录，避免程序依赖终端当前路径
LAB_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = LAB_DIR / "data" / "photo01.jpg"
OUTPUT_DIR = LAB_DIR / "results"

# 如果 results 目录不存在，则自动创建；已存在时不会报错
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 按实验指导书要求，以灰度模式读取图片
img = cv2.imread(str(INPUT_PATH), cv2.IMREAD_GRAYSCALE)

# OpenCV 读取失败时不会自动抛出异常，而是返回 None，
# 因此这里主动检查并给出明确的文件路径
if img is None:
    raise FileNotFoundError(f"无法读取图片：{INPUT_PATH}")

# 输出原图的基本信息，便于确认输入是否符合 uint8 灰度图要求
print("图片读取成功")
print("图片路径：", INPUT_PATH)
print("图片尺寸：", img.shape)
print("数据类型：", img.dtype)


# ==================== 2. 生成两种含噪图像 ====================

# 固定随机种子，使每次实验结果一致
rng = np.random.default_rng(0)

# 添加高斯噪声：均值为 0，标准差为 25
gaussian_noise = rng.normal(0, 25, img.shape)

# 先转成浮点型进行加法，随后把像素值限制到 0～255，
# 最后恢复成 OpenCV 常用的 uint8 类型
gaussian_img = np.clip(
    img.astype(np.float64) + gaussian_noise,
    0,
    255,
).astype(np.uint8)

# 添加椒盐噪声：5% 黑点、5% 白点
salt_pepper_img = img.copy()
mask = rng.random(img.shape)
salt_pepper_img[mask < 0.05] = 0
salt_pepper_img[mask > 0.95] = 255

# 设置两张含噪图像的保存路径
gaussian_path = OUTPUT_DIR / "gaussian_noise.jpg"
salt_pepper_path = OUTPUT_DIR / "salt_pepper.jpg"

# cv2.imwrite 返回布尔值，用它判断图片是否真正保存成功
gaussian_saved = cv2.imwrite(str(gaussian_path), gaussian_img)
salt_pepper_saved = cv2.imwrite(str(salt_pepper_path), salt_pepper_img)

if not gaussian_saved or not salt_pepper_saved:
    raise OSError("噪声图片保存失败")

print("高斯噪声图已保存：", gaussian_path)
print("椒盐噪声图已保存：", salt_pepper_path)


# ==================== 3. 三种空间滤波方法对比 ====================

# 对高斯噪声图进行三种滤波，并统一使用实验指导书规定的参数：
# 均值核为 5×5，高斯标准差为 1.5，中值滤波核大小为 5
mean_filtered = cv2.blur(gaussian_img, (5, 5))
gaussian_filtered = cv2.GaussianBlur(gaussian_img, (0, 0), 1.5)
median_filtered = cv2.medianBlur(gaussian_img, 5)

# 使用“文件名: 图像”的字典，统一保存三种滤波结果
filter_results = {
    "blur.jpg": mean_filtered,
    "gauss.jpg": gaussian_filtered,
    "median.jpg": median_filtered,
}

# 逐张保存高斯噪声的滤波结果，并检查是否写入成功
for filename, result_img in filter_results.items():
    output_path = OUTPUT_DIR / filename

    if not cv2.imwrite(str(output_path), result_img):
        raise OSError(f"图片保存失败：{output_path}")

    print("滤波结果已保存：", output_path)

# 对椒盐噪声图使用相同参数，保证两类噪声的实验条件一致
sp_mean_filtered = cv2.blur(salt_pepper_img, (5, 5))
sp_gaussian_filtered = cv2.GaussianBlur(salt_pepper_img, (0, 0), 1.5)
sp_median_filtered = cv2.medianBlur(salt_pepper_img, 5)

sp_filter_results = {
    "sp_blur.jpg": sp_mean_filtered,
    "sp_gauss.jpg": sp_gaussian_filtered,
    "sp_median.jpg": sp_median_filtered,
}

# 逐张保存椒盐噪声的滤波结果
for filename, result_img in sp_filter_results.items():
    output_path = OUTPUT_DIR / filename

    if not cv2.imwrite(str(output_path), result_img):
        raise OSError(f"图片保存失败：{output_path}")

    print("椒盐噪声滤波结果已保存：", output_path)


# ==================== 4. 拉普拉斯与 USM 锐化 ====================

# 拉普拉斯算子使用 64 位浮点深度，避免负梯度在计算中被截断
laplacian = cv2.Laplacian(img, cv2.CV_64F)

# 从原图中减去 0.8 倍拉普拉斯响应以增强边缘，
# 再将像素限制到 0～255 并转换回 uint8
sharp_laplacian = np.clip(
    img.astype(np.float64) - 0.8 * laplacian,
    0,
    255,
).astype(np.uint8)

# USM 锐化：先进行高斯模糊，再计算“原图×1.6 - 模糊图×0.6”
usm_blurred = cv2.GaussianBlur(img, (0, 0), 2.0)
sharp_usm = cv2.addWeighted(img, 1.6, usm_blurred, -0.6, 0)

# 设置两种锐化结果的输出文件名
sharpen_results = {
    "sharp_laplacian.jpg": sharp_laplacian,
    "sharp_usm.jpg": sharp_usm,
}

# 逐张保存锐化结果
for filename, result_img in sharpen_results.items():
    output_path = OUTPUT_DIR / filename

    if not cv2.imwrite(str(output_path), result_img):
        raise OSError(f"图片保存失败：{output_path}")

    print("锐化结果已保存：", output_path)


# ==================== 5. PSNR 与 SSIM 质量评价 ====================


def calculate_psnr(reference, test):
    """计算两张 uint8 灰度图之间的 PSNR。"""
    # 转成浮点型后相减，避免 uint8 运算产生溢出
    difference = (
        reference.astype(np.float64)
        - test.astype(np.float64)
    )

    # MSE 表示两张图对应像素之间的平均平方误差
    mse = np.mean(difference ** 2)

    # 两张图完全相同时 MSE 为 0，此时 PSNR 为正无穷
    if mse == 0:
        return float("inf")

    # 灰度图最大像素值为 255，按实验指导书公式计算 PSNR
    return 10 * np.log10((255.0 ** 2) / mse)


def calculate_metrics(reference, test):
    """同时计算 PSNR 和 SSIM。"""
    psnr_value = calculate_psnr(reference, test)

    # uint8 灰度图的动态范围为 0～255，因此 data_range 设置为 255
    ssim_value = ssim(reference, test, data_range=255)
    return psnr_value, ssim_value


# 将两类噪声及其三种滤波结果分组，便于统一计算指标
evaluation_groups = {
    "高斯噪声": {
        "含噪图": gaussian_img,
        "均值滤波": mean_filtered,
        "高斯滤波": gaussian_filtered,
        "中值滤波": median_filtered,
    },
    "椒盐噪声": {
        "含噪图": salt_pepper_img,
        "均值滤波": sp_mean_filtered,
        "高斯滤波": sp_gaussian_filtered,
        "中值滤波": sp_median_filtered,
    },
}

# 在终端输出评分表表头
print("\n质量评价结果")
print("-" * 50)
print(f"{'噪声类型':<12}{'处理方法':<12}{'PSNR/dB':>12}{'SSIM':>12}")
print("-" * 50)

# 以无噪声原图 img 为参考，计算每张图的 PSNR 和 SSIM
for noise_name, methods in evaluation_groups.items():
    for method_name, result_img in methods.items():
        psnr_value, ssim_value = calculate_metrics(img, result_img)

        print(
            f"{noise_name:<12}"
            f"{method_name:<12}"
            f"{psnr_value:>12.2f}"
            f"{ssim_value:>12.4f}"
        )

print("-" * 50)


# ==================== 6. 保存质量评价表 ====================

# 使用 CSV 格式保存评分结果，方便用 Excel 打开或插入实验报告
metrics_path = OUTPUT_DIR / "metrics.csv"

# utf-8-sig 可以避免 Windows Excel 打开文件时出现中文乱码
with metrics_path.open(
    "w",
    newline="",
    encoding="utf-8-sig",
) as csv_file:
    writer = csv.writer(csv_file)

    # 写入表头
    writer.writerow(["噪声类型", "处理方法", "PSNR/dB", "SSIM"])

    # 重新计算并逐行写入两类噪声的评价数据
    for noise_name, methods in evaluation_groups.items():
        for method_name, result_img in methods.items():
            psnr_value, ssim_value = calculate_metrics(img, result_img)

            writer.writerow(
                [
                    noise_name,
                    method_name,
                    f"{psnr_value:.2f}",
                    f"{ssim_value:.4f}",
                ]
            )

print("评分表已保存：", metrics_path)


# ==================== 7. 生成滤波效果对比图 ====================


def make_comparison(images, labels):
    """给每张灰度图添加标题，并将它们横向拼接成一张对比图。"""
    panels = []

    # images 和 labels 按相同顺序一一对应
    for panel_img, label in zip(images, labels):
        # 灰度图只有一个通道，先转换成三通道 BGR，
        # 便于添加文字并进行图像拼接
        panel_bgr = cv2.cvtColor(panel_img, cv2.COLOR_GRAY2BGR)

        # 在图片顶部添加 70 像素高的白色区域，用来显示标题
        panel_bgr = cv2.copyMakeBorder(
            panel_bgr,
            70,
            0,
            0,
            0,
            cv2.BORDER_CONSTANT,
            value=(255, 255, 255),
        )

        # 将滤波方法名称写到图片顶部
        # OpenCV 自带字体不支持中文，因此这里使用英文标题
        cv2.putText(
            panel_bgr,
            label,
            (20, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

        panels.append(panel_bgr)

    # 将四张尺寸相同的图片横向拼接
    return cv2.hconcat(panels)


# 四列图片使用统一标题，便于比较不同噪声下的滤波效果
comparison_labels = [
    "Noisy",
    "Mean 5x5",
    "Gaussian",
    "Median 5",
]

# 生成高斯噪声滤波对比图
gaussian_comparison = make_comparison(
    [
        gaussian_img,
        mean_filtered,
        gaussian_filtered,
        median_filtered,
    ],
    comparison_labels,
)

# 生成椒盐噪声滤波对比图
salt_pepper_comparison = make_comparison(
    [
        salt_pepper_img,
        sp_mean_filtered,
        sp_gaussian_filtered,
        sp_median_filtered,
    ],
    comparison_labels,
)

# 规定两张对比图的输出文件名
comparison_results = {
    "gaussian_comparison.jpg": gaussian_comparison,
    "salt_pepper_comparison.jpg": salt_pepper_comparison,
}

# 保存对比图，并检查 cv2.imwrite 是否执行成功
for filename, comparison_img in comparison_results.items():
    output_path = OUTPUT_DIR / filename

    if not cv2.imwrite(str(output_path), comparison_img):
        raise OSError(f"对比图保存失败：{output_path}")

    print("滤波对比图已保存：", output_path)

# ==================== 8. 生成锐化效果对比图 ====================

# 将原图、拉普拉斯锐化和 USM 锐化横向排列，
# 便于观察建筑网格、球体轮廓等边缘细节的变化
sharpen_comparison = make_comparison(
    [
        img,
        sharp_laplacian,
        sharp_usm,
    ],
    [
        "Original",
        "Laplacian",
        "USM",
    ],
)

# 保存锐化对比图，并检查写入是否成功
sharpen_comparison_path = OUTPUT_DIR / "sharpen_comparison.jpg"

if not cv2.imwrite(
    str(sharpen_comparison_path),
    sharpen_comparison,
):
    raise OSError(
        f"锐化对比图保存失败：{sharpen_comparison_path}"
    )

print("锐化对比图已保存：", sharpen_comparison_path)

# ==================== 9. 验证统一预处理接口 ====================

# 接口约定使用 uint8 BGR 图像，
# 因此这里重新以彩色模式读取原图
img_bgr = cv2.imread(
    str(INPUT_PATH),
    cv2.IMREAD_COLOR,
)

# 检查彩色图像是否读取成功
if img_bgr is None:
    raise FileNotFoundError(
        f"无法读取 BGR 图像：{INPUT_PATH}"
    )

# 设置一次完整的接口调用配置：
# 先进行高斯去噪，再进行 USM 锐化
preprocess_config = {
    "denoise": "gaussian",
    "kernel_size": 5,
    "sigma": 1.5,
    "sharpen": "usm",
    "usm_sigma": 2.0,
    "usm_amount": 0.6,
}

# 调用统一预处理接口
processed_bgr = preprocess(
    img_bgr,
    preprocess_config,
)

# 检查输出尺寸是否与输入一致
if processed_bgr.shape != img_bgr.shape:
    raise ValueError(
        "预处理后的图像尺寸与输入图像不一致"
    )

# 检查输出是否保持 uint8 类型
if processed_bgr.dtype != np.uint8:
    raise ValueError(
        "预处理后的图像类型不是 uint8"
    )

# 保存接口调用结果
preprocessed_path = (
    OUTPUT_DIR / "preprocessed_bgr.jpg"
)

if not cv2.imwrite(
    str(preprocessed_path),
    processed_bgr,
):
    raise OSError(
        f"接口结果保存失败：{preprocessed_path}"
    )

print("预处理接口调用成功")
print("接口输入格式：", img_bgr.shape, img_bgr.dtype)
print(
    "接口输出格式：",
    processed_bgr.shape,
    processed_bgr.dtype,
)
print("接口结果已保存：", preprocessed_path)
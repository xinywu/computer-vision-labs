from pathlib import Path

import cv2
import numpy as np


# 获取实验四的目录位置
LAB_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = LAB_DIR / "data"
RESULTS_DIR = LAB_DIR / "results"


def read_gray(filename):
    # 以灰度模式读取图片
    image_path = DATA_DIR / filename
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    # 图片不存在或损坏时报告错误
    if image is None:
        raise FileNotFoundError(f"无法读取图片：{image_path}")

    return image


def save_image(filename, image):
    # 将处理结果保存到 results 文件夹
    output_path = RESULTS_DIR / filename
    success = cv2.imwrite(str(output_path), image)

    if not success:
        raise OSError(f"图片保存失败：{output_path}")

    print(f"已保存：{filename}")


def run_sobel(image):
    # 分别使用 3×3 和 5×5 的 Sobel 卷积核
    magnitude_images = []

    for kernel_size in (3, 5):
        # 计算 x 方向和 y 方向的梯度
        gradient_x = cv2.Sobel(
            image, cv2.CV_64F, 1, 0, ksize=kernel_size
        )
        gradient_y = cv2.Sobel(
            image, cv2.CV_64F, 0, 1, ksize=kernel_size
        )

        # 计算综合梯度幅值
        magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

        # 将结果缩放到 0～255，再转换为 uint8
        magnitude_8u = cv2.normalize(
            magnitude, None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        save_image(f"sobel_k{kernel_size}.jpg", magnitude_8u)
        magnitude_images.append(magnitude_8u)

    # 左边为 ksize=3，右边为 ksize=5
    comparison = cv2.hconcat(magnitude_images)
    save_image("sobel_comparison.jpg", comparison)


def run_canny(image):
    # 实验要求中的三组 Canny 双阈值
    threshold_groups = [
        (50, 150),
        (100, 200),
        (150, 250),
    ]

    edge_images = []

    for low_threshold, high_threshold in threshold_groups:
        edges = cv2.Canny(image, low_threshold, high_threshold)

        filename = f"canny_{low_threshold}_{high_threshold}.jpg"
        save_image(filename, edges)
        edge_images.append(edges)

        # 计算边缘像素在整张图中的占比
        edge_density = np.count_nonzero(edges) / edges.size * 100
        print(
            f"Canny ({low_threshold}, {high_threshold}) "
            f"边缘密度：{edge_density:.2f}%"
        )

    # 从左到右依次对应三组双阈值
    comparison = cv2.hconcat(edge_images)
    save_image("canny_comparison.jpg", comparison)


def run_global_threshold(image):
    # 使用固定阈值 128 进行二值分割
    _, fixed_result = cv2.threshold(
        image, 128, 255, cv2.THRESH_BINARY
    )

    # 使用 Otsu 方法自动选择阈值
    otsu_threshold, otsu_result = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    save_image("threshold_fixed_128.jpg", fixed_result)
    save_image("threshold_otsu.jpg", otsu_result)

    # 左边为固定阈值，右边为 Otsu 阈值
    comparison = cv2.hconcat([fixed_result, otsu_result])
    save_image("threshold_comparison.jpg", comparison)

    print(f"photo01 的 Otsu 自动阈值：{otsu_threshold:.2f}")


def run_adaptive_threshold(image):
    # 先用全局 Otsu 阈值处理光照不均图片
    otsu_threshold, otsu_result = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    # 根据每个像素附近的局部亮度计算阈值
    adaptive_result = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        5,
    )

    save_image("uneven_otsu.jpg", otsu_result)
    save_image("uneven_adaptive.jpg", adaptive_result)

    # 左边为全局 Otsu，右边为自适应阈值
    comparison = cv2.hconcat([otsu_result, adaptive_result])
    save_image("adaptive_comparison.jpg", comparison)

    print(f"photo02 的 Otsu 自动阈值：{otsu_threshold:.2f}")


def main():
    # 如果 results 文件夹不存在就自动创建
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 读取清晰纹理图和光照不均图
    photo01 = read_gray("photo01.jpg")
    photo02 = read_gray("photo02.jpg")

    print("两张图片读取成功")
    print("photo01 尺寸：", photo01.shape)
    print("photo02 尺寸：", photo02.shape)

    print("\n开始 Sobel 梯度实验")
    run_sobel(photo01)

    print("\n开始 Canny 边缘检测实验")
    run_canny(photo01)

    print("\n开始固定阈值与 Otsu 分割实验")
    run_global_threshold(photo01)

    print("\n开始自适应阈值实验")
    run_adaptive_threshold(photo02)

    print("\n实验四的图像处理结果已全部生成")


# 直接运行本文件时才执行 main 函数
if __name__ == "__main__":
    main()
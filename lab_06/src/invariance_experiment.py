from pathlib import Path

import cv2

from features import extract_sift


# 实验文件路径
LAB_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = LAB_DIR / "data" / "input" / "photo01.jpg"
TRANSFORMED_PATH = LAB_DIR / "results" / "rotated_scaled.jpg"
MATCH_PATH = LAB_DIR / "results" / "sift_matches.jpg"
DATA_PATH = LAB_DIR / "results" / "invariance_results.txt"


def rotate_and_scale(img, angle=30, scale=0.6):
    """旋转并缩放图片，同时扩大画布，避免图像内容被裁剪。"""
    height, width = img.shape[:2]
    center = (width / 2, height / 2)

    # 生成旋转和缩放矩阵
    matrix = cv2.getRotationMatrix2D(center, angle, scale)

    # 计算变换后完整图像所需的画布尺寸
    cos_value = abs(matrix[0, 0])
    sin_value = abs(matrix[0, 1])
    new_width = int(height * sin_value + width * cos_value)
    new_height = int(height * cos_value + width * sin_value)

    # 调整平移量，使变换后的图像位于新画布中央
    matrix[0, 2] += new_width / 2 - center[0]
    matrix[1, 2] += new_height / 2 - center[1]

    return cv2.warpAffine(img, matrix, (new_width, new_height))


def main():
    # 读取原图
    img = cv2.imread(str(INPUT_PATH))
    if img is None:
        raise FileNotFoundError(f"无法读取图片：{INPUT_PATH}")

    # 生成旋转30度、缩放0.6倍的实验图像
    transformed = rotate_and_scale(img, angle=30, scale=0.6)
    cv2.imwrite(str(TRANSFORMED_PATH), transformed)

    # 分别提取原图和变换图的 SIFT 特征
    keypoints1, descriptors1 = extract_sift(img)
    keypoints2, descriptors2 = extract_sift(transformed)

    if descriptors1 is None or descriptors2 is None:
        raise RuntimeError("没有检测到足够的 SIFT 描述子")

    # 使用欧氏距离对两幅图的全部描述子进行 KNN 匹配
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    raw_matches = matcher.knnMatch(
        descriptors1,
        descriptors2,
        k=2,
    )

    # Lowe ratio test：只保留明显优于第二候选的匹配
    good_matches = [
        first
        for first, second in raw_matches
        if first.distance < 0.75 * second.distance
    ]

    # 用原图关键点数量作为分母，计算匹配比例
    match_ratio = len(good_matches) / max(len(keypoints1), 1)

    print("原图关键点数:", len(keypoints1))
    print("旋转缩放后关键点数:", len(keypoints2))
    print("通过 ratio test 的匹配数:", len(good_matches))
    print("匹配比例:", round(match_ratio, 3))

    # 只绘制距离最小的前50对，避免匹配线过于密集
    good_matches.sort(key=lambda match: match.distance)
    match_image = cv2.drawMatches(
        img,
        keypoints1,
        transformed,
        keypoints2,
        good_matches[:50],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    cv2.imwrite(str(MATCH_PATH), match_image)

    # 保存实验数据，供实验报告引用
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        file.write(f"原图关键点数: {len(keypoints1)}\n")
        file.write(f"旋转缩放后关键点数: {len(keypoints2)}\n")
        file.write(f"通过 ratio test 的匹配数: {len(good_matches)}\n")
        file.write(f"匹配比例: {match_ratio:.3f}\n")

    print("匹配图:", MATCH_PATH)
    print("实验数据:", DATA_PATH)


if __name__ == "__main__":
    main()
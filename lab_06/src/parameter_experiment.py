import csv
from pathlib import Path

import cv2

from features import extract_sift


# 获取实验六目录，确保从不同工作目录运行时都能正确定位文件
LAB_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = LAB_DIR / "data" / "input" / "photo01.jpg"
OUTPUT_PATH = LAB_DIR / "results" / "parameter_results.csv"


def main():
    # 读取实验原图
    img = cv2.imread(str(INPUT_PATH))
    if img is None:
        raise FileNotFoundError(f"无法读取图片：{INPUT_PATH}")

    # 每次只改变一个主要参数，便于比较参数对关键点数量的影响
    experiments = [
        ("默认参数", {}),
        ("nfeatures=1000", {"nfeatures": 1000}),
        ("nfeatures=3000", {"nfeatures": 3000}),
        ("contrastThreshold=0.01", {"contrastThreshold": 0.01}),
        ("contrastThreshold=0.04", {"contrastThreshold": 0.04}),
        ("contrastThreshold=0.08", {"contrastThreshold": 0.08}),
        ("edgeThreshold=5", {"edgeThreshold": 5}),
        ("edgeThreshold=10", {"edgeThreshold": 10}),
        ("edgeThreshold=20", {"edgeThreshold": 20}),
    ]

    # 保存各组实验的统计结果
    rows = []

    for name, config in experiments:
        # 使用当前参数提取 SIFT 关键点与描述子
        keypoints, descriptors = extract_sift(img, config)

        # 正常情况下描述子形状为“关键点数量 × 128”
        descriptor_shape = (
            None if descriptors is None else descriptors.shape
        )

        print(
            f"{name}: 关键点数={len(keypoints)}, "
            f"描述子形状={descriptor_shape}"
        )

        rows.append([
            name,
            len(keypoints),
            str(descriptor_shape),
        ])

    # 使用 utf-8-sig，方便之后直接用 Excel 打开中文 CSV
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["实验参数", "关键点数量", "描述子形状"])
        writer.writerows(rows)

    print("参数实验表格:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
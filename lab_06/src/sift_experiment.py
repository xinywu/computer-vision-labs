from pathlib import Path

import cv2

from features import extract_sift


LAB_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = LAB_DIR / "data" / "input" / "photo01.jpg"
OUTPUT_PATH = LAB_DIR / "results" / "l6_sift.jpg"


def main():
    img = cv2.imread(str(INPUT_PATH))
    if img is None:
        raise FileNotFoundError(f"无法读取图片：{INPUT_PATH}")

    keypoints, descriptors = extract_sift(img)

    print("关键点数:", len(keypoints))
    print("描述子形状:", descriptors.shape)

    result = cv2.drawKeypoints(
        img,
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )

    cv2.imwrite(str(OUTPUT_PATH), result)
    print("可视化结果:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
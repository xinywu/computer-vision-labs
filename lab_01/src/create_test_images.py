from pathlib import Path

import cv2
import numpy as np


def main():
    input_dir = Path(__file__).resolve().parent.parent / "data" / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    height, width = 480, 640
    x = np.linspace(0, 255, width, dtype=np.uint8)
    y = np.linspace(0, 255, height, dtype=np.uint8)

    blue = np.tile(x, (height, 1))
    green = np.tile(y[:, np.newaxis], (1, width))
    red = np.full((height, width), 160, dtype=np.uint8)
    color = np.dstack((blue, green, red))

    cv2.imwrite(str(input_dir / "color.png"), color)
    cv2.imwrite(str(input_dir / "photo.jpg"), color)

    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(str(input_dir / "gray.png"), gray)

    alpha = np.full((height, width), 180, dtype=np.uint8)
    rgba = np.dstack((color, alpha))
    cv2.imwrite(str(input_dir / "rgba.png"), rgba)

    black = np.zeros((300, 400), dtype=np.uint8)
    white = np.full((300, 400), 255, dtype=np.uint8)
    cv2.imwrite(str(input_dir / "black.png"), black)
    cv2.imwrite(str(input_dir / "white.png"), white)

    large = np.zeros((1080, 1920, 3), dtype=np.uint8)
    large[:, :, 0] = 80
    large[:, :, 1] = 150
    large[:, :, 2] = 220
    
    cv2.imwrite(str(input_dir / "large.png"), large)

    success, encoded_image = cv2.imencode(".png", color)

    if not success:
        raise OSError("Failed to encode Unicode path test image")

    encoded_image.tofile(
        str(input_dir / "\u4e2d\u6587\u8def\u5f84.png")
    )

    print("测试图像已生成：", input_dir)


if __name__ == "__main__":
    main()
    
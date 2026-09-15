import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(
        description="读取图像、检查属性、转换为灰度图并保存。"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="输入图像路径",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="输出灰度图像路径",
    )
    return parser.parse_args()


def read_image(image_path):
    file_data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(file_data, cv2.IMREAD_UNCHANGED)
    return image


def write_image(image_path, image):
    suffix = image_path.suffix.lower()

    if suffix not in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
        raise ValueError(f"不支持的输出文件格式：{suffix}")

    success, encoded_image = cv2.imencode(suffix, image)

    if not success:
        return False

    encoded_image.tofile(str(image_path))
    return True


def get_channel_count(image):
    if image.ndim == 2:
        return 1

    if image.ndim == 3:
        return image.shape[2]

    return 0


def convert_to_gray(image):
    if image.ndim == 2:
        return image

    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    raise ValueError(f"不支持的图像形状：{image.shape}")


def process_image(input_path, output_path):
    start_time = time.perf_counter()

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"输入文件不存在：{input_path}")

    image = read_image(input_path)

    if image is None:
        raise ValueError(f"读取失败，文件可能不是有效图像：{input_path}")

    channels = get_channel_count(image)

    print("输入路径:", input_path)
    print("输入 shape:", image.shape)
    print("输入 dtype:", image.dtype)
    print("输入通道数:", channels)

    gray = convert_to_gray(image)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not write_image(output_path, gray):
        raise OSError(f"保存失败：{output_path}")

    elapsed_time = time.perf_counter() - start_time

    print("输出路径:", output_path)
    print("输出 shape:", gray.shape)
    print("输出 dtype:", gray.dtype)
    print("输出通道数:", get_channel_count(gray))
    print(f"运行耗时: {elapsed_time:.6f} 秒")
    print("状态: SUCCESS")


def main():
    args = parse_args()

    try:
        process_image(args.input, args.output)
        return 0
    except (FileNotFoundError, ValueError, OSError) as error:
        print("状态: ERROR", file=sys.stderr)
        print(f"错误信息: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print("状态: ERROR", file=sys.stderr)
        print(f"未知错误: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
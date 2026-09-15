import os
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np


LAB_DIR = Path(__file__).resolve().parent.parent
PIPELINE = LAB_DIR / "src" / "baseline_pipeline.py"
INPUT_DIR = LAB_DIR / "data" / "input"
OUTPUT_DIR = LAB_DIR / "data" / "output"
EVIDENCE_DIR = LAB_DIR / "evidence"


TEST_CASES = [
    {
        "id": "T01",
        "name": "标准彩色 PNG",
        "input": INPUT_DIR / "color.png",
        "output": OUTPUT_DIR / "t01_color_gray.png",
        "expected_code": 0,
    },
    {
        "id": "T02",
        "name": "JPEG 图像",
        "input": INPUT_DIR / "photo.jpg",
        "output": OUTPUT_DIR / "t02_photo_gray.png",
        "expected_code": 0,
    },
    {
        "id": "T03",
        "name": "不存在的输入路径",
        "input": INPUT_DIR / "missing.png",
        "output": OUTPUT_DIR / "t03_missing_gray.png",
        "expected_code": 1,
    },
    {
        "id": "T04",
        "name": "灰度 PNG",
        "input": INPUT_DIR / "gray.png",
        "output": OUTPUT_DIR / "t04_gray.png",
        "expected_code": 0,
    },
    {
        "id": "T05",
        "name": "RGBA PNG",
        "input": INPUT_DIR / "rgba.png",
        "output": OUTPUT_DIR / "t05_rgba_gray.png",
        "expected_code": 0,
    },
    {
        "id": "T06",
        "name": "中文路径",
        "input": INPUT_DIR / "\u4e2d\u6587\u8def\u5f84.png",
        "output": OUTPUT_DIR / "\u4e2d\u6587\u8f93\u51fa.png",
        "expected_code": 0,
    },
    {
        "id": "T07",
        "name": "损坏文件",
        "input": INPUT_DIR / "corrupted.png",
        "output": OUTPUT_DIR / "t07_corrupted_gray.png",
        "expected_code": 1,
    },
    {
        "id": "T08",
        "name": "输出目录不存在",
        "input": INPUT_DIR / "color.png",
        "output": OUTPUT_DIR / "auto_created" / "t08_gray.png",
        "expected_code": 0,
    },
    {
        "id": "T09",
        "name": "全黑图像",
        "input": INPUT_DIR / "black.png",
        "output": OUTPUT_DIR / "t09_black_gray.png",
        "expected_code": 0,
    },
    {
        "id": "T10",
        "name": "1920×1080 大图像",
        "input": INPUT_DIR / "large.png",
        "output": OUTPUT_DIR / "t10_large_gray.png",
        "expected_code": 0,
    },
]


def read_image(image_path):
    if not image_path.is_file():
        return None

    file_data = np.fromfile(str(image_path), dtype=np.uint8)
    return cv2.imdecode(file_data, cv2.IMREAD_UNCHANGED)


def run_test(test_case):
    command = [
        sys.executable,
        str(PIPELINE),
        "--input",
        str(test_case["input"]),
        "--output",
        str(test_case["output"]),
    ]

    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
    )

    passed = result.returncode == test_case["expected_code"]

    output_image = None
    if result.returncode == 0:
        output_image = read_image(test_case["output"])
        passed = passed and output_image is not None

    lines = [
        f"{test_case['id']}：{test_case['name']}",
        f"命令：{' '.join(command)}",
        f"预期退出码：{test_case['expected_code']}",
        f"实际退出码：{result.returncode}",
    ]

    if result.stdout.strip():
        lines.append("标准输出：")
        lines.append(result.stdout.strip())

    if result.stderr.strip():
        lines.append("错误输出：")
        lines.append(result.stderr.strip())

    if output_image is not None:
        lines.append(f"验证输出 shape：{output_image.shape}")
        lines.append(f"验证输出 dtype：{output_image.dtype}")
        lines.append(
            f"验证像素范围：{output_image.min()} 至 {output_image.max()}"
        )

    lines.append(f"测试结论：{'PASS' if passed else 'FAIL'}")
    lines.append("=" * 60)

    return passed, "\n".join(lines)


def main():
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    auto_created_dir = OUTPUT_DIR / "auto_created"
    if auto_created_dir.exists():
        shutil.rmtree(auto_created_dir)

    all_passed = True
    reports = []

    for test_case in TEST_CASES:
        passed, report = run_test(test_case)
        all_passed = all_passed and passed
        reports.append(report)
        print(
            f"{test_case['id']} "
            f"{'PASS' if passed else 'FAIL'}："
            f"{test_case['name']}"
        )

    summary = [
        "",
        f"测试总数：{len(TEST_CASES)}",
        f"通过数量：{sum('测试结论：PASS' in report for report in reports)}",
        f"总体结论：{'PASS' if all_passed else 'FAIL'}",
        "",
    ]

    evidence_path = EVIDENCE_DIR / "test_results.txt"
    evidence_path.write_text(
        "\n".join(summary + reports),
        encoding="utf-8",
    )

    print(f"测试证据已保存：{evidence_path}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
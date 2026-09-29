"""运行实验五并生成全部图片和文本证据。"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from feature import adjacent_dog, build_pyramid, harris_corners, harris_response, shi_tomasi_corners


LAB_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = LAB_DIR / "data"
RESULTS_DIR = LAB_DIR / "results"
EVIDENCE_DIR = LAB_DIR / "evidence"


def make_chessboard(path: Path, rows: int = 7, cols: int = 10, square: int = 72) -> None:
    """生成无版权依赖、可重复使用的标准黑白棋盘格。"""
    board = np.full((rows * square, cols * square), 255, np.uint8)
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                board[row * square : (row + 1) * square, col * square : (col + 1) * square] = 0
    write_image(path, board)


def write_image(path: Path, image: np.ndarray) -> None:
    """使用 imencode + tofile，兼容 Windows 中文路径。"""
    extension = path.suffix or ".png"
    success, encoded = cv2.imencode(extension, image)
    if not success:
        raise OSError(f"无法编码图片：{path}")
    encoded.tofile(path)


def read_gray(path: Path) -> np.ndarray | None:
    """使用 fromfile + imdecode，兼容 Windows 中文路径。"""
    try:
        encoded = np.fromfile(path, dtype=np.uint8)
    except OSError:
        return None
    return cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)


def draw_points(gray: np.ndarray, points: np.ndarray, color: tuple[int, int, int]) -> np.ndarray:
    output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for x, y in points:
        cv2.circle(output, (int(x), int(y)), 5, color, -1, cv2.LINE_AA)
    return output


def save_image(name: str, image: np.ndarray) -> None:
    path = RESULTS_DIR / name
    write_image(path, image)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)
    EVIDENCE_DIR.mkdir(exist_ok=True)
    chess_path = DATA_DIR / "chess.png"
    if not chess_path.exists():
        make_chessboard(chess_path)

    gray = read_gray(chess_path)
    if gray is None:
        raise FileNotFoundError(f"无法读取图片：{chess_path}")

    lines = [f"输入图片：{chess_path}", f"图片尺寸：{gray.shape[1]} x {gray.shape[0]}"]
    harris_sets: dict[float, np.ndarray] = {}
    for k in (0.04, 0.06, 0.10):
        points = harris_corners(gray, k=k)
        harris_sets[k] = points
        save_image(f"harris_k{k:.2f}.png", draw_points(gray, points, (0, 0, 255)))
        response = harris_response(gray, k=k)
        positive_ratio = float(np.count_nonzero(response > 0.01 * response.max()) / response.size)
        lines.append(
            f"Harris k={k:.2f}：{len(points)} 个局部极大角点，"
            f"最大响应 {float(response.max()):.2e}，强响应像素占比 {positive_ratio:.4%}"
        )

    shi = shi_tomasi_corners(gray, max_corners=100, quality_level=0.01, min_distance=10)
    save_image("shi_tomasi.png", draw_points(gray, shi, (0, 255, 0)))
    lines.append(f"Shi-Tomasi：{len(shi)} 个角点（上限 100）")

    comparison = np.hstack(
        [draw_points(gray, harris_sets[0.04], (0, 0, 255)), draw_points(gray, shi, (0, 255, 0))]
    )
    cv2.putText(comparison, "Harris k=0.04", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    cv2.putText(comparison, "Shi-Tomasi", (gray.shape[1] + 15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    save_image("corner_comparison.png", comparison)

    pyramid = build_pyramid(gray, levels=4)
    for index, level in enumerate(pyramid):
        save_image(f"pyr{index}.png", level)
        lines.append(f"金字塔第 {index} 层：{level.shape[1]} x {level.shape[0]}")

    dogs = adjacent_dog(pyramid)
    for index, dog in enumerate(dogs):
        save_image(f"dog_{index}_{index + 1}.png", dog)
        threshold = float(np.percentile(dog, 99))
        strong = int(np.count_nonzero(dog >= threshold))
        lines.append(f"DoG {index}-{index + 1}：99% 分位阈值 {threshold:.1f}，强响应像素 {strong}")

    log = "\n".join(lines) + "\n"
    (EVIDENCE_DIR / "run_log.txt").write_text(log, encoding="utf-8")
    print(log, end="")


if __name__ == "__main__":
    main()

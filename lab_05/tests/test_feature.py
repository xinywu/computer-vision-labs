from pathlib import Path
import sys

import cv2
import numpy as np
import pytest

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_DIR / "src"))

from feature import build_pyramid, harris_corners  # noqa: E402


def make_chessboard(rows: int = 7, cols: int = 10, square: int = 24) -> np.ndarray:
    board = np.full((rows * square, cols * square), 255, np.uint8)
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                board[row * square : (row + 1) * square, col * square : (col + 1) * square] = 0
    return board


def test_valid_uint8_input_does_not_raise():
    points = harris_corners(np.zeros((20, 20), dtype=np.uint8))
    assert points.shape == (0, 2)


def test_non_array_input_rejected():
    with pytest.raises(TypeError):
        harris_corners([[0, 1], [1, 0]])


def test_empty_image_rejected():
    with pytest.raises(ValueError):
        harris_corners(np.empty((0, 0), dtype=np.uint8))


def test_plain_image_returns_empty():
    points = harris_corners(np.full((50, 50), 128, np.uint8))
    assert len(points) == 0


def test_chessboard_has_corners():
    points = harris_corners(make_chessboard())
    assert len(points) > 10


def test_coordinates_are_integer_and_in_range():
    image = make_chessboard()
    points = harris_corners(image)
    assert np.issubdtype(points.dtype, np.integer)
    assert np.all((0 <= points[:, 0]) & (points[:, 0] < image.shape[1]))
    assert np.all((0 <= points[:, 1]) & (points[:, 1] < image.shape[0]))


def test_color_image_is_supported():
    color = cv2.cvtColor(make_chessboard(), cv2.COLOR_GRAY2BGR)
    assert len(harris_corners(color)) > 10


def test_pyramid_has_four_halving_levels():
    levels = build_pyramid(np.zeros((160, 240), np.uint8), levels=4)
    assert [level.shape for level in levels] == [(160, 240), (80, 120), (40, 60), (20, 30)]

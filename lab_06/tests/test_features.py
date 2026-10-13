import unittest

import cv2
import numpy as np

from lab_06.src.features import extract_sift


class TestExtractSift(unittest.TestCase):
    def setUp(self):
        # 创建带有文字和几何图形的测试图像
        self.image = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.rectangle(self.image, (40, 40), (260, 260), (255, 255, 255), 4)
        cv2.circle(self.image, (150, 150), 60, (255, 255, 255), 4)
        cv2.putText(
            self.image,
            "SIFT",
            (75, 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            3,
        )

    def test_extracts_keypoints(self):
        # 应当能够从有明显纹理的图像中检测到关键点
        keypoints, descriptors = extract_sift(self.image)

        self.assertGreater(len(keypoints), 0)
        self.assertIsNotNone(descriptors)

    def test_descriptor_has_128_dimensions(self):
        # 每个 SIFT 描述子必须具有128个分量
        _, descriptors = extract_sift(self.image)

        self.assertEqual(descriptors.shape[1], 128)
        self.assertEqual(descriptors.dtype, np.float32)

    def test_rejects_empty_image(self):
        # 输入空图像时应主动报告错误
        with self.assertRaises(ValueError):
            extract_sift(None)


if __name__ == "__main__":
    unittest.main()
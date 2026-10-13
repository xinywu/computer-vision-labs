import cv2


def extract_sift(img, cfg=None):
    """提取图像的 SIFT 关键点和描述子。"""
    if img is None:
        raise ValueError("输入图像不能为空")

    cfg = cfg or {}
    sift = cv2.SIFT_create(**cfg)
    keypoints, descriptors = sift.detectAndCompute(img, None)

    return keypoints, descriptors
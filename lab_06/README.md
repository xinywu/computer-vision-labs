# 实验六 SIFT 特征提取与描述

## 实验内容

本实验使用 OpenCV 完成 SIFT 关键点检测、128 维描述子提取、参数对比，以及旋转和尺度不变性验证。

## 环境

- Python 3.12
- OpenCV 5.0.0
- NumPy

## 模块接口

模块位置：`src/features.py`

```python
extract_sift(img, cfg=None) -> (keypoints, descriptors)
```

参数说明：

- `img`：OpenCV 读取的输入图像。
- `cfg`：可选的 SIFT 参数字典，例如 `{"contrastThreshold": 0.04}`。
- `keypoints`：SIFT 关键点列表。
- `descriptors`：形状为 `(N, 128)` 的 `float32` 描述子矩阵。

## 运行方法

在仓库根目录运行：

```powershell
python lab_06\src\sift_experiment.py
python lab_06\src\parameter_experiment.py
python lab_06\src\invariance_experiment.py
python -m unittest discover -s lab_06\tests -v
```

## 主要结果

- 默认参数检测到 29512 个关键点。
- 描述子形状为 `(29512, 128)`。
- 旋转 30° 并缩放至 0.6 倍后检测到 11189 个关键点。
- 6474 个匹配通过 Lowe ratio test。
- 以原图关键点数量为分母，匹配比例为 0.219。
- 3 项自动测试全部通过。

## 输出文件

- `results/l6_sift.jpg`：SIFT 关键点可视化。
- `results/parameter_results.csv`：参数对比数据。
- `results/rotated_scaled.jpg`：旋转和缩放后的图像。
- `results/sift_matches.jpg`：前 50 对优质匹配。
- `results/invariance_results.txt`：不变性验证数据。
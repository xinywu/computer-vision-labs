# 实验五 角点检测与尺度空间

## 1 实验内容

本实验完成 Harris 角点检测、Shi-Tomasi 角点检测、四层图像金字塔、相邻尺度 DoG 近似以及自动化单元测试。

## 2 目录结构

    lab_05
    ├─ data
    │  └─ chess.png
    ├─ docs
    │  └─ report.md
    ├─ evidence
    │  ├─ pytest_log.txt
    │  └─ run_log.txt
    ├─ results
    ├─ src
    │  ├─ feature.py
    │  └─ run_experiment.py
    ├─ tests
    │  └─ test_feature.py
    ├─ README.md
    └─ requirements.txt

## 3 运行方法

在 `Labs` 仓库根目录运行：

    conda run -n opencv python lab_05\src\run_experiment.py
    conda run -n opencv python -m pytest lab_05\tests -v

程序会生成棋盘格输入图、三组 Harris 结果、Shi-Tomasi 对比图、四层金字塔、三幅相邻尺度 DoG 图和运行日志。

## 4 结果说明

- `harris_k0.04.png`、`harris_k0.06.png`、`harris_k0.10.png`：比较 k 值对 Harris 响应的影响。
- `shi_tomasi.png`：前 100 个 Shi-Tomasi 角点。
- `corner_comparison.png`：Harris 与 Shi-Tomasi 并排对比。
- `pyr0.png` 至 `pyr3.png`：尺寸逐层减半的尺度空间。
- `dog_0_1.png` 至 `dog_2_3.png`：相邻尺度对齐后的绝对差分与归一化结果。

具体数值、现象解释和测试结论见 `docs/report.md` 与 `evidence` 目录。

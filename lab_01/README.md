# 实验一 需求分析与 OpenCV 环境基线

本实验实现一个可通过命令行运行的基础图像处理程序。程序读取静态图像，检查图像属性，将图像转换为灰度图并保存，同时处理文件不存在、文件损坏和输出目录不存在等情况。

## 1 实验功能

- 通过命令行参数传入输入和输出路径。
- 输出输入图像的 shape、dtype 和通道数。
- 支持彩色、灰度和 RGBA 图像。
- 将输入图像转换为单通道灰度图。
- 自动创建不存在的输出目录。
- 支持 Windows 中文输入和输出路径。
- 失败时输出明确错误信息并返回非零退出码。
- 记录处理耗时和运行状态。

## 2 环境要求

- Windows 11 64 位
- Python 3.12
- OpenCV
- NumPy
- Matplotlib

本实验实际验证的版本见 `docs/environment.md`。

## 3 安装方法

在仓库根目录 `Labs` 中打开 PowerShell，创建并激活 Conda 环境：

```powershell
conda create -n opencv python=3.12
conda activate opencv
```

安装实验依赖：

```powershell
python -m pip install -r lab_01\requirements.txt
```

检查环境：

```powershell
python lab_01\src\version_check.py
```

如果能够输出 Python、OpenCV、NumPy 和 Matplotlib 版本，说明环境配置成功。

## 4 目录结构

```text
Labs
├── .gitignore
├── README.md
└── lab_01
    ├── README.md
    ├── requirements.txt
    ├── src
    │   ├── baseline_pipeline.py
    │   ├── create_test_images.py
    │   ├── run_tests.py
    │   └── version_check.py
    ├── data
    │   ├── input
    │   └── output
    ├── docs
    │   ├── environment.md
    │   ├── requirements.md
    │   └── test_report.md
    └── evidence
        ├── environment_versions.txt
        └── test_results.txt
```

## 5 运行方法

程序需要使用 `--input` 和 `--output` 参数：

```powershell
python lab_01\src\baseline_pipeline.py --input 输入图片路径 --output 输出图片路径
```

示例：

```powershell
python lab_01\src\baseline_pipeline.py --input lab_01\data\input\color.png --output lab_01\data\output\color_gray.png
```

成功运行后，程序会输出：

- 输入和输出路径
- shape
- dtype
- 通道数
- 运行耗时
- SUCCESS 状态

## 6 生成测试数据

运行以下命令生成本实验使用的测试图像：

```powershell
python lab_01\src\create_test_images.py
```

生成的数据包括彩色 PNG、JPEG、灰度 PNG、RGBA PNG、全黑图像、全白图像、大尺寸图像、中文路径图像和损坏文件。

其中 `corrupted.png` 是故意生成的无效文件，用于验证程序的异常处理能力。

## 7 执行测试

运行：

```powershell
python lab_01\src\run_tests.py
```

测试程序将自动执行 T01 至 T10，并将详细结果写入：

```text
lab_01\evidence\test_results.txt
```

测试内容包括：

- 标准彩色 PNG
- JPEG 图像
- 不存在的输入路径
- 灰度 PNG
- RGBA PNG
- 中文路径
- 损坏文件
- 不存在的输出目录
- 全黑图像
- 1920×1080 大图像

## 8 输入输出约定

- 原始输入保存在 `data/input`，不得被程序覆盖。
- 程序结果保存在 `data/output`。
- 彩色图像通常表示为 `(H, W, 3)`。
- 灰度图像通常表示为 `(H, W)`。
- OpenCV 彩色图像默认采用 BGR 通道顺序。
- Matplotlib 显示彩色图像时通常采用 RGB 通道顺序。
- 像素通过 `image[y, x]` 访问。
- 常见 `uint8` 图像的像素范围为 0 至 255。

## 9 退出状态

- 处理成功：退出码为 `0`，输出 `状态: SUCCESS`。
- 处理失败：退出码为非零值，输出 `状态: ERROR` 和具体错误信息。

可在 PowerShell 中使用以下命令查看上一条 Python 命令的退出码：

```powershell
$LASTEXITCODE
```

## 10 实验文档

- `docs/requirements.md`：功能需求、非功能需求、异常需求、用例和验收标准。
- `docs/environment.md`：操作系统、软件版本和环境问题记录。
- `docs/test_report.md`：测试过程、实际结果、问题分析和结论。
- `evidence/test_results.txt`：自动测试产生的原始运行证据。
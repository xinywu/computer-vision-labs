import platform
import sys

import cv2
import matplotlib
import numpy as np


def main():
    print("操作系统:", platform.platform())
    print("Python:", sys.version)
    print("OpenCV:", cv2.__version__)
    print("NumPy:", np.__version__)
    print("Matplotlib:", matplotlib.__version__)


if __name__ == "__main__":
    main()
"""
File: img_tool.py
Author: Chuncheng Zhang
Date: 2023-11-17
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-11-17 ------------------------
# Requirements and constants
import cv2
import numpy as np
from PIL import Image


# %% ---- 2023-11-17 ------------------------
# Function and class
def pil2mat(img: Image, code=cv2.COLOR_BGR2RGB):
    return cv2.cvtColor(np.array(img, dtype=np.uint8), code)


# %% ---- 2023-11-17 ------------------------
# Play ground


# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

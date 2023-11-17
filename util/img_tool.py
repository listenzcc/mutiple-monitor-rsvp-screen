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


def overlay(background: np.array, foreground: np.array, foreground_map: np.array, x: float, y: float, copy=True):
    if copy:
        background = background.copy()

    w1, h1, _ = background.shape
    w2, h2, _ = foreground.shape

    # Convert (0, 1) to the ratio of width | height
    x = int(x * w1)
    y = int(y * h1)

    x = max(min(x, w1-w2), w2)
    y = max(min(y, h1-h2), h2)

    a = w2 // 2
    b = w2 - a
    c = h2 // 2
    d = h2 - c

    background[x-a:x+b, y-c:y+d][foreground_map] = foreground[foreground_map]

    return background


def draw_trace(background: np.array, trace: list, copy=True):
    if copy:
        background = background.copy()

    w1, h1, _ = background.shape
    w2 = 3
    h2 = 3

    for x, y in trace:
        # Convert (0, 1) to the ratio of width | height
        x = int(x * w1)
        y = int(y * h1)

        x = max(min(x, w1-w2), w2)
        y = max(min(y, h1-h2), h2)

        a = w2 // 2
        b = w2 - a
        c = h2 // 2
        d = h2 - c

        # BGR
        background[x-a:x+b, y-c:y+d] = (0, 255, 255)

    return background


# %% ---- 2023-11-17 ------------------------
# Play ground


# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

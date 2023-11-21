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
    """
    Converts a PIL Image object to a NumPy array using OpenCV color conversion.

    Args:
        img (Image): The PIL Image object to convert.
        code (int, optional): The color conversion code to use. Defaults to cv2.COLOR_BGR2RGB.

    Returns:
        np.array: The NumPy array representation of the image.

    Examples:
        >>> from PIL import Image
        >>> img = Image.open('image.jpg')
        >>> result = pil2mat(img, code=cv2.COLOR_BGR2GRAY)
    """

    if img.mode == 'P':
        img = img.convert('RGB', palette=img.palette)
    return cv2.cvtColor(np.array(img, dtype=np.uint8), code)


def overlay(background: np.array,
            foreground: np.array,
            foreground_map: np.array = None,
            x: float = 0.5,
            y: float = 0.5,
            alpha: float = 0.8,
            copy: bool = True):
    """
    Overlays a foreground image onto a background image at a specified position.

    Args:
        background (np.array): The background image.
        foreground (np.array): The foreground image to overlay.
        foreground_map (np.array, optional): A mask indicating the regions of the foreground image to overlay. Defaults to None.
        x (float, optional): The x-coordinate of the overlay position as a ratio of the background width. Defaults to 0.5.
        y (float, optional): The y-coordinate of the overlay position as a ratio of the background height. Defaults to 0.5.
        alpha (float, optional): The opacity of the overlay. Defaults to 0.8.
        copy (bool, optional): Indicates whether to create a copy of the background image. Defaults to True.

    Returns:
        np.array: The background image with the foreground image overlaid.

    Examples:
        >>> background = np.zeros((100, 100, 3), dtype=np.uint8)
        >>> foreground = np.ones((20, 20, 3), dtype=np.uint8) * 255
        >>> result = overlay(background, foreground, x=0.3, y=0.7, alpha=0.5)
    """

    if copy:
        background = background.copy()

    w1, h1, _ = background.shape
    w2, h2, _ = foreground.shape

    # Convert (0, 1) to the ratio of width | height
    x = int(x * w1)
    y = int(y * h1)

    x = max(min(x, w1-w2), w2)
    y = max(min(y, h1-h2), h2)
    alpha = max(min(alpha, 1), 0)

    a = w2 // 2
    b = w2 - a
    c = h2 // 2
    d = h2 - c

    if foreground_map is not None:
        fg = (foreground[foreground_map] * alpha).astype(np.uint8)
        bg = (background[x-a:x+b, y-c:y+d][foreground_map]
              * (1-alpha)).astype(np.uint8)
        background[x-a:x+b, y-c:y+d][foreground_map] = fg + bg
    else:
        fg = (foreground * alpha).astype(np.uint8)
        bg = (background[x-a:x+b, y-c:y+d] * (1-alpha)).astype(np.uint8)
        background[x-a:x+b, y-c:y+d] = fg + bg

    return background


def draw_trace(background: np.array, trace: list, color: tuple = (0, 0, 255), copy=True):
    """
    Draws a trace on a background image.

    Args:
        background (np.array): The background image on which to draw the trace.
        trace (list): The list of (x, y) coordinates representing the trace.
        color (tuple, optional): The color of the trace in BGR format. Defaults to (0, 0, 255).
        copy (bool, optional): Indicates whether to create a copy of the background image. Defaults to True.

    Returns:
        np.array: The background image with the trace drawn on it.

    Examples:
        >>> background = np.zeros((100, 100, 3), dtype=np.uint8)
        >>> trace = [(0.1, 0.1), (0.5, 0.5), (0.9, 0.9)]
        >>> color = (0, 255, 0)
        >>> result = draw_trace(background, trace, color)
    """

    if not trace:
        return background

    if copy:
        background = background.copy()

    w1, h1, _ = background.shape
    w2 = 3
    h2 = 3

    for obj in trace:
        if isinstance(obj, tuple):
            x, y = obj
        if isinstance(obj, dict):
            x = obj['x']
            y = obj['y']
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
        background[x-a:x+b, y-c:y+d] = color

    return background


# %% ---- 2023-11-17 ------------------------
# Play ground


# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

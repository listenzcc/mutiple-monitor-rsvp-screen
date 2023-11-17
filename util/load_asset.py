"""
File: load_asset.py
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
from . import LOGGER, CONF, singleton
from .img_tool import pil2mat


# %% ---- 2023-11-17 ------------------------
# Function and class
def _read_img(path):
    img = Image.open(path)
    img = img.convert(mode='RGB')
    img = img.resize((int(CONF.width), int(CONF.height)))
    LOGGER.debug(f'Loaded image: {path}')

    return dict(img=img, mat=pil2mat(img))


@singleton
class Asset(object):
    root = CONF.root_path
    folder = CONF.root_path.joinpath('asset')

    def __init__(self):
        self.load_asset()

    def load_asset(self):
        self.image_rsvp_idle = _read_img(self.folder.joinpath('rsvp/idle.png'))
        self.image_rsvp_between_blocks = _read_img(
            self.folder.joinpath('rsvp/between-blocks.png'))


# %% ---- 2023-11-17 ------------------------
# Play ground


# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

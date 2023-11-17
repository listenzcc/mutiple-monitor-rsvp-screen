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

from rich import inspect


# %% ---- 2023-11-17 ------------------------
# Function and class
def _read_img(path, resize=True):
    img = Image.open(path)
    img = img.convert(mode='RGB')

    if resize:
        img = img.resize((int(CONF.width), int(CONF.height)))
        LOGGER.debug(f'Resized the image: {path}')
    else:
        LOGGER.debug(f'Not resized the image: {path}')

    LOGGER.debug(f'Loaded image: {path}')

    return dict(img=img, mat=pil2mat(img))


def _read_gif(path):
    gif = Image.open(path)

    mats = []
    mat_maps = []
    for j in range(2, gif.n_frames-2):
        gif.seek(j)
        img = gif.convert(mode=gif.mode)  # 'RGB')
        img = img.resize((50, 50))
        mat = pil2mat(img)
        mat_map = np.sum(mat, axis=2) > 0
        mats.append(mat)
        mat_maps.append(mat_map)

    LOGGER.debug(f'Loaded gif ({gif.n_frames} frames): {path}')

    return dict(gif=gif, mats=mats, mat_maps=mat_maps, i=0, n=len(mats))


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
        self.terrain_terrain = _read_img(self.folder.joinpath('terrain/terrain.png'),
                                         resize=False)
        self.terrain_gif_jet = _read_gif(
            self.folder.joinpath('terrain/jet.gif'))


# %% ---- 2023-11-17 ------------------------
# Play ground


# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

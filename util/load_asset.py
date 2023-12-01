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
import time
import contextlib
import numpy as np

from threading import Thread
from PIL import Image
from . import LOGGER, CONF, singleton
from .img_tool import pil2mat
from .mapbox_tool import Mapbox

from rich import inspect

# %% ---- 2023-11-17 ------------------------
# Function and class


def _read_img(path, new_size: tuple = None, name: str = 'na'):
    img = Image.open(path)
    img = img.convert(mode='RGB')

    if new_size is not None:
        img = img.resize(new_size)
        LOGGER.debug(f'Resized the image: {path}')
    else:
        LOGGER.debug(f'Not resized the image: {path}')

    LOGGER.debug(f'Loaded image: {path}')

    return dict(name=name, img=img, mat=pil2mat(img))


def _read_gif(path):
    gif = Image.open(path)

    mats = []
    mat_maps = []
    for j in range(2, gif.n_frames-2):
        gif.seek(j)
        img = gif.convert(mode=gif.mode)  # 'RGB')
        img = img.resize((50, 50))
        # Rotate the image to fit the forward direction
        mat = pil2mat(img).transpose((1, 0, 2))[::-1]
        mat_map = np.sum(mat, axis=2) > 0
        mats.append(mat)
        mat_maps.append(mat_map)

    LOGGER.debug(f'Loaded gif ({gif.n_frames} frames): {path}')

    return dict(gif=gif, mats=mats, mat_maps=mat_maps, i=0, n=len(mats))


@singleton
class Asset(object):
    root = CONF.root_path
    folder = CONF.root_path.joinpath('asset')
    mapbox = Mapbox()
    lon = -180
    lat = 30

    def __init__(self):
        self.load_asset()
        Thread(target=self._real_time_terrain, daemon=True).start()

    def load_asset(self):
        rsvp_size = (int(CONF.width), int(CONF.height))
        self.image_rsvp_idle = _read_img(
            self.folder.joinpath('rsvp/idle.png'), new_size=rsvp_size)

        self.image_rsvp_between_blocks = _read_img(self.folder.joinpath('rsvp/between-blocks.png'),
                                                   new_size=rsvp_size)

        self.terrain_terrain = _read_img(
            self.folder.joinpath('terrain/terrain.png'))

        self.terrain_gif_jet = _read_gif(
            self.folder.joinpath('terrain/jet.gif'))

        self.terrain_bomb = _read_img(
            self.folder.joinpath('terrain/bomb.png'), name='bomb', new_size=(50, 50))

    def _real_time_terrain(self):
        # ! Only works when the mapbox is valid
        LOGGER.debug('Mapbox starts.')
        while self.mapbox.valid:
            # Rolling 1.0 degrees for 1.0 seconds
            self.lon = (time.time()/1.0 % 360) - 180
            with contextlib.suppress(Exception):
                dct, key = self.mapbox.fetch_img(self.lon, self.lat)
                self.terrain_terrain = dct
                LOGGER.debug(f'Updated terrain: {key}')

            # ! Add some gap, to make sure it will not crush the system in a doing-nothing-loop
            time.sleep(0.1)
        LOGGER.debug('Mapbox stopped.')


# %% ---- 2023-11-17 ------------------------
# Play ground


# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

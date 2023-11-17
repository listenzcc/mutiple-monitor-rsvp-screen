"""
File: terrain_monitor.py
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
import opensimplex
import numpy as np

from threading import Thread

from . import LOGGER, CONF, singleton
from .message_box import MessageBox
from .load_asset import Asset
from .img_tool import overlay, draw_trace


# %% ---- 2023-11-17 ------------------------
# Function and class
@singleton
class Jet(object):
    asset = Asset()

    def __init__(self):
        pass

    def get(self):
        i = int(self.asset.terrain_gif_jet['i'])
        mat = self.asset.terrain_gif_jet['mats'][i]
        mat_map = self.asset.terrain_gif_jet['mat_maps'][i]
        self.asset.terrain_gif_jet['i'] += 1/5
        if int(self.asset.terrain_gif_jet['i']) >= self.asset.terrain_gif_jet['n']:
            self.asset.terrain_gif_jet['i'] = 0

        return mat, mat_map


def get_noise(x, y):
    return opensimplex.noise2(x, y) * 0.5 + 0.5


@singleton
class TerrainMonitor(object):
    winname = str(CONF.terrain_wnd_name)
    asset = Asset()
    jet = Jet()
    dt = 0.001
    x = 0.5
    y = 0.5
    dx = 0.001  # np.random.randn() / 100
    dy = 0.001  # np.random.randn() / 100
    trace = []

    def __init__(self):
        Thread(target=self.loop, daemon=True).start()

    def update(self):
        self.x = get_noise(1, time.time()/10)
        self.y = get_noise(2, time.time()/10)
        self.trace.append((self.x, self.y))
        self.trace = self.trace[-500:]

    def loop(self):
        cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.winname, cv2.WND_PROP_TOPMOST, 1)

        while True:
            self.update()
            cv2.setWindowTitle(self.winname, self.winname)

            mat = self.asset.terrain_terrain['mat'].copy()
            mat_jet, mat_jet_map = self.jet.get()
            draw_trace(mat, self.trace, copy=False)
            overlay(mat, mat_jet, mat_jet_map, self.x, self.y, copy=False)
            # mat[100:150, 100:150][mat_jet_map] = mat_jet[mat_jet_map]

            cv2.imshow(self.winname, mat)
            cv2.pollKey()
            time.sleep(self.dt)

        cv2.destroyAllWindows()

# %% ---- 2023-11-17 ------------------------
# Play ground

# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

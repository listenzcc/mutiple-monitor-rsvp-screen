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
    fps = 20

    def __init__(self):
        pass

    def get(self):
        i = int(time.time() * self.fps)
        i %= self.asset.terrain_gif_jet['n']
        mat = self.asset.terrain_gif_jet['mats'][i]
        mat_map = self.asset.terrain_gif_jet['mat_maps'][i]
        return mat, mat_map


class Thumbnail(object):
    k = 10  # The thumbnail lasts how many seconds
    valid = True

    def __init__(self, dct, x, y):
        self.name = dct['name']
        self.mat = dct['mat']
        self.tic = None
        self.x = x
        self.y = y
        LOGGER.debug(f'Thumbnail is created {self.name}, {x}, {y}')

    def get(self):
        # Set tic at its first call
        if self.tic is None:
            self.tic = time.time()
            LOGGER.debug(f'Thumbnail is activated {self.name}')

        t = (time.time() - self.tic) / self.k

        alpha = max(1-t, 0)

        if t > 1:
            self.valid = False
            LOGGER.debug(f'Thumbnail become invalid {self.name}')

        return self.mat, alpha


def get_noise(x, y):
    return opensimplex.noise2(x, y) * 0.5 + 0.5


@singleton
class TerrainMonitor(object):
    winname = str(CONF.terrain_wnd_name)
    asset = Asset()
    jet = Jet()
    mb = MessageBox()
    dt = 0.001
    x = 0.5
    y = 0.5
    dx = 0.001  # np.random.randn() / 100
    dy = 0.001  # np.random.randn() / 100
    trace = []
    thumbnails = []

    def __init__(self):
        Thread(target=self.loop, daemon=True).start()

    def update_status(self):
        # Update the position of the jet
        self.x = get_noise(1, time.time()/10)
        self.y = get_noise(2, time.time()/10)

        # Update the trace
        self.trace.append((self.x, self.y))

        if len(self.trace) > 5000:
            self.trace = self.trace[-2500:]
            LOGGER.warning('Trace exceeded limit (5000), shrink to the half')

        if self.mb.toggle_clear_terrain_trace:
            self.trace = []
            self.mb.toggle_clear_terrain_trace = False
            LOGGER.debug('Unset messageBox toggle_clear_terrain_trace flag')

        # Update the thumbnail
        if self.mb.rsvp_target_buffer:
            self.thumbnails.append(
                Thumbnail(self.mb.rsvp_target_buffer.pop(), self.x, self.y))

        self.thumbnails = [e for e in self.thumbnails if e.valid]

    def loop(self):
        cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.winname, cv2.WND_PROP_TOPMOST, 1)

        while True:
            self.update_status()
            cv2.setWindowTitle(self.winname, self.winname)

            mat = self.asset.terrain_terrain['mat'].copy()
            mat_jet, mat_jet_map = self.jet.get()

            draw_trace(mat, self.trace, copy=False)

            for thumb in self.thumbnails:
                m, a = thumb.get()
                overlay(mat, m, None, thumb.x, thumb.y, a, copy=False)
            # [overlay(mat, e.mat, None, e.x, e.y, e.alpha, copy=False)
            #  for e in self.thumbnails]

            overlay(mat, mat_jet, mat_jet_map, self.x, self.y, copy=False)

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

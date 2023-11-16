"""
File: rsvp_monitor.py
Author: Chuncheng Zhang
Date: 2023-11-16
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


# %% ---- 2023-11-16 ------------------------
# Requirements and constants
import cv2
import time
import numpy as np

from . import LOGGER, CONF


# %% ---- 2023-11-16 ------------------------
# Function and class
class RSVPMonitor(object):
    winname = str(CONF.rsvp_wnd_name)
    fps = int(CONF.rsvp_fps)

    def __init__(self):
        pass

    def update_fps(self):
        self.fps = int(CONF.rsvp_fps)
        return 1 / self.fps

    def display_rsvp_block(self, block):
        n = len(block)

        dt = self.update_fps()
        next_t = dt

        # times = np.linspace(0, n/self.fps, n, endpoint=False)

        tic = time.time()

        i = 0
        while i < n:
            t = time.time() - tic

            if (t < next_t):
                time.sleep(0.001)
                continue

            print(f'Image onset: {i} | {t:0.4f}')

            dt = self.update_fps()
            next_t = t + dt - t % dt

            obj = block[i]
            mat = obj[3]

            cv2.imshow(self.winname, mat)
            cv2.pollKey()

            if obj[0] == 'target':
                cv2.imshow('Target', mat)
                cv2.pollKey()

            i += 1

        toc = time.time()
        t = toc-tic
        r = t/n
        LOGGER.debug(f'Finished rsvp block: {r} | {t} | {n}')


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

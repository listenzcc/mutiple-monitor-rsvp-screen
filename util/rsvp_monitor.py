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

from threading import Thread

from . import LOGGER, CONF, singleton
from .messager import MessageBox


# %% ---- 2023-11-16 ------------------------
# Function and class
@singleton
class RSVPMonitor(object):
    winname = str(CONF.rsvp_wnd_name)
    fps = int(CONF.rsvp_fps)
    mb = MessageBox()

    def __init__(self):
        pass

    def update_fps(self):
        self.fps = int(CONF.rsvp_fps)
        return 1 / self.fps

    def display_rsvp_block(self, block):
        cv2.namedWindow("Target", cv2.WINDOW_NORMAL)
        cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)

        n = len(block)

        dt = self.update_fps()
        next_t = dt

        self.mb.send_parallel_code(CONF.signal_rsvp_block_start)

        tic = time.time()

        i = 0
        while i < n:
            t = time.time() - tic

            if (t < next_t):
                time.sleep(0.001)
                continue

            dt = self.update_fps()
            next_t = t + dt - t % dt

            obj = block[i]
            img = obj[2]
            mat = obj[3]

            print(f'Image onset: {i} | {t:0.4f} | {mat.shape}')

            cv2.imshow(self.winname, mat)
            cv2.pollKey()

            if obj[0] == 'target':
                cv2.imshow('Target', mat)
                cv2.pollKey()
                self.mb.send_parallel_code(CONF.signal_target_onset)
            else:
                self.mb.send_parallel_code(CONF.signal_other_onset)

            i += 1

        self.mb.send_parallel_code(CONF.signal_rsvp_block_stop)

        toc = time.time()
        t = toc-tic
        r = t/n
        LOGGER.debug(f'Finished rsvp block: {r} | {t} | {n}')
        cv2.destroyAllWindows()


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

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
from .message_box import MessageBox
from .load_asset import Asset


# %% ---- 2023-11-16 ------------------------
# Function and class
@singleton
class RSVPMonitor(object):
    winname = str(CONF.rsvp_wnd_name)
    winname_target = str(CONF.rsvp_target_wnd_name)
    rsvp_fps = int(CONF.rsvp_fps)
    mb = MessageBox()
    asset = Asset()
    blocks = []
    dt = 0.001

    def __init__(self):
        Thread(target=self.loop, daemon=True).start()

    def update_fps(self):
        self.rsvp_fps = int(CONF.rsvp_fps)
        return 1 / self.rsvp_fps

    def loop(self):
        cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)
        cv2.namedWindow(self.winname_target, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.winname, cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty(self.winname_target, cv2.WND_PROP_TOPMOST, 1)

        while True:
            # Reset titles
            cv2.setWindowTitle(self.winname, self.winname)
            cv2.setWindowTitle(self.winname_target, self.winname_target)

            # Display idle image
            cv2.imshow(self.winname, self.asset.image_rsvp_idle['mat'])
            cv2.imshow(self.winname_target, self.asset.image_rsvp_idle['mat'])
            cv2.pollKey()
            time.sleep(self.dt)

            # There are RSVP blocks
            while self.blocks:
                cv2.imshow(
                    self.winname, self.asset.image_rsvp_between_blocks['mat'])
                cv2.imshow(self.winname_target,
                           self.asset.image_rsvp_between_blocks['mat'])
                cv2.waitKey(1000 * CONF.rsvp_between_blocks_secs)
                self.display_rsvp_block(self.blocks.pop(0))

        cv2.destroyAllWindows()

    def display_rsvp_block(self, block):
        n = len(block)

        dt = self.update_fps()
        next_t = dt

        self.mb.send_parallel_code(CONF.signal_rsvp_block_start)

        tic = time.time()

        i = 0
        while i < n:
            t = time.time() - tic

            if (t < next_t):
                time.sleep(self.dt)
                continue

            dt = self.update_fps()
            next_t = t + dt - t % dt

            obj = block[i]
            mat = obj[3]

            print(f'Image onset: {i} | {t:0.4f} | {mat.shape}')

            # winname | remain blocks | real fps | ideal fps
            cv2.setWindowTitle(self.winname,
                               f'{self.winname} | Blocks: {len(self.blocks)} | Fps: {(i+1)/t:0.4f} | {CONF.rsvp_fps}')
            cv2.imshow(self.winname, mat)
            cv2.pollKey()

            if obj[0] == 'target':
                # winname_target | latest target file name
                cv2.setWindowTitle(self.winname_target,
                                   f'{self.winname_target} | Name: {obj[1]}')
                cv2.imshow(self.winname_target, mat)
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


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

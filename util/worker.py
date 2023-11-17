"""
File: worker.py
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

from threading import Thread

from . import LOGGER, singleton
from .rsvp_images import RSVPImages
from .rsvp_monitor import RSVPMonitor


# %% ---- 2023-11-16 ------------------------
# Function and class

@singleton
class Worker(object):
    monitor = RSVPMonitor()
    rsvp_images = RSVPImages()
    busy = False

    def __init__(self):
        self.rsvp_images.report()

    def start_new_block(self):
        if self.busy:
            LOGGER.warning('Failed to start new block')
            return self.block

        # self._running_block()

        block = self.rsvp_images.new_block()
        self.monitor.blocks.append(block)
        # Thread(target=self._running_block, args=(block,), daemon=True).start()

        return block

    def _running_block(self, block):
        self.block = block
        self.busy = True
        LOGGER.debug('Started running block')

        self.monitor.display_rsvp_block(block)
        cv2.waitKey(0)

        self.busy = False
        LOGGER.debug('Stopped running block')


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

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
import time
import keyboard

from threading import Thread

from . import LOGGER, CONF, singleton
from .rsvp_images import RSVPImages
from .rsvp_monitor import RSVPMonitor
from .terrain_monitor import TerrainMonitor
from .message_box import MessageBox


# %% ---- 2023-11-16 ------------------------
# Function and class

@singleton
class Worker(object):
    rsvp_monitor = RSVPMonitor()
    rsvp_images = RSVPImages()
    terrain_monitor = TerrainMonitor()
    mb = MessageBox()

    def __init__(self):
        self.rsvp_images.report()

    def start_new_block(self):
        block = self.rsvp_images.new_block()
        self.rsvp_monitor.blocks.append(block)
        return block

    def _key_press_callback(self, key):
        self.mb.on_key_press(key.name)

    def keep_alive(self):
        Thread(target=self._keep_alive).start()

    def _keep_alive(self):
        keyboard.on_press(self._key_press_callback, suppress=True)

        while True:
            if not self.rsvp_monitor.running:
                LOGGER.debug('RSVP monitor is not running')
                break

            if not self.terrain_monitor.running:
                LOGGER.debug('Terrain monitor is not running')
                break

            time.sleep(0.1)

        keyboard.unhook_all()


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

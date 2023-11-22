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
import contextlib

from threading import Thread

from . import LOGGER, CONF, singleton
from .rsvp_images import RSVPImages
from .rsvp_monitor import RSVPMonitor
from .terrain_monitor import TerrainMonitor
from .message_box import MessageBox

from rich import print, inspect

# %% ---- 2023-11-16 ------------------------
# Function and class


@singleton
class Worker(object):
    '''
    The main worker of the project.
    Its keep_alive method keeps the program alive.
    '''
    rsvp_monitor = RSVPMonitor()
    rsvp_images = RSVPImages()
    terrain_monitor = TerrainMonitor()
    mb = MessageBox()

    def __init__(self):
        self.rsvp_images.report()

    def insert_rsvp_block(self):
        block = self.rsvp_images.new_block()
        self.rsvp_monitor.blocks.append(block)
        return block

    def _key_press_callback(self, key):
        name = key.name
        if len(name) > 1:
            return
        self.mb.on_key_press(name)

        if name == '-':
            with contextlib.suppress(Exception):
                self.rsvp_monitor.blocks.pop()

        elif name == '=':
            self.insert_rsvp_block()

        # inspect(key, all=True)
        print(name)

    def keep_alive(self):
        Thread(target=self._keep_alive).start()

    def _keep_alive(self):
        """
        Keeps the program alive by monitoring the RSVP and Terrain monitors.

        The method starts by registering a key press callback using the keyboard.on_press function.
        It then enters an infinite loop where it checks if the RSVP and Terrain monitors are running.
        If either of them is not running, it logs a debug message and breaks out of the loop.
        The method sleeps for 0.1 seconds between each iteration of the loop.
        Finally, it unregisters all key press callbacks using keyboard.unhook_all().

        Args:
            self: The instance of the class.

        Returns:
            None

        Examples:
            >>> worker = Worker()
            >>> worker._keep_alive()
        """

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

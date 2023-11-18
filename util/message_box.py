"""
File: message_box.py
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
from threading import Thread

from . import LOGGER, CONF, singleton
from .img_tool import pil2mat


# %% ---- 2023-11-16 ------------------------
# Function and class

@singleton
class MessageBox(object):
    port = CONF.parallel_port
    toggle_clear_terrain_trace = False
    rsvp_target_buffer = []

    def __init__(self):
        LOGGER.debug(f'Initialized with parallel port: {self.port}')

    def send_parallel_code(self, code: int):
        LOGGER.debug(f'Sent code to parallel port: {code}')

    def internal_message_rsvp_block_starts(self):
        self.toggle_clear_terrain_trace = True
        LOGGER.debug('RSVP block started')

    def internal_message_rsvp_target_onset(self, name, thumbnail):
        mat = pil2mat(thumbnail)
        self.rsvp_target_buffer.append(dict(name=name, mat=mat))
        LOGGER.debug(
            f'RSVP target ({name}) onset, buffer size: {len(self.rsvp_target_buffer)}')


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

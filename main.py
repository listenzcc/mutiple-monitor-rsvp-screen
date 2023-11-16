"""
File: main.py
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
from util import LOGGER
from util.rsvp_images import RSVPImages
from util.rsvp_monitor import RSVPMonitor


# %% ---- 2023-11-16 ------------------------
# Function and class


# %% ---- 2023-11-16 ------------------------
# Play ground
if __name__ == '__main__':
    monitor = RSVPMonitor()
    rsvp_images = RSVPImages()
    rsvp_images.report()
    block = rsvp_images.new_block()
    monitor.display_rsvp_block(block)


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

"""
File: __init__.py
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

from PIL import Image
from threading import Thread
from omegaconf import OmegaConf
from dataclasses import dataclass

from pathlib import Path
from loguru import logger as LOGGER
from datetime import datetime
from rich import print, inspect


# %% ---- 2023-11-16 ------------------------
# Function and class
root = Path(__file__).parent.parent


@dataclass
class Project:
    root: Path = root


CONF = OmegaConf.structured(Project)
print(CONF)

# %% ---- 2023-11-16 ------------------------
# Play ground
now = datetime.now()  # current date and time
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
LOGGER.add(root.joinpath(f'log/{date_time}.log'))


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

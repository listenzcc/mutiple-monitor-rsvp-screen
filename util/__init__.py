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
import sys
from loguru import logger

from pathlib import Path
from datetime import datetime
from omegaconf import OmegaConf

from dataclasses import dataclass


# %% ---- 2023-11-16 ------------------------
# Function and class
root = Path(__file__).parent.parent
root = Path(sys.argv[0]).parent


@dataclass
class CustomOverride:
    version: str = '0.0'


@dataclass
class Runtime(CustomOverride):
    root_path: Path = root


def init_logger():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    logger.add(root.joinpath(f'log/{date_time}.log'))
    return logger


LOGGER = init_logger()


def init_conf():
    p = root.joinpath('custom/custom.json')
    if p.is_file():
        custom = OmegaConf.load(p)
    else:
        custom = OmegaConf.structured(CustomOverride)

    runtime = OmegaConf.structured(Runtime)
    CONF = OmegaConf.merge(custom, runtime)

    OmegaConf.save(CONF, root.joinpath('latest.yaml'))

    return CONF


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        else:
            LOGGER.debug(f'Using existing instance: {instances[cls]}')

        return instances[cls]

    return _singleton


# %% ---- 2023-11-16 ------------------------
# Play ground
CONF = init_conf()
LOGGER.debug(f'Started with {CONF}')


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

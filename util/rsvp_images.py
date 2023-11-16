"""
File: rsvp_images.py
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
import time
import numpy as np
import pandas as pd

from tqdm.auto import tqdm

from PIL import Image
from pathlib import Path
from threading import Thread

from rich import print, inspect

from . import LOGGER, CONF

# %% ---- 2023-11-16 ------------------------
# Function and class


def _find_images(folder: Path, type: str = 'na'):
    if not folder.is_dir():
        LOGGER.error(f'Invalid folder: {folder}')
        return []

    def _read(file):
        # Only tolerate file can not open error
        try:
            image = Image.open(file)
        except Exception as err:
            return

        image = image.convert(mode='RGB')
        image = image.resize((int(CONF.width), int(CONF.height)))
        res.append((type, file.name, image))

        return

    res = []
    ts = []

    for file in tqdm([e for e in folder.iterdir() if e.is_file()], 'Find images'):
        t = Thread(target=_read, args=(file,), daemon=True)
        t.start()
        ts.append(t)

    while ts:
        ts = [e for e in ts if e.is_alive()]
        time.sleep(0.1)

    LOGGER.debug(f'Finished read images: {len(res)} | {folder}')

    return res


def _mk_rsvp_block_design():
    n = int(CONF.rsvp_block_total_images)
    k = int(CONF.rsvp_block_targets)
    m = int(CONF.rsvp_block_targets_min_gap)

    valid_flag = (k+1)*(m+1) < n

    if not valid_flag:
        LOGGER.error(f'Invalid rsvp block setup, {(n, k, m)}')

    assert valid_flag, f'Invalid rsvp block setup, {(n, k, m)}'

    res = []
    for _ in range(k):
        res.extend(0 for _ in range(m))
        res.append(1)
    res.extend(0 for _ in range(m))

    while len(res) < n:
        i = np.random.randint(0, len(res))
        res.insert(i, 0)

    LOGGER.debug(f'Generated rsvp block design: {res}')

    return res


class RSVPImages(object):
    def __init__(self):
        self.load()

    def report(self):
        grp = self.table.groupby('type')
        print('-' * 80)
        print(self.table)
        print(grp.count())
        print(grp.first())

    def load(self, targets_folder=None, others_folder=None):
        targets_folder = CONF.targets_folder if targets_folder is None else targets_folder
        others_folder = CONF.others_folder if others_folder is None else others_folder

        self.targets_folder = Path(targets_folder)
        self.others_folder = Path(others_folder)

        self.targets = _find_images(self.targets_folder, 'target')
        self.others = _find_images(self.others_folder, 'other')

        df1 = pd.DataFrame(self.targets)
        df2 = pd.DataFrame(self.others)
        self.table = pd.concat([df1, df2])
        self.table.columns = ['type', 'name', 'imgObject']
        self.table['size'] = self.table['imgObject'].map(lambda img: img.size)
        LOGGER.debug(f'Loaded images for {len(self.table)} images.')

    def shuffle(self):
        self.target_idx = 0
        self.other_idx = 0
        np.random.shuffle(self.targets)
        np.random.shuffle(self.others)
        LOGGER.debug('Shuffled images')

    def get_target(self):
        output = self.targets[self.target_idx]
        self.target_idx += 1
        if self.target_idx >= len(self.targets):
            self.target_idx = 0
            LOGGER.warning('Target images are exceeded, re-start from 0')
        return output

    def get_other(self):
        output = self.others[self.other_idx]
        self.other_idx += 1
        if self.other_idx >= len(self.others):
            self.other_idx = 0
            LOGGER.warning('Other images are exceeded, re-start from 0')
        return output

    def new_block(self):
        type_line = _mk_rsvp_block_design()
        self.shuffle()
        block = []
        for e in type_line:
            obj = self.get_target() if e == 1 else self.get_other()
            mat = np.array(obj[-1], dtype=np.uint8)
            block.append(obj + (mat,))
        LOGGER.debug(f'Generated block: {[e[:2] for e in block]}')
        return block


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

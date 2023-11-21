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
import time
import pandas as pd

from threading import Thread

from . import LOGGER, CONF, singleton
from .img_tool import pil2mat
from .parallel.parallel import Parallel


# %% ---- 2023-11-16 ------------------------
# Function and class
code = dict(
    rsvp_block_start=CONF.code_rsvp_block_start,
    rsvp_block_stop=CONF.code_rsvp_block_stop,
    target_onset=CONF.code_target_onset,
    other_onset=CONF.code_other_onset,
    subject_keypress=CONF.code_subject_keypress,
    bomb=CONF.code_bomb
)


@singleton
class MessageBox(object):
    trigger_rsvp_block_starts = False
    trigger_rsvp_block_stops = False
    parallel = Parallel(CONF.parallel_port)
    rsvp_target_buffer = []
    rsvp_block_record = []

    def __init__(self):
        pass

    def _record_event(self, dct: dict, clear: bool = False):
        if clear:
            self.rsvp_block_record = []

        dct['time'] = time.time()
        self.rsvp_block_record.append(dct)

    def _save_events(self):
        df = pd.DataFrame(self.rsvp_block_record)
        path = CONF.root_path.joinpath(f'block_records/{time.time()}.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_json(path)
        LOGGER.debug(f'Saved to {path}')

    def on_bomb(self):
        self._send_parallel_code(code['bomb'])
        self._record_event(dict(event='BOMB'))

    def on_key_press(self, name):
        self._send_parallel_code(code['subject_keypress'])
        self._record_event(dict(event='KEY_PRESS', name=name))

    def on_rsvp_block_starts(self):
        self.trigger_rsvp_block_starts = True
        self._send_parallel_code(code['rsvp_block_start'])
        self._record_event(dict(event='RSVP_BLOCK_START'), clear=True)

    def on_rsvp_block_stops(self):
        self.trigger_rsvp_block_stops = True
        self._send_parallel_code(code['rsvp_block_stop'])
        self._record_event(dict(event='RSVP_BLOCK_STOP'))
        self._save_events()

    def on_rsvp_other_image_onsets(self):
        self._send_parallel_code(code['other_onset'])
        self._record_event(dict(event='RSVP_OTHER_ONSET'))

    def on_rsvp_target_image_onsets(self, name, thumbnail):
        self._send_parallel_code(code['target_onset'])
        mat = pil2mat(thumbnail)
        self.rsvp_target_buffer.append(dict(name=name, mat=mat))
        self._record_event(dict(event='RSVP_TARGET_ONSET', name=name))
        LOGGER.debug(
            f'RSVP target ({name}) onset, buffer size: {len(self.rsvp_target_buffer)}')

    def _send_parallel_code(self, code: int):
        self.parallel.send(code)
        LOGGER.debug(f'Sent code to parallel port: {code}')


# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

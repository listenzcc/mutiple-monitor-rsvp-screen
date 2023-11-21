"""
File: terrain_monitor.py
Author: Chuncheng Zhang
Date: 2023-11-17
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


# %% ---- 2023-11-17 ------------------------
# Requirements and constants
import cv2
import time
import opensimplex
import numpy as np

from threading import Thread

from . import LOGGER, CONF, singleton
from .message_box import MessageBox
from .load_asset import Asset
from .img_tool import overlay, draw_trace
from .patrol_trace import PatrolTrace


# %% ---- 2023-11-17 ------------------------
# Function and class
@singleton
class Jet(object):
    asset = Asset()
    fps = 20

    def __init__(self):
        pass

    def get(self):
        i = int(time.time() * self.fps)
        i %= self.asset.terrain_gif_jet['n']
        mat = self.asset.terrain_gif_jet['mats'][i]
        mat_map = self.asset.terrain_gif_jet['mat_maps'][i]
        return mat, mat_map


class Thumbnail(object):
    lasts_secs = 10  # The thumbnail lasts how many seconds
    valid = True

    def __init__(self, dct: dict, x: float, y: float, lasts_secs=None):
        '''
        Generate the thumbnail with the image and its position (x, y)
        '''
        self.name = dct.get('name', 'na')
        self.mat = dct['mat']
        self.mat_map = np.sum(self.mat, axis=2) > 0
        self.tic = None
        self.x = x
        self.y = y

        if lasts_secs is not None:
            self.lasts_secs = lasts_secs

        LOGGER.debug(f'Thumbnail created {self.name}, {x}, {y}')

    def get(self):
        # Set tic at its first call
        if self.tic is None:
            self.tic = time.time()
            LOGGER.debug(f'Thumbnail activated {self.name}')

        t = (time.time() - self.tic) / self.lasts_secs

        alpha = max(1-t, 0)

        if t > 1:
            self.valid = False
            LOGGER.debug(f'Thumbnail dis-activated {self.name}')

        return dict(mat=self.mat, mat_map=self.mat_map, alpha=alpha)


def get_noise(x, y):
    return opensimplex.noise2(x, y) * 0.5 + 0.5


@singleton
class TerrainMonitor(object):
    winname = str(CONF.terrain_wnd_name)
    asset = Asset()
    jet = Jet()
    mb = MessageBox()
    pt = PatrolTrace()
    dt = 0.001
    x = 0.5
    y = 0.5
    theta = 0
    thumbnails = []
    running = True

    def __init__(self):
        Thread(target=self.loop, daemon=True).start()

    def update_status(self):
        # Update the position of the jet
        xy, left, right = self.pt.get()
        x = xy['x']
        y = xy['y']
        visited = xy['visited']

        if not visited:
            theta = np.arctan2(y-self.y, x-self.x) * 180 / np.pi
            self.theta = theta
            # Prevent repeat visit
            xy['visited'] = True

        self.x = x
        self.y = y

        # It is bomb and has not been visited
        if xy.get('is_bomb', False) and not visited:
            self.thumbnails.append(Thumbnail(
                self.asset.terrain_bomb.copy(), self.x + 0.1*(np.random.rand()-0.5), self.y +
                0.1*(np.random.rand()-0.5)
            ))
            self.mb.on_bomb()

        # Toggle the trace,
        # It usually means the RSVP block starts
        if self.mb.trigger_rsvp_block_starts:
            self.pt.generate_trace()
            self.thumbnails = []
            self.mb.trigger_rsvp_block_starts = False
            LOGGER.debug('Unset messageBox toggle_clear_terrain_trace flag')

        # Update the thumbnail
        # One-time for one thumbnail
        if self.mb.rsvp_target_buffer:
            self.thumbnails.append(
                Thumbnail(self.mb.rsvp_target_buffer.pop(), self.x, self.y, 1))

        self.thumbnails = [e for e in self.thumbnails if e.valid]

        return left, right

    def loop(self):
        cv2.namedWindow(self.winname, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.winname, cv2.WND_PROP_TOPMOST, 1)

        while cv2.getWindowProperty(self.winname, cv2.WND_PROP_VISIBLE):
            left, right = self.update_status()

            cv2.setWindowTitle(self.winname, self.winname)

            mat = self.asset.terrain_terrain['mat'].copy()
            mat_jet, mat_jet_map = self.jet.get()

            # Draw the trace in the tail
            draw_trace(mat, left, color=(200, 0, 0), copy=False)
            draw_trace(mat, right, color=(0, 200, 0), copy=False)

            # Draw the thumbnails
            for thumb in self.thumbnails:
                obj = thumb.get()
                overlay(mat, obj['mat'], obj['mat_map'],
                        thumb.x, thumb.y, obj['alpha'], copy=False)

            # Draw the jet
            w, h, _ = mat_jet.shape
            M = cv2.getRotationMatrix2D((w/2, h/2), self.theta, 1.0)
            rotated = cv2.warpAffine(mat_jet, M, (w, h))
            rotated_map = np.sum(rotated, 2) > 0
            # overlay(mat, mat_jet, mat_jet_map, self.x, self.y, 0.9, copy=False)
            overlay(mat, rotated, rotated_map, self.x, self.y, 0.9, copy=False)

            cv2.imshow(self.winname, mat)
            cv2.pollKey()
            time.sleep(self.dt)

        # cv2.destroyAllWindows()
        self.running = False
        LOGGER.debug(f'Closed window: {self.winname}')

# %% ---- 2023-11-17 ------------------------
# Play ground

# %% ---- 2023-11-17 ------------------------
# Pending


# %% ---- 2023-11-17 ------------------------
# Pending

"""
File: patrol_trace.py
Author: Chuncheng Zhang
Date: 2023-11-21
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


# %% ---- 2023-11-21 ------------------------
# Requirements and constants
import time
import bezier
import random
import numpy as np

from . import CONF, LOGGER, singleton


# %% ---- 2023-11-21 ------------------------
# Function and class
@singleton
class PatrolTrace(object):
    total_secs = CONF.patrol_total_secs
    total_bombs = CONF.patrol_total_bombs
    total_pnts = CONF.patrol_total_pnts
    degree = 1

    def __init__(self):
        self.generate_trace()

    def get(self, t=None):
        """
        Gets the check point at a given time.
        It will generate new trace if no right points are available

        Args:
            t (float, optional): The time to get the check point for. Defaults to None = time.time().

        Returns:
            dict: The check point at the given time.

        Raises:
            IndexError: If there are no check points available.

        Examples:
            >>> patrol = PatrolTrace()
            >>> check_point = patrol.get(t=1609459200.0)
        """

        if t is None:
            t = time.time()

        check_points = self.check_points
        left = [e for e in check_points if e['t'] < t]
        right = [e for e in check_points if not e['t'] < t]
        # Have not been visited yet
        if not left:
            xy = right[0]

        # Have been visited all, generate new trace
        if not right:
            xy = left[-1]
            self.generate_trace()
        else:
            # Inside the trace
            xy = right[0]

        return xy, left, right

    def generate_trace(self, tic=None, nodes=None):
        # Nodes: The control points of the bezier curve;
        # Points: The patrol trace

        # If nodes is not provided, use random values in (0, 1)
        if tic is None:
            tic = time.time()

        if nodes is None:
            nodes = np.asfortranarray(np.random.rand(2, 10))
            LOGGER.warning('Generated random nodes')

        curve = bezier.Curve(nodes, degree=nodes.shape[1]-1)
        s_vals = np.linspace(0, 1, self.total_pnts)
        # Convert 2 x n array into n x 2 array, n=self.total_pnts
        pnts = curve.evaluate_multi(s_vals).transpose()
        # The check_point is dict,
        # t: When the point is visited;
        # x, y: Where the point is visited.
        check_points = [
            dict(t=tic+v * self.total_secs, x=pnt[0], y=pnt[1], visited=False)
            for v, pnt in zip(s_vals, pnts)
        ]

        select = random.choices(check_points, k=int(self.total_bombs))
        for e in select:
            e['is_bomb'] = True

        self.check_points = check_points
        LOGGER.debug('Generated check_points')

        return check_points


# %% ---- 2023-11-21 ------------------------
# Play ground


# %% ---- 2023-11-21 ------------------------
# Pending


# %% ---- 2023-11-21 ------------------------
# Pending

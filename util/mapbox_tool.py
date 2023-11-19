"""
File: mapbox_tool.py
Author: Chuncheng Zhang
Date: 2023-11-19
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


# %% ---- 2023-11-19 ------------------------
# Requirements and constants

import requests
from io import BytesIO
from PIL import Image
from . import singleton
from .img_tool import pil2mat


# %% ---- 2023-11-19 ------------------------
# Function and class

def mk_box(lon, lat):
    return [lon-10, lat-10, lon+10, lat+10]


def fetch_png(lon, lat, img_width, img_height, access_token):
    box = f'{mk_box(lon, lat)}'
    size = f'{img_width:d}x{img_height:d}'
    url = f'https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/{box}/{size}?access_token={access_token}'
    resp = requests.get(url)
    # print(url, resp)
    io = BytesIO(resp.content)
    img = Image.open(io)
    mat = pil2mat(img)
    return dict(img=img, mat=mat)


@singleton
class Mapbox(object):
    access_token = open(
        'C:\\Users\\zcc\\OneDrive\\SafeBox\\.mapbox_token').read()
    buffer = {}

    def __init__(self):
        pass

    def fetch_img(self, lon, lat, img_width=1000, img_height=1000):
        box = f'{mk_box(lon, lat)}'
        size = f'{img_width:d}x{img_height:d}'
        key = f'{box}-{size}'

        if key in self.buffer:
            dct = self.buffer[key]
        else:
            dct = fetch_png(lon, lat, img_width, img_height, self.access_token)
            self.buffer[key] = dct

        return dct, key
# %% ---- 2023-11-19 ------------------------
# Play ground


# %% ---- 2023-11-19 ------------------------
# Pending


# %% ---- 2023-11-19 ------------------------
# Pending

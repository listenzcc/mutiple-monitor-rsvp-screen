"""
File: test.py
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
import cv2
import requests
import numpy as np

from io import BytesIO
from PIL import Image
from mapbox import Static
from tqdm.auto import tqdm
from rich import print, inspect


# %% ---- 2023-11-19 ------------------------
# Function and class
access_token = open('C:\\Users\\zcc\\OneDrive\\SafeBox\\.mapbox_token').read()


def mk_box(lon, lat):
    return [lon-0.1, lon+0.1, lat-0.1, lat+0.1]


# %% ---- 2023-11-19 ------------------------
# Play ground
lon = -60.05
lat = 12

box = mk_box(lon, lat)
url = f'https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/{box}/400x400?access_token={access_token}'
resp = requests.get(url)
with open(f'mapbox-{lon}-{lat}.png', 'wb') as f:
    f.write(resp.content)

io = BytesIO(resp.content)

img = Image.open(io)
img.save('b.png')
img

# %%
inspect(img)
img = img.convert('RGB', palette=img.palette)
mat = np.array(img)
mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)

cv2.imshow('a', mat)
cv2.waitKey()


# %% ---- 2023-11-19 ------------------------
# Pending


# %% ---- 2023-11-19 ------------------------
# Pending

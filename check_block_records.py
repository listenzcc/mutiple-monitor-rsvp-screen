"""
File: check_block_records.py
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
import pandas as pd
from rich import print
from pathlib import Path
import plotly.express as px


# %% ---- 2023-11-21 ------------------------
# Function and class

# %% ---- 2023-11-21 ------------------------
# Play ground
file = list(Path(__file__).parent.joinpath('block_records').iterdir())[-1]
print(file)

df = pd.read_json(file)
t0 = df.iloc[0]['time']
df['time'] -= t0

group = df.groupby('event')
print(df)
print(group.count())

px.scatter(df, x='time', y='event', hover_name='name', color='event').show()

# %% ---- 2023-11-21 ------------------------
# Pending


# %% ---- 2023-11-21 ------------------------
# Pending

"""
File: web_controller.py
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
import pandas as pd
import gradio as gr

from .worker import Worker
from . import LOGGER, CONF

worker = Worker()

# %% ---- 2023-11-16 ------------------------
# Function and class


def image_classifier(inp):
    print(inp)
    block = worker.start_new_block()
    df = gr.Dataframe(
        value=[(j,) + e[:2] for j, e in enumerate(block)],
        headers=['idx', "type", "name"],
        datatype=['number', 'str', 'str'],
        col_count=(3, "fixed"),
    )
    return df


demo = gr.Interface(fn=image_classifier, inputs="image", outputs="dataframe")
# demo.launch()

# %% ---- 2023-11-16 ------------------------
# Play ground


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

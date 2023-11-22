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

from datetime import datetime

from .worker import Worker
from . import LOGGER, CONF

worker = Worker()

# %% ---- 2023-11-16 ------------------------
# Function and class


def _record(subject, experiment):
    return f'Record: {subject}, {experiment}, {datetime.now()}'


def _insert_block():
    block = worker.insert_rsvp_block()
    return gr.Dataframe(
        value=[(j, e["img_type"], e["img_name"]) for j, e in enumerate(block)],
        headers=['idx', "type", "name"],
        datatype=['number', 'str', 'str'],
        col_count=(3, "fixed"),
    )


def _rsvp_fps(fps):
    CONF.rsvp_fps = fps
    LOGGER.debug(f'Changed RSVP fps to {fps}')

# %% ---- 2023-11-16 ------------------------
# Play ground


with gr.Blocks() as demo:
    gr.Markdown('## Subject & experiment')
    subject = gr.Textbox(label="Subject")
    experiment = gr.Textbox(label="Experiment", lines=2)
    record = gr.Textbox(value="", label='Record')
    submit_btn = gr.Button(value="Submit")
    submit_btn.click(_record, inputs=[subject, experiment], outputs=[record])

    gr.Markdown('## RSVP control')
    rsvp_fps_slider = gr.Slider(
        1, 30, value=10, step=1, interactive=True, label='FPS', info="Choose between 1 to 30 Hz")
    insert_block_btn = gr.Button(value="Insert block")
    block_design = gr.Dataframe()
    insert_block_btn.click(_insert_block, outputs=[block_design])
    rsvp_fps_slider.input(_rsvp_fps, inputs=rsvp_fps_slider)


# demo.launch()

# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

"""
File: main.py
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
from threading import Thread
from util.worker import Worker
from util.web_controller import demo


# %% ---- 2023-11-16 ------------------------
# Function and class


# %% ---- 2023-11-16 ------------------------
# Play ground
if __name__ == '__main__':
    Thread(target=demo.launch, daemon=True).start()
    worker = Worker()
    worker.run_forever()
    print('Bye')


# %% ---- 2023-11-16 ------------------------
# Pending


# %% ---- 2023-11-16 ------------------------
# Pending

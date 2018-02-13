#!/usr/bin/env python

import gym
import os
import mj_transfer
from mj_transfer.robots import NewBrightEnv

from random import random
import csv

from time import time, sleep

try:
    # Windows
    from msvcrt import getch
except ImportError:
    # Unix
    import sys
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


CURR_DIRR = os.path.abspath(os.path.curdir)
SAVE_FOLDER = './driving_data/'
SAVE_FOLDER = os.path.join(CURR_DIRR, SAVE_FOLDER)
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
SAVE_CSV = os.path.join(SAVE_FOLDER, 'labels.csv')

if __name__ == '__main__':
    with open(SAVE_CSV, 'a') as f_csv:
        f_csv.seek(0, os.SEEK_END)
        writer = csv.writer(f_csv)
        env = NewBrightEnv('192.168.42.1', 5000)
        time_init = time()
        env.reset()
        while True:
            action = [0.0, 0.0, 0.0, 0.0]
            c = getch()
            if c == 'q':
                break
            if c == 'w':
                action[0] = 1.0
            if c == 's':
                action[1] = 1.0
            if c == 'd':
                action[2] = 1.0
            if c == 'a':
                action[3] = 1.0

            # action = [1.0, 0.0, 1.0, 0.0]
            # TODO: Keep everything to 1.0 if key pressed ?
            # TODO: Deal with opposing directions ?
            state, reward, done, info = env.step(action)
            state_fname = str(time()) + '_' + str(random()) + '.jpg'
            state_path = os.path.join(SAVE_FOLDER, state_fname)
            # state_fname = state_fname.decode('utf-8')
            state.save(state_path)
            row = [state_fname,
                   action[0],
                   action[1],
                   action[2],
                   action[3]]
            print(row)
            writer.writerow(row)
            f_csv.flush()
        env.disconnect()

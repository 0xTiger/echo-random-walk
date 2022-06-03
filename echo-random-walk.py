import os
import time
import random
import curses
import argparse

from typing import List
from pathlib import Path
from itertools import chain

parser = argparse.ArgumentParser()
text_source_group = parser.add_mutually_exclusive_group(required=True)
text_source_group.add_argument('--file')
text_source_group.add_argument('--dir')
args = parser.parse_args()

import logging
logging.basicConfig(
    filename='curses.log',
    filemode='w',
    format='%(asctime)s %(message)s',
    level=logging.INFO
)

def inc(r: float, pdf: List):
    cum = 0
    for i, p in enumerate(pdf):
        cum += p
        if r < cum: return i
    return None

def text_source():
    files = [args.file] if args.file else Path(args.dir).rglob('*')
    files = (file for file in files if not os.path.isdir(file))
    for file in files:
        with open(file, 'r') as f:
            try:
                for c in chain.from_iterable(f):
                    if c != '\n':
                        yield c
            except UnicodeDecodeError:
                continue


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.use_default_colors()
    max_y, max_x = stdscr.getmaxyx()
    y = 0
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_BLUE, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)
    for x, char in enumerate(text_source()):
        if y % max_y == max_y - 1 and x % max_x == max_x - 1:
            y -= 1
        if stdscr.getch() == ord('q'):
            return
        logging.debug(f'{x},{y}, {x % max_x}, {y % max_y}, {char}')
        stdscr.addch(y % max_y, x % max_x, char, curses.color_pair(random.randint(1, 3)))
        stdscr.refresh()
        r = random.random()
        y += [-1, 0, 1][inc(r, [0.05, 0.9, 0.05])]
        time.sleep(0.0001)

    logging.info('done')
    while True:
        logging.info('doner')
        if stdscr.getch() == ord('q'):
            return
        time.sleep(0.1)
    logging.info('proper_done')

curses.wrapper(main)
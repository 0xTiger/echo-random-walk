import time
import random
import curses
import argparse
import logging

from typing import List
from pathlib import Path
from itertools import chain

parser = argparse.ArgumentParser()
parser.add_argument('path', 
    help='path of file or directory containing text to display')
parser.add_argument('--log', action='store_true',
    help='enables logging')
parser.add_argument('--speed', default=500, type=int, 
    help='set the display speed in characters per second')
args = parser.parse_args()


fh = logging.FileHandler(filename='echo-random-walk.log', mode='w', delay=True)
fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
fh.setLevel(logging.INFO)
logger = logging.Logger(__file__)
logger.addHandler(fh)
logger.disabled = not args.log

def weighted_choice(pdf: List):
    r = random.random()
    cum = 0
    for i, p in enumerate(pdf):
        cum += p
        if r < cum: return i
    return None


def text_source():
    source_path = Path(args.path)
    paths = [source_path] if source_path.is_file() else source_path.rglob('*')
    paths = (path for path in paths if path.is_file())
    for path in paths:
        with open(path, 'r') as f:
            try:
                for c in chain.from_iterable(f):
                    if c not in '\t\0':
                        yield c
            except UnicodeDecodeError:
                continue


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.use_default_colors()
    max_y, max_x = stdscr.getmaxyx()
    y = max_y // 2
    c = 1
    for i in range(9):
        curses.init_pair(i, i, -1)
    for x, char in enumerate(text_source()):
        if y % max_y == max_y - 1 and x % max_x == max_x - 1:
            y -= 1
        if stdscr.getch() == ord('q'):
            return
        if char == '\n':
            char = ' '
            c += 1
        logger.debug(f'{x},{y}, {x % max_x}, {y % max_y}, {char}')
        stdscr.addch(y % max_y, x % max_x, char, curses.color_pair(c % 9))
        stdscr.refresh()
        y += [-1, 0, 1][weighted_choice([0.05, 0.9, 0.05])]
        time.sleep(1 / args.speed)

    logger.debug('done')
    while True:
        if stdscr.getch() == ord('q'):
            return
        time.sleep(0.1)

curses.wrapper(main)
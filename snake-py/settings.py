import pygame as pg
from pygame.math import Vector2
import sys
import random

# game settings
CELL_SIZE = 40
CELL_NUMBER = 20

# path
HEAD_UP = 'assets/head_up.png'
HEAD_DOWN = 'assets/head_down.png'
HEAD_RIGHT = 'assets/head_right.png'
HEAD_LEFT = 'assets/head_left.png'

TAIL_UP = 'assets/tail_up.png'
TAIL_DOWN = 'assets/tail_down.png'
TAIL_RIGHT = 'assets/tail_right.png'
TAIL_LEFT = 'assets/tail_left.png'

BODY_VER = 'assets/body_vertical.png'
BODY_HOR = 'assets/body_horizontal.png'

BODY_TR = 'assets/body_tr.png'
BODY_TL = 'assets/body_tl.png'
BODY_BR = 'assets/body_br.png'
BODY_BL = 'assets/body_bl.png'

CRUNCH_WAV = 'audio/crunch.wav'

APPLE = 'assets/apple.png'
FONT = 'font/PoetsenOne-Regular.ttf'

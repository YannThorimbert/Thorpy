"""
This module defines constant variables used by the GUI. These variable should
never be modified by user.
Variables defining the style or theme of the GUI can be found in:
    - style.py
    - painterstyle.py
"""
import os

import pygame.event as pygame_event
from pygame.font import get_fonts
from pygame.locals import USEREVENT, QUIT

from thorpy import THORPY_PATH

try:
    import numpy
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import PIL
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

CAN_SHADOWS = HAS_NUMPY and HAS_PIL

# fonts
AVAILABLE_FONTS = sorted(get_fonts())

# pygame events
EVENT_QUIT = pygame_event.Event(QUIT)

THORPY_EVENT = USEREVENT
# events types : these are the ID's of thorpy events.
# A ThorPy event has an attribute ID, and the numbers below are these attributes, not pygame events!!!
EVENT_TIME =   1
EVENT_PRESS =   2  # posted when an element enter state pressed
# posted when sth has been inserted into an Inserter
EVENT_INSERT =   3
EVENT_WHEEL =   4 # posted when mousewheel has been used on an element that handles it
EVENT_SLIDE =   5  # posted when a slider's dragger has been slided
EVENT_DONE =   6  # posted when a "Done" button has been clicked
EVENT_UNPRESS =   7
EVENT_HOVER =   8
EVENT_CANCEL =   9
EVENT_CHANGE_STATE =   10
EVENT_DRAG = 11
EVENT_TOGGLE = 12
EVENT_UNTOGGLE = 13
EVENT_DDL = 14
EVENT_LAUNCH = 15
EVENT_UNLAUNCH = 16

EVENT_NAMES = { EVENT_CANCEL:"EVENT_CANCEL",
                EVENT_CHANGE_STATE:"EVENT_CHANGE_STATE",
                EVENT_DDL:"EVENT_DDL",
                EVENT_DONE:"EVENT_DONE",
                EVENT_DRAG:"EVENT_DRAG",
                EVENT_HOVER:"EVENT_HOVER",
                EVENT_INSERT:"EVENT_INSERT",
                EVENT_LAUNCH:"EVENT_LAUNCH",
                EVENT_PRESS:"EVENT_PRESS",
                EVENT_SLIDE:"EVENT_SLIDE",
                EVENT_TIME:"EVENT_TIME",
                EVENT_TOGGLE:"EVENT_TOGGLE",
                EVENT_UNLAUNCH:"EVENT_UNLAUNCH",
                EVENT_UNPRESS:"EVENT_UNPRESS",
                EVENT_UNTOGGLE:"EVENT_UNTOGGLE",
                EVENT_WHEEL:"EVENT_WHEEL"}

# => post EVENT_PRESS. reacts to parameters.BUTTON_PRESS_EVENT
REAC_PRESSED = 0
# => post EVENT_UNPRESS. reacts to parameters.BUTTON_UNPRESS_EVENT
REAC_UNPRESS = 1
REAC_HOVER = 2  # => post EVENT_HOVER. reacts to pygame.MOUSEMOTION
REAC_TIME = 3  # => post nothing. Usually reacts to EVENT_TIME event
REAC_KEYPRESS = 4  # => post nothing. reacts to parameters.KEY_PRESS_EVENT
REAC_MOTION = 5  # => post nothing. reacts to pygame.MOUSEMOTION
REAC_SLIDER_PRESS = 7
REAC_SLIDER_UNPRESS = 8
REAC_SELECT = 9
REAC_PRESS_DDL = 10
REAC_WHEELUP = 11
REAC_WHEELDOWN = 12
REAC_HELP = 13
REAC_CLICKQUIT = 14
REAC_MOUSE_REPEAT = 15
REAC_PRESSED2 = 16
REAC_SLIDER_PRESS2 = 17
REAC_SLIDER_UNPRESS2 = 18
REAC_RIGHT_CLICK = 19
REAC_CHANGE_STATE = 20
REAC_USER = 100


#for launchers
LAUNCH_CANCEL = 0
LAUNCH_DONE = 1
LAUNCH_CLICK_QUIT = 2

# _states
STATE_NORMAL = 0  # should always stay 0 for compatibility reasons
STATE_PRESSED = 1

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
LIGHTBLUE = (150, 150, 255)
# colors (gray levels)
WHITE = (255, 255, 255)
ULTRABRIGHT = (240, 240, 240)
BRIGHT = (220, 220, 220)
BRAY = (200, 200, 200)
GRAY = (150, 150, 150)
MID = (127, 127, 127)
DARK = (50, 50, 50)
BLACK = (0, 0, 0)
# alphacolors
TRANSPARENT = (0, 0, 0, 0)

# cursors
CURSOR_NORMAL = 0
CURSOR_TEXT = 1
CURSOR_BROKEN = 2
CURSOR_BALL = 3

SYNTAX_BEG = "#SB"
SYNTAX_END = "#SE"
SYNTAX_FIRST = False
SYNTAX_LAST = False

DEFAULT_RANK = 0

##METADATA_PATH = os.path.join(THORPY_PATH, "metadata")
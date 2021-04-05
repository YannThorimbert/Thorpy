"""
This module stores the variables that define the style of the GUI.
Note that the module "painterstyle" also define the default painters.
Default painters are in a separate module because they need to import painters,
and painters need to import style.
"""

import os

from thorpy import THORPY_PATH
from thorpy.miscgui import constants

# Default Texts
OK_TXT = "Ok"
CANCEL_TXT = "Cancel"

# default font (distributed with thorpy) - NOT USED FOR THE MOMENT
DEFAULT_FONT_PATH = os.path.join(THORPY_PATH,"data/Carlito/Carlito-Regular.ttf")

# Default Fonts : the program will try to use the fonts in the order of FONTS
FONTS = ("verdana", "comicsansms", "arial", "timesnewroman",
         "dejavusansserif", "ubuntu", "century")
FONT_SIZE = 12
FONT_COLOR = constants.BLACK
ITALIC = False
BOLD = False
UNDERLINE = False
FONT_AA = True
FONT_BCKGR = None

FONT_SIZE_INCREMENTS = {"bar":0, "title":3, "path":-2}

# Default fonts for titles (bar) texts
BAR_FONTS = ("verdana", "comicsansms", "arial", "timesnewroman",
             "dejavusansserif", "ubuntu", "century")
FONT_BAR_SIZE = 12
FONT_BAR_COLOR = constants.YELLOW
BAR_ITALIC = False
BAR_BOLD = False
BAR_UNDERLINE = False
FONT_BAR_AA = True
FONT_BAR_BCKGR = None

#storage
STORE_MODE = "vertical"
STORE_ALIGN = "center"

MARGINS = (5, 5)
GAPS = (5, 5)
NAME_SPACING = 5  # space between the name and the value

# default element color:
DEF_COLOR = constants.BRAY  # base color
DEF_COLOR2 = constants.ULTRABRIGHT  # color of elements bckgr
DEF_COLOR3 = constants.BRIGHT
DEF_HELP_COLOR = tuple(list(constants.ULTRABRIGHT) + [220])
DARK_FACTOR = 0.5
LIGHT_FACTOR = 1.2
BORDER_FACT = 0.3
DEF_RADIUS = 10
DEF_DARK = constants.DARK

# default colors
COLOR_TXT_HOVER = constants.BLUE  # hover highlight
COLOR_BULK_HOVER = constants.GREEN
COLOR_HOVER_DRAGGER = constants.BRIGHT  # hover highlight for lift draggers
COLOR_HOVER_CHECK = constants.BRIGHT  # hover highlight for check and radio
BAR_COLOR = constants.LIGHTBLUE  # head bar

#title
TITLE_SPACE = 3
TITLE_ALIGN = "left"
CUT_WORD = ".."
TITLE_POS = (0, 0)
TITLE_FONT_SIZE = 15
TITLE_FONT_COLOR = (0, 0, 0)
# default elements size
SIZE = (80, 30)
SMALL_SIZE = (16, 16)
LARGE_SIZE = (150, 30)
XLARGE_SIZE = (250, 30)
Y_SMALL_SIZE = 20
CHECK_SIZE = (14, 14)  # check and radio boxes
FILE_WIDTH = 100  # width for filenames

# box
BOX_SIZE = (250, 150)
BOX_RADIUS = 8

#help
HELP_SIZE = (80, 30)

# slider (also affects lift)
SLIDER_MARGINS = (2, 2)
SLIDER_THICK = 8
SLIDERX_DRAG_SIZE = (8, 20)
SLIDERY_DRAG_SIZE = (20, 8)

# lift
LIFT_DRAG_SIZE = (14, 20)
LIFT_BUTTON_SIZE = (16, 16)
LIFT_MARGINS = (1, 1)
BUTTON_MARGINS = (2, 2)
ARROW_COLOR = constants.BLACK

# dropdown lists
DDL_SIZE = (100, 250)
DDL_MARGINS = (1, 1)
DDL_MAX_SIZE = (200, 250)

# browserlight
BROWSERLIGHT_SIZE = (300, 300)
BROWSERLIGHT_DDL_SIZE = (200, 200)
# only used to determine the size of father
BROWSERLIGHT_STORE_MARGINS = (20, 5)
BROWSERLIGHT_STORE_GAPS = (2, 5)
BROWSERLIGHT_LEFT_SHIFT = 20

# browser
BROWSER_SIZE = (300, 300)
BROWSER_DDL_SIZE = (280, 280)
PATH_FONT_SIZE = 10

# dirviewer
DIRVIEWER_GAP = 5  # gap between lines
DIRVIEWER_X = None  # x margin

# inserter
MAX_INSERTER_WIDTH = 100
CURS_FACT = 0.8
CURS_THICK = 1
CURS_COLOR = constants.BLACK
INSERTWRITER_MARGIN = 2

#Shadow
SHADOW_ALTITUDE = 5

# default images
CHECKBOX_IMG = os.path.join(THORPY_PATH, "data/check_box.bmp")
CHECKBOX_IMG_COLORKEY = (255, 255, 255)
CHECKBOX_SPACE = 4
#for the moment, same colorkey has to be used for checkbox and radio
RADIO_IMG = os.path.join(THORPY_PATH, "data/check_radio.bmp")

ARROW_IMG = os.path.join(THORPY_PATH, "data/arrow.bmp")
ARROW_IMG_COLORKEY = (255, 255, 255)
ARROW_IMG_COLORSOURCE = (0, 0, 0)

FOLDER_IMG = os.path.join(THORPY_PATH, "data/folder.png")
FOLDER_IMG_COLORKEY = (255, 255, 255)

EXAMPLE_IMG = os.path.join(THORPY_PATH, "data/painting.jpg")

DEFAULT_ICON = os.path.join(THORPY_PATH, "data/thorpy_icon.png")

SMOKE_IMG = os.path.join(THORPY_PATH, "data/smoke.png")

HEART_FULL = os.path.join(THORPY_PATH, "data/heart_full.png")
HEART_EMPTY = os.path.join(THORPY_PATH, "data/heart_empty.png")

# default styles
STYLE = "normal"
STYLE_NAME = "text"
STYLE_INSERTER_NAME = "text"
STYLE_CHECKER_NAME = "text"
STYLE_SLIDER_NAME = "text"
STYLE_SLIDER_VALUE = "text"
STYLE_BROWSER_LAUNCHER = "normal"
MAKE_SIZE = "scaled"

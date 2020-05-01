"""
This module define the default painters used to build graphical elements.
"""
from thorpy.painting.writer import Writer
from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.painting.painters.classicframe import ClassicFrame
from thorpy.painting.painters.classicround import ClassicRound
from thorpy.painting.painters.roundrect import RoundRect
from thorpy.painting.painters.optionnal.human import Human, HumanLite
from thorpy.painting.painters.optionnal.rectframe import RectFrame
from thorpy.painting.painters.optionnal.rectframe import Windows10Frame

# default painters
BASIC_PAINTER = BasicFrame
DEF_PAINTER = ClassicFrame
INSERTER_PAINTER = ClassicFrame
INSERTER_NAME_PAINTER = BasicFrame
CHECKER_NAME_PAINTER = BasicFrame
CHECKER_VALUE_PAINTER = BasicFrame
BROWSER_PAINTER = ClassicFrame
BAR_PAINTER = ClassicFrame
CHECKBOX_PAINTER = ClassicFrame
RADIO_PAINTER = ClassicRound
NAME_PAINTER = BasicFrame
BROWSER_LAUNCHER_PAINTER = ClassicFrame
HELP_PAINTER = RoundRect
CURSOR_PAINTER = BasicFrame
BOX_PAINTER = ClassicFrame


painters = {"basic" : BasicFrame,
            "round" : HumanLite,
            "human" : Human,
            "classic" : ClassicFrame,
            "simple" : RectFrame,
            "windows10" : Windows10Frame}

# default writers

WRITER = Writer

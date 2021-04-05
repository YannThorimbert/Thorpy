import sys
from thorpy.miscgui import constants, functions, style, painterstyle

_DEFAULT_STYLE = {}
_DEFAULT_PAINTERSTYLE = {}

def get_current_theme():
    """Returns style and painterstyle variables into dictionnaries."""
    style_dict = sys.modules["thorpy.miscgui.style"].__dict__
    painterstyle_dict = sys.modules["thorpy.miscgui.painterstyle"].__dict__
    style_dict_clean = {}
    painterstyle_dict_clean = {}
    for key, value in iter(style_dict.items()):
        if not key.startswith("_"):
            style_dict_clean[key] = value
    for key, value in iter(painterstyle_dict.items()):
        if not key.startswith("_"):
            painterstyle_dict_clean[key] = value
    return style_dict_clean, painterstyle_dict_clean

def set_current_theme_as_default():
    global _DEFAULT_STYLE, _DEFAULT_PAINTERSTYLE
    style_dict, painterstyle_dict = get_current_theme()
    _DEFAULT_STYLE = style_dict
    _DEFAULT_PAINTERSTYLE = painterstyle_dict

def set_default_theme_as_current():
    """Equivalent to set_theme('default')."""
    if not _DEFAULT_PAINTERSTYLE or not _DEFAULT_STYLE:
        raise Exception("No default theme avalaible.\
                        thorpy.set_default_theme_as_current must be called\
                        first.")
    for key, value in iter(_DEFAULT_STYLE.items()):
        setattr(style, key, value)
    for key, value in (_DEFAULT_PAINTERSTYLE.items()):
        setattr(painterstyle, key, value)

def set_theme(name):
    name = name.lower()
    if name == "default":
        functions.debug_msg("Setting default theme.")
        set_default_theme_as_current()
    elif name == "classic":
        style.MARGINS = (5,5)
        painterstyle.DEF_PAINTER = painterstyle.painters[name]
        painterstyle.INSERTER_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_PAINTER = painterstyle.painters[name]
        painterstyle.BAR_PAINTER = painterstyle.painters[name]
        painterstyle.CHECKBOX_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_LAUNCHER_PAINTER = painterstyle.painters[name]
        painterstyle.BOX_PAINTER = painterstyle.painters[name]
##        style.DARK_FACTOR = 0.75
    elif name == "human":
        style.DARK_FACTOR = 0.8
        style.DEF_COLOR = constants.BRIGHT
        style.DEF_RADIUS = 10
        style.MARGINS = (5,5)
        painterstyle.DEF_PAINTER = painterstyle.painters[name]
        painterstyle.INSERTER_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_PAINTER = painterstyle.painters[name]
        painterstyle.BAR_PAINTER = painterstyle.painters[name]
        painterstyle.CHECKBOX_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_LAUNCHER_PAINTER = painterstyle.painters[name]
        painterstyle.BOX_PAINTER = painterstyle.painters[name]
    elif name == "round":
        style.DARK_FACTOR = 0.8
        style.DEF_COLOR = constants.BRIGHT
        style.DEF_RADIUS = 12
        style.MARGINS = (5,5)
        painterstyle.DEF_PAINTER = painterstyle.painters[name]
        painterstyle.INSERTER_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_PAINTER = painterstyle.painters[name]
        painterstyle.BAR_PAINTER = painterstyle.painters[name]
        painterstyle.CHECKBOX_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_LAUNCHER_PAINTER = painterstyle.painters[name]
        painterstyle.BOX_PAINTER = painterstyle.painters[name]
    elif name == "simple":
        painterstyle.DEF_PAINTER = painterstyle.painters[name]
        painterstyle.INSERTER_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_PAINTER = painterstyle.painters[name]
        painterstyle.BAR_PAINTER = painterstyle.painters[name]
        painterstyle.CHECKBOX_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_LAUNCHER_PAINTER = painterstyle.painters[name]
        painterstyle.BOX_PAINTER = painterstyle.painters[name]
        style.LIGHT_FACTOR = 1.1
        style.DARK_FACTOR = 0.9
        style.MARGINS = (5,5)
    elif name == "windows10":
        painterstyle.DEF_PAINTER = painterstyle.painters[name]
        painterstyle.INSERTER_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_PAINTER = painterstyle.painters[name]
        painterstyle.BAR_PAINTER = painterstyle.painters[name]
        painterstyle.CHECKBOX_PAINTER = painterstyle.painters[name]
        painterstyle.BROWSER_LAUNCHER_PAINTER = painterstyle.painters[name]
        painterstyle.BOX_PAINTER = painterstyle.painters[name]
        style.DEF_COLOR = (100,100,255)
        style.COLOR_TXT_HOVER = style.FONT_COLOR
        style.LIGHT_FACTOR = 1.1
        style.DARK_FACTOR = 0.9
        style.MARGINS = (5,5)

def increment_font_sizes(incr):
    functions.debug_msg("Incrementing font sizes")
    style.FONT_SIZE += incr
    style.FONT_BAR_SIZE += incr
    style.TITLE_FONT_SIZE += incr
    style.PATH_FONT_SIZE += incr

def set_font_sizes(size, increments=None):
    if increments is None: increments = style.FONT_SIZE_INCREMENTS
    style.FONT_SIZE = size
    style.FONT_BAR_SIZE = size + increments["bar"]
    style.TITLE_FONT_SIZE = size + increments["title"]
    style.PATH_FONT_SIZE = size + increments["path"]

def add_font(fontname):
    functions.debug_msg("Adding font", fontname)
    newlist = [fontname]+list(style.FONTS)
    style.FONTS = tuple(newlist)

set_current_theme_as_default()

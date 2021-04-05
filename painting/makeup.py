"""This module provides functions to add graphical effects on elements."""

from thorpy.elements._makeuputils._shadow import StaticShadow
from thorpy.elements.hoverzone import HoverZone
from thorpy.miscgui import style
from thorpy.painting.painters.imageframe import ImageFrame

def add_static_shadow(element, dict_args=None):
    """Adds a static shadow to <element>. This means that the shadow is always
    the same, regardless of the state of the element.
    """
    shadowel = StaticShadow(element)
    if dict_args:
        for key, value in iter(dict_args.items()):
            setattr(shadowel, key, value)
    shadowel.finish()

def add_button_shadow(element, altitude=None, dict_args=None):
    altitude = style.SHADOW_ALTITUDE if altitude is None else altitude
    shadow = StaticShadow(element)
    shadow.target_altitude = altitude
    shadow.vertical = False
    shadow.sun_angle2 = 45.
    shadow.alpha_factor = 0.5
    if dict_args:
        for key, value in (dict_args.items()):
            setattr(shadowel, key, value)
    shadow.finish()

def remove_shadow(element):
    element._shadow.unlink()

def add_basic_help(element, text, wait_time=None, jail=None, shadow=False,
                    rect=None):
    if rect is None:
        rect = element.get_help_rect()
    hoverzone = HoverZone(rect)
    hoverzone.finish()
    element.add_elements([hoverzone])
    hoverzone.add_basic_help(text, wait_time, jail)
    if shadow:
        add_button_shadow(hoverzone._help_element)
        hoverzone._help_element._shadow.visible = False
    return hoverzone

##def set_image_normal(element, image):
##    painter = ImageFrame(image)
##    fusionner =
##
##def set_image_pressed(element, image):
##    pass
##
##def set_image_hover(element, image):
##    pass
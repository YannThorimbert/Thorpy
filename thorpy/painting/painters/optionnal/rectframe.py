from pygame.draw import rect as draw_rect
from pygame import Rect

from thorpy.painting.painters.basicframe import BasicFrame
from thorpy._utils.colorscomputing import normalize_color, grow_color
from thorpy.miscgui import style


class RectFrame(BasicFrame):

    def __init__(self, size=None, color=None, clip="auto",
                 dark=None, light=None, thick=2, pressed=False, hover=False):
        if size is None: size=style.SIZE
        if color is None: color=style.DEF_COLOR
        if clip is "auto":
            inflation = -2 * thick
            clip = (inflation, inflation)
        BasicFrame.__init__(self,
                            size=size,
                            color=color,
                            clip=clip,
                            pressed=pressed,
                            hovered=hover)
        self.light = style.LIGHT_FACTOR if light is None else light
        self.dark = style.DARK_FACTOR if dark is None else dark
        if isinstance(self.light, float):
            self.light = normalize_color(grow_color(self.light, self.color))
        if isinstance(self.dark, float):
            self.dark = normalize_color(grow_color(self.dark, self.color))
        self.thick = thick

    def draw(self):
        surface = BasicFrame.draw(self)
        if not self.pressed:
            draw_rect(surface, self.dark, Rect((0, 0), self.size), self.thick)
        else:
            draw_rect(surface, self.light, Rect((0, 0), self.size), self.thick)
        return surface

    def get_surface(self):
        surface = self.draw()
        surface.set_clip(self.clip)
        return surface

class Windows10Frame(RectFrame):
    def __init__(self, size=None, color=None, clip="auto", dark=(20,20,20),
                            light=None, thick=3, pressed=False, hover=False):
        RectFrame.__init__(self, size, color, clip, dark, light, thick, pressed, hover)

    def draw(self):
        surface = BasicFrame.draw(self)
        if self.pressed:
            draw_rect(surface, self.dark, Rect((0, 0), self.size), self.thick+2)
        elif self.hovered:
            draw_rect(surface, self.dark, Rect((0, 0), self.size), self.thick)
        return surface


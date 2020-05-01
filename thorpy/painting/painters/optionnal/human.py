from pygame import BLEND_RGBA_MIN
from pygame import Surface

from thorpy._utils.colorscomputing import grow_color, normalize_color
from thorpy.painting.painters.roundrect import RoundRect
from thorpy.painting.painters.classicframe import ClassicFrame
from thorpy.painting.graphics import linear_v_monogradation
from thorpy.miscgui import style


class Human(ClassicFrame):

    def __init__(self, size=None, color=None, clip="auto", radius_ext=None,
                 radius_int=None, pressed=False, dark=None, light=None, thick=1,
                 hovered=False, border_color=None): #changer border
        """If radius is in the range [0, 1], self.radius_value is the fraction
        of radius * min(size), else it is interpreted as a raw pixel value.
        """
        if clip == "auto":
            inflation = -2 * thick
            clip = (inflation, inflation)
        ClassicFrame.__init__(self,
                              size=size,
                              color=color,
                              pressed=pressed,
                              hovered=hovered,
                              dark=dark,
                              light=light,
                              thick=thick,
                              clip=clip)
        radius_value = style.DEF_RADIUS if radius_ext is None else radius_ext
        if 0. <= radius_value <= 1.:
            radius_value = min(self.size) * radius_value
        self.radius_ext = radius_value
        self.radius_int = radius_int
        if radius_int == None:
            self.radius_int = self.radius_ext - self.thick

        self.border_color = style.BORDER_FACT if border_color is None else border_color
        if isinstance(self.border_color, float):
            self.border_color = normalize_color(grow_color(self.border_color,
                                                           self.color))

    def draw(self):
        if self.hovered:
            exterior = RoundRect(self.size, style.COLOR_BULK_HOVER, self.clip,
                                 self.radius_ext)
        else:
            exterior = RoundRect(self.size, self.border_color, self.clip,
                                 self.radius_ext)
        w, h = (self.size[0] - 2*self.thick, self.size[1] - 2*self.thick)
        w = 0 if w < 0 else w
        h = 0 if h < 0 else h
        int_size = (w, h)
        if self.pressed:
            interior = RoundRect(int_size, self.color, self.clip, self.radius_int)
        else:
            interior = RoundRect(int_size, self.light, self.clip, self.radius_int)
        sext = exterior.draw()
        sint = interior.draw()
        degrad = Surface(int_size)
        if self.pressed:
            linear_v_monogradation(degrad, 0, int(h), self.color, self.dark)
            sint.blit(degrad, (0, 0), special_flags=BLEND_RGBA_MIN)
        else:
            linear_v_monogradation(degrad, 0, int(h), self.dark, self.color)
            sint.blit(degrad, (0, 0), special_flags=BLEND_RGBA_MIN)
        sext.blit(sint, (self.thick, self.thick))
        return sext

    def set_color(self, color):
        ClassicFrame.set_color(self, color)
        if len(color) == 4:
            self.border_color = tuple(list(self.border_color) + [color[3]])

class HumanLite(Human):

    def draw(self):
        if self.hovered:
            exterior = RoundRect(self.size, style.COLOR_BULK_HOVER, self.clip,
                                 self.radius_ext)
        else:
            exterior = RoundRect(self.size, self.border_color, self.clip,
                                 self.radius_ext)
        w, h = (self.size[0] - 2*self.thick, self.size[1] - 2*self.thick)
        w = 0 if w < 0 else w
        h = 0 if h < 0 else h
        int_size = (w, h)
        if self.pressed:
            interior = RoundRect(int_size, self.color, self.clip, self.radius_int)
        else:
            interior = RoundRect(int_size, self.light, self.clip, self.radius_int)
        sext = exterior.draw()
        sint = interior.draw()
        degrad = Surface(int_size)
        if self.pressed:
            degrad.fill(self.dark)
            sint.blit(degrad, (0, 0), special_flags=BLEND_RGBA_MIN)
        else:
            degrad.fill(self.color)
            sint.blit(degrad, (0, 0), special_flags=BLEND_RGBA_MIN)
        sext.blit(sint, (self.thick, self.thick))
        return sext
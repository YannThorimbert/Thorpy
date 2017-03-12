from __future__ import division

from pygame import Surface
from pygame.constants import SRCALPHA
from pygame.gfxdraw import arc as arc  # to change if pygame changes
# to change if pygame changes:
from pygame.gfxdraw import filled_circle as filled_circle

from thorpy._utils.colorscomputing import mid_color, make_compatible
from thorpy.painting.painters.painter import Painter
from thorpy.miscgui import constants, style


class ClassicRound(Painter):

    def __init__(self, size=None, color=None, pressed=False, dark=None,
                 hovered=False, light=None, thick=1, clip=None):
        """Size : diameter"""
        size = style.CHECK_SIZE if size is None else size
        color = style.DEF_COLOR2 if color is None else color
        Painter.__init__(self, size=size, clip=clip, pressed=pressed,
                         hovered=hovered)
        self.color = color
        self.dark = dark
        self.light = light
        self.thick = thick

    def blit_borders_on(self, surface):
        if not self.light:
            white = make_compatible(constants.WHITE, self.color)
            self.light = mid_color(self.color, white)
        if not self.dark:
            black = make_compatible(constants.BLACK, self.color)
            self.dark = mid_color(self.color, black)
##        rect = Rect((0, 0), self.size)
        x = y = r = self.size[0] // 2
        r -= 2
        filled_circle(surface, x, y, r, self.color)
##        circle(surface, x, y, r,  self.dark)
        arc(surface, x, y, r, 135, 135 + 180, self.dark)
        arc(surface, x, y, r, 135 + 180, 135 + 360, self.light)

    def draw(self):
        surface = Surface(self.size, flags=SRCALPHA).convert_alpha()
        surface.fill(constants.TRANSPARENT)
        self.blit_borders_on(surface)
        return surface

    def get_surface(self):
        surface = self.draw()
        surface.set_clip(self.clip)
        return surface

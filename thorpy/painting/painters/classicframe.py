from pygame import Rect
from pygame.draw import lines

from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui import style
from thorpy._utils.rectscomputing import get_top_coords, get_bottom_coords
from thorpy._utils.colorscomputing import grow_color, normalize_color


class ClassicFrame(BasicFrame):

    def __init__(self, size=None, color=None, pressed=False, dark=None,
                 hovered=False, light=None, thick=1, clip="auto"):
        if clip == "auto":
            inflation = -2 * thick
            clip = (inflation, inflation)
        BasicFrame.__init__(self,
                            size=size,
                            color=color,
                            clip=clip,
                            pressed=pressed,
                            hovered=hovered)
        self.dark = dark
        self.light = light
        self.thick = thick
        self.light = style.LIGHT_FACTOR if light is None else light
        self.dark = style.DARK_FACTOR if dark is None else dark
##        if self.light is None:
##            white = make_compatible(constants.WHITE, self.color)
##            self.light = mid_color(self.color, white)
        if isinstance(self.light, float):
            self.light = normalize_color(grow_color(self.light, self.color))
##        if self.dark is None:
##            black = make_compatible(constants.BLACK, self.color)
##            self.dark = mid_color(self.color, black)
        if isinstance(self.dark, float):
            self.dark = normalize_color(grow_color(self.dark, self.color))

    def blit_borders_on(self, surface):
        rect = Rect((0, 0), self.size)
        for x in range(0, self.thick):
            r = rect.inflate(-x, -x)
            tc = get_top_coords(r)
            bc = get_bottom_coords(r)
            if self.pressed:
                lines(surface, self.dark, False, tc, 1)
                lines(surface, self.light, False, bc, 1)
            else:
                lines(surface, self.light, False, tc, 1)
                lines(surface, self.dark, False, bc, 1)

    def draw(self):
        surface = BasicFrame.draw(self)
        self.blit_borders_on(surface)
        return surface

    def get_fusion(self, title, center_title):
        """Fusion the painter.img and the title.img and returns this fusion"""
        if self.pressed:
            if center_title is True:  # center the title on the element rect
                title.center_on(self.size)
                title._pos = (title._pos[0], title._pos[1] + self.thick)
            # center_title is the topleft argument
            elif center_title is not False:
                title._pos = center_title
            else:
                title._pos = (0, 0)
            painter_img = self.get_surface()
            title.blit_on(painter_img)
            return painter_img
        else:
            return BasicFrame.get_fusion(self, title, center_title)

    def set_color(self, color):
        self.color = color
        if len(color) == 4:
            self.dark = tuple(list(self.dark) + [color[3]])
            self.light = tuple(list(self.light) + [color[3]])

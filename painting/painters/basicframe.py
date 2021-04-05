from pygame import Surface, SRCALPHA

from thorpy.miscgui.functions import debug_msg
from thorpy.miscgui import style
from thorpy.painting.painters.painter import Painter

class BasicFrame(Painter):
    # get_fusion()
        # get_surface()
            # draw()
                # personnals...

    def __init__(self, size=None, color=None, pressed=False, hovered=False,
                 clip=None):
        color = style.DEF_COLOR if color is None else color
        Painter.__init__(self, size=size, clip=clip, pressed=pressed,
                         hovered=hovered)
        self.color = color

    def draw(self):
        if len(self.color) == 3 or self.color[-1] == 255:
            if self.size[0] < 1:
                debug_msg("Width < 1, automatic resize.", self)
                self.size = (1, self.size[1])
            if self.size[1] < 1:
                debug_msg("Height < 1, automatic resize.", self)
                self.size = (self.size[0], 1)
            surface = Surface(self.size).convert()
        elif len(self.color) == 4:
            surface = Surface(self.size, flags=SRCALPHA).convert_alpha()
        else:
            raise Exception("Invalid color attribut")
        surface.fill(self.color)
        return surface

    def get_surface(self):
        surface = self.draw()
        surface.set_clip(self.clip)
        return surface
from pygame import Surface, Rect, SRCALPHA

from thorpy.painting.painters.classicframe import ClassicFrame
from thorpy.miscgui import style

# get_fusion()
# get_surface()
# draw()
# personnals...


class InserterFrame(ClassicFrame):

    def __init__(self, size=None, color=None, pressed=False, space=8, dark=None,
                 light=None, thick=1, clip="auto"):
        size = style.XLARGE_SIZE if size is None else size
        color = style.DEF_COLOR2 if color is None else color
        ClassicFrame.__init__(self,
                              size=size,
                              color=color,
                              pressed=pressed,
                              hovered=hovered,
                              dark=dark,
                              light=light,
                              thick=thick,
                              clip=clip)
        self.space = space
        self.txt_zone = None

    def get_fusion(self, title, center_title=None, hover=False):
        """Fusion the painter.img and the title.img and returns this fusion.
        center_title is ignored."""
        title.center_on(self.size)
        title._pos = (0, title._pos[1])
        title_length = title.img.get_size()[0]
        painter_img = self.get_surface(title_length)
##        painter_img.blit(title.img, title._pos)
        title.blit_on(painter_img)
        return painter_img

    def get_surface(self, title_length):
        surface = self.draw(title_length)
        surface.set_clip(self.clip)
        return surface

    def draw(self, title_length):
        # actual surface (transparent):
        surface = Surface(self.size, flags=SRCALPHA).convert_alpha()
        surface.fill((0, 0, 0, 0))
        # computing frame length: tot = title + space + frame
        frame_length = self.size[0] - title_length - self.space
        frame_size = (frame_length, self.size[1])
        self.txt_zone = Rect((title_length + self.space, 0), frame_size)
        frame_painter = ClassicFrame(frame_size, self.color, True, self.dark,
                                     self.light, self.thick)
        # frame in which text will be inserted:
        frame = frame_painter.get_surface()
        surface.blit(frame, (title_length + self.space, 0))
        return surface

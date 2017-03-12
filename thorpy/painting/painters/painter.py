from pygame.rect import Rect

from thorpy.miscgui import style
from thorpy.miscgui.functions import debug_msg


class Painter(object):
    """Mother class for all painters. Not to be instanciated.
    Any Painter must have the following attributes:
        - size (a 2-tuple)
        - clip, can either be:
            1) a couple : (a, b) with a and b the x and y values for the
            inflation of the surface's size. E.g, (-3, -3).

            2) a 4-uple : (a, b, c, d) with a and b the topleft of the rect and
            c and d its size. It creates a pygame.Rect to be used for the
            clipping of the surface.

            3) else : no clip will be used.
        - pressed : boolean
        - hovered : boolean
        """

    def __init__(self, size=None, clip=None, pressed=False, hovered=False):
        size = style.SIZE if size is None else size
        w, h = size
        w = int(w)
        h = int(h)
        if w < 0:
            w = 0
            debug_msg("Painter width was negative. Set to 0.")
        if h < 0:
            h = 0
            debug_msg("Painter height was negative. Set to 0.")
        self.size = (w, h)
        self.clip = self.treat_clip(clip)
        self.original_clip = clip
        self.pressed = pressed
        self.hovered = hovered

    def set_size(self, size):
        self.size = size

    def treat_clip(self, clip):
        """
        Get <clip> as argument and returns a Rect suitable for use with pygame
        surface's set_clip method.

        <clip> can either be:
            1) a couple : (a, b) with a and b the x and y values for the
            inflation of the surface's size. E.g, (-3, -3).

            2) a 4-uple : (a, b, c, d) with a and b the topleft of the rect and
            c and d its size. It creates a pygame.Rect to be used for the
            clipping of the surface.

            3) else : no clip will be used.
        """
        if clip:
            if len(clip) == 2:  # then <clip> is the inflation of the rect
                return Rect((0, 0), self.size).inflate(clip)
            # then <clip> is the topleft, size args of the rect
            elif len(clip) == 4:
                return Rect(clip[0], clip[1], clip[2], clip[3])
        return None  # then <clip> is the whole frame

    def set_clip(self, new_clip):
        self.clip = self.treat_clip(new_clip)

    def get_clip(self):
        return self.clip

    def refresh_clip(self):
        self.clip = self.treat_clip(self.original_clip)
        if self.clip and len(self.original_clip) == 4:
            debug_msg("Attention : painter is refreshing, but original clip is\
                        not an inflation or 'None'.")

    def get_surface(self):
        pass

    def get_fusion(self, title, center_title):
        """Fusion the painter.img and the title.img and returns this fusion"""
        if center_title is True:  # center the title on the element rect
            title.center_on(self.size)
        elif center_title is not False:  # center_title is the topleft argument
            title._pos = center_title
        else:
            title._pos = (0, 0)
        painter_img = self.get_surface()
##        painter_img.blit(title.img, title._pos)
        title.blit_on(painter_img)
        return painter_img

    def set_color(self, color):
        self.color = color

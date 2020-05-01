from pygame import RLEACCEL, Surface
from pygame.transform import scale

from thorpy._utils.images import load_image
from thorpy.painting.painters.painter import Painter
from thorpy.miscgui import functions


class ImageFrame(Painter):

    def __init__(self, img_path, alpha=255, colorkey=None, clip=None,
                 pressed=False, mode=None, hovered=False,
                 force_convert_alpha=False):
        self.alpha = alpha
        self.img_path = img_path
        self.colorkey = colorkey
        self.mode = mode
        self.force_convert_alpha = force_convert_alpha
        size = list(self.init_get_img().get_size())
        W, H = functions.get_screen_size()
        if self.mode == "cut":
            if W < size[0]:
                size[0] = W
            if H < size[1]:
                size[1] = H
        Painter.__init__(self, size=size, clip=clip, pressed=pressed,
                         hovered=hovered)
        self._resized = False

    def set_size(self, size):
        # define a way to resize (deform or cut)
        # refresh self.size
        W, H = functions.get_screen_size()
        if self.mode == "cut":
            if W < size[0]:
                size[0] = W
            if H < size[1]:
                size[1] = H
        Painter.set_size(self, size)
        self._resized = size


    def init_get_img(self):
        """Only to find size of image during initialization."""
        if isinstance(self.img_path, str):
            return load_image(self.img_path, colorkey=self.colorkey,
                                use_img_dict=False)
        elif isinstance(self.img_path, Surface):
            return self.img_path
        else:
            raise Exception(type(self.img_path), self.img_path)

    def get_image(self):
        if isinstance(self.img_path, str):  # load image
            surface = load_image(self.img_path)
        else:  # take image
            surface = self.img_path
        if self.force_convert_alpha:
            return surface.convert_alpha()
        return surface

    def get_surface(self):
        W, H = functions.get_screen_size()
        surface = self.get_image()
        if 0 < self.alpha < 255:
            surface.set_alpha(self.alpha, RLEACCEL)
        if self.mode == "scale to screen":
            surface = scale(surface, (W, H))
            self.size = (W, H)
        elif self.mode == "cut to screen":
            new_surface = Surface((W, H))
            new_surface.blit(surface, (0, 0))
            self.size = (W, H)
        elif self._resized:
            surface = scale(surface, self._resized)
        elif self.mode:
            functions.debug_msg("Unrecognized mode : ", self.mode)
        if self.colorkey:
            surface.set_colorkey(self.colorkey, RLEACCEL)
        surface.set_clip(self.clip)
        if self.alpha < 255 or self.force_convert_alpha:
            return surface.convert_alpha()
        else:
            return surface.convert()


class ImageButton(ImageFrame):

    def __init__(self, img_normal, img_pressed=None, img_hover=None, alpha=255,
                 colorkey=None, clip=None, pressed=False, mode=None,
                 hovered=False, force_convert_alpha=False):
        ImageFrame.__init__(self, img_normal, alpha, colorkey, clip, pressed,
                            mode, hovered, force_convert_alpha)
        img_pressed = img_normal if not img_pressed else img_pressed
        img_hover = img_normal if not img_hover else img_hover
        self.img_pressed = img_pressed
        self.img_hover = img_hover

    def get_image(self):
        if self.pressed:
            if isinstance(self.img_pressed, str):  # load image
                surface = load_image(self.img_pressed)
            else:  # take image
                surface = self.img_pressed
        elif self.hovered:
            if isinstance(self.img_hover, str):  # load image
                surface = load_image(self.img_hover)
            else:  # take image
                surface = self.img_hover
        else:
            surface = ImageFrame.get_image(self)
        return surface

class ImageButtonFrame(ImageButton):

    def __init__(self, painter, img_normal, img_pressed=None, img_hover=None, alpha=255,
                 colorkey=None, clip=None, pressed=False, mode=None,
                 hovered=False):
        ImageFrame.__init__(self, img_normal, alpha, colorkey, clip, pressed,
                            mode, hovered)
        img_pressed = img_normal if not img_pressed else img_pressed
        img_hover = img_normal if not img_hover else img_hover
        self.img_pressed = img_pressed
        self.img_hover = img_hover
        self.painter = painter

    def get_image(self):
        if self.pressed:
            if isinstance(self.img_pressed, str):  # load image
                img = load_image(self.img_pressed)
            else:  # take image
                img = self.img_pressed
        elif self.hovered:
            if isinstance(self.img_hover, str):  # load image
                img = load_image(self.img_hover)
            else:  # take image
                img = self.img_hover
        else:
            img = ImageFrame.get_image(self)
        #
        self.painter.pressed = self.pressed
        surface = self.painter.get_image()
        r = img.get_rect()
        r.center = surface.get_rect().center
        surface.blit(img, r.topleft)
        return surface

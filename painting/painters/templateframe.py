from pygame import RLEACCEL, Surface
from pygame.transform import rotate, flip

from thorpy._utils.images import load_image
from thorpy.painting.painters.painter import Painter

class TemplateFrame(Painter):

    def __init__(self, topleft_path, top_path, size, alpha=255, colorkey=None,
                 clip=None, pressed=False, mode="flip", hovered=False):
        self.alpha = alpha
        self.colorkey = colorkey
        self.mode = mode
        self.topleft_img = load_image(topleft_path)
        self.top_img = load_image(top_path)
        size = self.find_size(size)
        Painter.__init__(self, size=size, clip=clip, pressed=pressed,
                         hovered=hovered)

    def find_size(self, size):
        return size

    def blit_templates(self, surface):
        x = 0
        y = 0
        #not memory nor performance efficient, but clear:
        if self.mode == "flip":
            corners = {"topleft" : self.topleft_img,
                       "bottomleft" : flip(self.topleft_img, False, True),
                       "bottomright" : flip(self.topleft_img, True, True),
                       "topright" : flip(self.topleft_img, True, False)}
            sides = {"top" : self.top_img,
                     "left" : rotate(self.top_img, 90),
                     "bottom" : rotate(self.top_img, 180),
                     "right" : rotate(self.top_img, 270)}
        elif self.mode == "rotate":
            corners = {"topleft" : self.topleft_img,
                       "bottomleft" : rotate(self.topleft_img, 90),
                       "bottomright" : rotate(self.topleft_img, 180),
                       "topright" : rotate(self.topleft_img, 270)}
            sides = {"top" : self.top_img,
                     "left" : rotate(self.top_img, 90),
                     "bottom" : rotate(self.top_img, 180),
                     "right" : rotate(self.top_img, 270)}
        cornsize = {key : value.get_size() for key, value in iter(corners.items())}
        sidsize = {key : value.get_size() for key, value in iter(sides.items())}
        #Blitting Sides
        nx = (self.size[0] - cornsize["topleft"][0] - cornsize["topright"][0])\
                                                         // sidsize["top"][0]
        ny = (self.size[1] - cornsize["topleft"][1] - cornsize["bottomleft"][1])\
                                                         // sidsize["left"][1]
        endx = nx*sidsize["top"][0] + cornsize["topleft"][0]
        endy = ny*sidsize["left"][1] + cornsize["topleft"][1]
        sizex = endx + cornsize["topright"][0]
        sizey = endy + cornsize["bottomleft"][1]
        self.size = (sizex, sizey)
        for i in range(nx):
            x = i*sidsize["top"][0] + cornsize["topleft"][0]
            surface.blit(sides["top"], (x, 0))
            x = i*sidsize["bottom"][0] + cornsize["bottomleft"][0]
            surface.blit(sides["bottom"], (x, sizey - sidsize["bottom"][1]))
        for i in range(ny):
            y = i*sidsize["left"][1] + cornsize["topleft"][1]
            surface.blit(sides["left"], (0, y))
            y = i*sidsize["right"][1] + cornsize["topright"][1]
            surface.blit(sides["right"], (sizex - sidsize["right"][0], y))
        #Blitting corners
        surface.blit(corners["topleft"], (0, 0))
        surface.blit(corners["bottomleft"], (0, endy))
        surface.blit(corners["bottomright"], (endx, endy))
        surface.blit(corners["topright"], (endx, 0))

    def set_size(self):
        # define a way to resize (deform or cut)
        # refresh self.size
        pass

    def get_surface(self):
        surface = Surface(self.size)
        if self.colorkey:
            surface.fill(self.colorkey)
        if 0 < self.alpha < 255:
            surface.set_alpha(self.alpha, RLEACCEL)
        self.blit_templates(surface)
##        self.blit_corners(surface)
##        self.blit_sides(surface)
        surface.set_colorkey(self.colorkey, RLEACCEL)
        surface.set_clip(self.clip)
        return surface.convert()

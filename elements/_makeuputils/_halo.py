from pygame import Surface

from thorpy.elements.element import Element
from thorpy.painting import pilgraphics
from thorpy.painting.painters.imageframe import ImageFrame
from thorpy.miscgui import constants


SHADOW_RADIUS = 10
BLACK = 255
ALPHA_FACTOR = 0.85
DECAY_MODE = "linear"
CAPTURE_STATE_STATIC = constants.STATE_NORMAL
OFFSET = (0., 0.)

class Halo(Element):
    def __init__(self, target, color, elements=None, normal_params=None):
        Element.__init__(self, "", elements, normal_params)
        self.link(target)
        self.shadow_radius = SHADOW_RADIUS
        self.black = BLACK
        self.alpha_factor = ALPHA_FACTOR
        self.decay_mode = DECAY_MODE
        self.capture_state = CAPTURE_STATE_STATIC
        self.offset = OFFSET
        self.color = color

    def link(self, target):
        self.target = target
        self.target.add_elements([self])
##        self.target.set_blit_before(self)
        self.target._halo = self

    def unlink(self):
        self.target.remove_elements([self])
        self.target._halo = None
        self.target = None

    def _get_raw_shadow(self):
        target_img = self.target.get_image(self.capture_state)
        r = target_img.get_rect()
        #the shadow will be larger in order to make free space for fadeout.
        r.inflate_ip(2*self.shadow_radius, 2*self.shadow_radius)
        img = Surface(r.size)
        img.fill((255, 255, 255, 255))
        img.blit(target_img, (self.shadow_radius, self.shadow_radius))
        shadow = pilgraphics.get_shadow(img,
                                        radius=self.shadow_radius,
                                        black=self.black,
                                        alpha_factor=self.alpha_factor,
                                        decay_mode=self.decay_mode,
                                        color=self.color)
        return shadow

    def _get_shadow_painter(self):
        shadow = self._get_raw_shadow()
        return ImageFrame(shadow, alpha=-1)

    def _refresh_position(self):
        self.center(element=self.target)

    def finish(self):
        painter = self._get_shadow_painter()
        self.set_painter(painter)
        Element.finish(self)
        self._refresh_position()
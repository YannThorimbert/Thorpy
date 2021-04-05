from math import tan, pi

from pygame import Surface
from pygame.transform import rotate, flip, scale

from thorpy.elements.element import Element
from thorpy.painting import pilgraphics
from thorpy.painting.painters.imageframe import ImageFrame
from thorpy.miscgui import constants, functions
from thorpy.miscgui.reaction import ConstantReaction


SUN_ANGLE = 30.
SUN_ANGLE2 = 0.
SHADOW_RADIUS = 7
SHADOW_COLOR = (0, 0, 0)
BLACK = 255
ALPHA_FACTOR = 0.85
DECAY_MODE = "exponential"
ANGLE_MODE = "flip"
MODE_VALUE = (False, True)
##ANGLE_MODE = "rotate"
##MODE_VALUE = 90.
CAPTURE_STATE_STATIC = constants.STATE_NORMAL
TARGET_ALTITUDE = 0.
OFFSET = (0., 0.)
VERTICAL = True


class StaticShadow(Element):

    def __init__(self, target, elements=None, normal_params=None):
        Element.__init__(self, "", elements, normal_params, finish=False)
        self.target = None
        self.link(target)
        self.sun_angle = SUN_ANGLE
        self.sun_angle2 = SUN_ANGLE2
        self.shadow_radius = SHADOW_RADIUS
        self.black = BLACK
        self.alpha_factor = ALPHA_FACTOR
        self.decay_mode = DECAY_MODE
        self.angle_mode = ANGLE_MODE
        self.mode_value = MODE_VALUE
        self.capture_state = CAPTURE_STATE_STATIC
        self.target_altitude = TARGET_ALTITUDE
        self.offset = OFFSET
        self.vertical = VERTICAL #rpg style : vertical=True
        self.color = SHADOW_COLOR

    def link(self, target):
        self.target = target
        self.target.add_elements([self])
        self.target.set_blit_before(self)
        self.target._shadow = self
        self.target._overframe = True
        if self.target._jail:
            self.set_jailed(self.target._jail)

    def unlink(self):
        self.target.remove_elements([self])
        self.target._shadow = None
        self.target._overframe = False
        self.target = None

    def _get_raw_shadow(self):
        target_img = self.target.get_image(self.capture_state)
        r = target_img.get_rect()
        #the shadow will be larger in order to make free space for fadeout.
        r.inflate_ip(2*self.shadow_radius, 2*self.shadow_radius)
        img = Surface(r.size)
        img.fill((255, 255, 255, 255))
        img.blit(target_img, (self.shadow_radius, self.shadow_radius))
        if self.sun_angle <= 0.:
            raise Exception("Sun angle must be greater than zero.")
        elif self.sun_angle != 45. and self.vertical:
            w, h = img.get_size()
            new_h = h / tan(self.sun_angle * pi / 180.)
            screen_size = functions.get_screen().get_size()
            new_h = abs(int(min(new_h, max(screen_size))))
            img = scale(img, (w, new_h))
        if self.angle_mode == "flip":
            img = flip(img, self.mode_value[0], self.mode_value[1])
        elif self.angle_mode == "rotate":
            img = rotate(img, self.mode_value)
        else:
            raise Exception("angle_mode not available: " + str(self.angle_mode))
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
        if self.vertical:
            if self.angle_mode == "flip":
                targ_rect = self.target.get_fus_rect()
                self_rect = self.get_fus_rect().inflate((-2*self.shadow_radius,
                                                         -2*self.shadow_radius))
##                altitude = self.target_altitude / tan(self.sun_angle*pi / 180.)
                if self.mode_value[1]: #inverted shadow (to the south)
                    self_rect.top = targ_rect.bottom
                else: #to the north
                    self_rect.bottom = targ_rect.bottom
                self.set_center((targ_rect.centerx+self.offset[0],
                                 self_rect.centery+self.offset[1]))
                if self.sun_angle2 != 0.:
                    functions.info_msg("Sun angle2 unused for ", self)
            else:
                self.move(self.offset)
        else:
            dx = 0.
            if self.sun_angle2 > 0.:
                dx = self.target_altitude / tan(self.sun_angle2*pi / 180.)
            dy = self.target_altitude / tan(self.sun_angle*pi / 180.)
            self.move((self.offset[0] + dx, self.offset[1] + dy))


    def finish(self):
        painter = self._get_shadow_painter()
        self.set_painter(painter)
        Element.finish(self)
        self._refresh_position()


class DynamicShadow(StaticShadow):

    def __init__(self, target, elements=None, normal_params=None,
                 capture_states=None):
        StaticShadow.__init__(self, target, elements, normal_params)
        if capture_states is None:
            capture_states = target._states.keys()
##            capture_states = [CAPTURE_STATE_STATIC]
        self._capture_states = capture_states
        self._shadows = {}
        self.offsets = {s : (0., 0.) for s in self._capture_states}
        reaction = ConstantReaction(constants.THORPY_EVENT,
                                    self._reaction_change_state,
                                    {"id":constants.EVENT_CHANGE_STATE,
                                     "el" : self.target},
                                    reac_name=constants.REAC_CHANGE_STATE)
        self.add_reaction(reaction)

    def set_offset(self, offset, state=None):
        if state is None:
            for s in self._capture_states:
                self.set_offset(offset, s)
        self.offsets[state] = offset

    def set_shadow_image(self, state, image, offset=None):
        self._shadows[state] = image
        if self.offset is not None:
            self.offsets[state] = offset

    def finish(self):
        for state_key in self._capture_states:
            self.capture_state = state_key
            self.offset = self.offsets[state_key]
            painter = self._get_shadow_painter()
            self.build_state(state_key, painter)
        self.current_state = self._states[constants.STATE_NORMAL]
        self._finished = True
        self._refresh_position()

    def _reaction_change_state(self):
        self.change_state(self.target.current_state_key)
        self._refresh_position()
##        pass

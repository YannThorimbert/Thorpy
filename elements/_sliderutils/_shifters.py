from pygame.mouse import get_pressed

from thorpy.elements.clickable import Clickable
from thorpy.miscgui.constants import STATE_PRESSED
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import parameters, constants, style
from thorpy.painting.graphics import blit_arrow_on


class Shifter(Clickable):

    def __init__(self):
        Clickable.__init__(self)
        reac_rightclick = Reaction(parameters.BUTTON_UNPRESS_EVENT,
                                   self._reaction_rightpress,
                                   {"button": parameters.RIGHT_CLICK_BUTTON},
                                   reac_name=constants.REAC_RIGHT_CLICK)
        self.add_reaction(reac_rightclick)
        self.normal_params.polite_set("painter size", (16, 16))
        self.press_params.polite_set("painter size", (16, 16))

    def _reaction_rightpress(self, event):
        pass

    def add_arrow(self, side):
        #first, get frame:
        normal_img = self.get_image(constants.STATE_NORMAL)
        press_img = self.get_image(constants.STATE_PRESSED)
        #then blit an arrow
        blit_arrow_on(style.ARROW_IMG, style.ARROW_IMG_COLORKEY,
                      style.ARROW_IMG_COLORSOURCE,
                      style.ARROW_COLOR, side, normal_img)
        blit_arrow_on(style.ARROW_IMG, style.ARROW_IMG_COLORKEY,
                      style.ARROW_IMG_COLORSOURCE,
                      style.ARROW_COLOR, side, press_img)
        #then set the new image (with the arrow)
        self.set_image(normal_img, constants.STATE_NORMAL, False)
        self.set_image(press_img, constants.STATE_PRESSED, False)
        #now we do the same for hovered images
        normal_hov = self._hover_imgs[constants.STATE_NORMAL]
        press_hov = self._hover_imgs[constants.STATE_PRESSED]
        blit_arrow_on(style.ARROW_IMG, style.ARROW_IMG_COLORKEY,
                      style.ARROW_IMG_COLORSOURCE,
                      style.COLOR_TXT_HOVER, side, normal_hov)
        blit_arrow_on(style.ARROW_IMG, style.ARROW_IMG_COLORKEY,
                      style.ARROW_IMG_COLORSOURCE,
                      style.COLOR_TXT_HOVER, side, press_hov)
        self.set_image(normal_hov, constants.STATE_NORMAL, hovered=True)
        self.set_image(press_hov, constants.STATE_PRESSED, hovered=True)


class Plus(Shifter):

    def finish(self):
        Clickable.finish(self)
        self.add_arrow("top")

    def _reaction_rightpress(self, event):
        if self.collide(event.pos, self.current_state_key):
            self.father._drag_element.goto_start()

    def _reaction_time(self):
        if self.current_state_key == STATE_PRESSED:
            if get_pressed()[0]:
                self.father._drag_element.shift(parameters.CLICK_LIFT_REPEAT)



class Minus(Shifter):

    def finish(self):
        Clickable.finish(self)
        self.add_arrow("bottom")

    def _reaction_rightpress(self, event):
        if self.collide(event.pos, self.current_state_key):
            self.father._drag_element.goto_end()

    def _reaction_time(self):
        if self.current_state_key == STATE_PRESSED:
            if get_pressed()[0]:
                self.father._drag_element.shift(-parameters.CLICK_LIFT_REPEAT)

from pygame import event as pygevent

from thorpy.elements.draggable import Draggable
from thorpy.miscgui import constants, functions, style, painterstyle


class Dragger(Draggable):

    def __init__(self, slider, normal_params=None, press_params=None):
        super(Dragger, self).__init__("", [], normal_params, press_params)
        self.slider = slider
        params = {"color": style.COLOR_HOVER_DRAGGER}
        self.normal_params.polite_set("params hover",
                                      {"painter": painterstyle.DEF_PAINTER,
                                       "params": params})
        self.normal_params.polite_set("typ hover", "redraw")

    def set_setter(self):
        self.dragmove = self.dragmove_setter

    def _reaction_drag_transp(self, shift):
        self.unblit()
        self.update()
        self.move((shift[0], shift[1]))
        self.blit()
        self.update()


class DraggerX(Dragger):

    def __init__(self, slider, normal_params=None, press_params=None):
        Dragger.__init__(self, slider, normal_params, press_params)

    def dragmove_setter(self, x):
        self._reaction_drag_transp((x, 0))
        self.slider.father.refresh_value() #!!!

    def dragmove(self, x):
        self._reaction_drag_transp((x, 0))

    def is_and_will_be_inside(self, shift):
        slider_rect = self.slider._get_slide_rect()
        left = slider_rect.left
        right = slider_rect.right
        now = left <= self.current_state.ghost_rect.centerx <= right
        future = left <= self.current_state.ghost_rect.centerx + shift <= right
        return now and future

    def will_be_inside(self, shift):
        """Shift is in pixels units"""
        slider_rect = self.slider._get_slide_rect()
        left = slider_rect.left
        right = slider_rect.right
        return left <= self.current_state.ghost_rect.centerx + shift <= right

    def _reaction_drag(self, event):
        if self.current_state_key == constants.STATE_PRESSED:
            if self.will_be_inside(event.rel[0]):
                self.dragmove(event.rel[0])
                drag_event = pygevent.Event(constants.THORPY_EVENT,
                                            id=constants.EVENT_SLIDE,
                                            el=self.father.father)
                pygevent.post(drag_event)

    def shift(self, sign=1):
        if self.will_be_inside(sign):
            self.dragmove(sign)

    def place_at(self, value):
        x0 = self.slider._get_slide_rect().left
        pix = self.slider.val_to_pix(value, x0)
##        test = self.slider.pix_to_val(pix, x0) == value ?
        self.set_center((pix, None))



class DraggerY(Dragger):

    def __init__(self, slider, normal_params=None, press_params=None):
        Dragger.__init__(self, slider, normal_params, press_params)

    def goto_start(self):
        y = self.slider._plus.get_fus_topleft()[1]
        y += self.slider._plus.get_fus_size()[1]
        yself = self.get_fus_topleft()[1]
        shift = yself - y
        self.dragmove(-shift)
        return shift

    def goto_end(self):
        y = self.slider._minus.get_fus_topleft()[1]
        yself = self.get_fus_topleft()[1]
        yself += self.get_fus_size()[1]
        shift = yself - y
        self.dragmove(-shift)
        return shift

    def dragmove(self, y):
        self.unblit()
        self.update()
        self.move((0, y))
        self.blit()
        self.update()

    def is_and_will_be_inside(self, shift):
        slider_rect = self.slider._get_slide_rect()
        top = slider_rect.y
        bottom = slider_rect.bottom
        now = top <= self.current_state.ghost_rect.centery <= bottom
        future = top <= self.current_state.ghost_rect.centery + shift <= bottom
        return now and future

    def will_be_inside(self, shift):
        slider_rect = self.slider._get_slide_rect()
        top = slider_rect.y
        bottom = slider_rect.bottom
        return top <= self.current_state.ghost_rect.centery + shift <= bottom

    def _reaction_drag(self, event):
        if self.current_state_key == constants.STATE_PRESSED:
            if self.will_be_inside(event.rel[1]):
                self.dragmove(event.rel[1])

    def place_at(self, value):
        y0 = self.slider._get_slide_rect().y
        pix = self.slider.val_to_pix(value, y0)
        self.set_center((None, pix))

    def shift(self, sign=1):
        sign = -sign
        if self.is_and_will_be_inside(sign):
            self.dragmove(sign)
            debug_msg(self.slider.get_value())


class DraggerLiftY(DraggerY):

    """Dragger for a lift"""

    def __init__(self, slider, image=None, colorkey=None):
        super(DraggerLiftY, self).__init__(slider, image, colorkey)
        self.last_value = self.slider.limvals[0]  # init last_value

    def shift(self, sign=1):
        sign = -sign
        if self.is_and_will_be_inside(sign):
            self.dragmove(sign)
            current_value = self.slider.get_value()
            delta = self.last_value - current_value
            shift_y = 1 * delta
            self.slider._linked.scroll_children([self.slider], (0, shift_y))
            functions.debug_msg("Lift value : ", current_value)
            self.last_value = current_value

    def goto_start(self):
        shift = DraggerY.goto_start(self)
        current_value = self.slider.get_value()
        self.last_value = current_value
        self.slider._linked.scroll_children([self.slider], (0, shift))

    def goto_end(self):
        shift = DraggerY.goto_end(self)
        current_value = self.slider.get_value()
        self.last_value = current_value
        self.slider._linked.scroll_children([self.slider], (0, shift))

    def _reaction_drag(self, event):
        if self.current_state_key == constants.STATE_PRESSED:
            if self.will_be_inside(event.rel[1]):
                self.dragmove(event.rel[1])
                current_value = self.slider.get_value()
                delta = self.last_value - current_value
                shift_y = 1 * delta
                # move childrens
                self.slider._linked.scroll_children([self.slider], (0, shift_y))
                self.last_value = current_value


class DraggerDirViewerY(DraggerLiftY):

    def refresh_and_blit_ddlf(self):
        ddlf = self.slider._linked
        ddlf.unblit()
        ddlf.blit()
        ddlf.update()

    def shift(self, sign=1):
        sign = -sign
        if self.is_and_will_be_inside(sign):
            self.dragmove(sign)
            self.slider._linked._dv.pix_0 += sign
            self.refresh_and_blit_ddlf()

    def _reaction_drag(self, event):
        if self.current_state_key == constants.STATE_PRESSED:
            if self.will_be_inside(event.rel[1]):
                self.dragmove(event.rel[1])
                current_value = self.slider.get_value()
                shift_y = round(self.last_value - current_value)
                self.slider._linked._dv.pix_0 -= shift_y
                self.refresh_and_blit_ddlf()
                self.last_value = current_value

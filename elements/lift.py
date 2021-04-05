from thorpy.elements.ghost import Ghost
from thorpy.elements._sliderutils._shifters import Plus, Minus
from thorpy.elements.slider import SliderY
from thorpy.elements._sliderutils._dragger import DraggerLiftY, DraggerDirViewerY
from thorpy.miscgui.reaction import ConstantReaction
from thorpy.miscgui import constants, functions, parameters, style, painterstyle


class LiftY(SliderY):

    def __init__(self,
                 link,
                 text="",
                 elements=None,
                 dragsize=style.LIFT_DRAG_SIZE,
                 buttonsize=style.LIFT_BUTTON_SIZE,
                 normal_params=None,
                 finish=True):
        """<link> is the element affected by the lift"""
        dragsize = style.LIFT_DRAG_SIZE if dragsize is None else dragsize
        buttonsize=style.LIFT_BUTTON_SIZE if buttonsize is None else buttonsize
        link_h = link.get_fus_size()[1]  # get height of the linked element
        # set maxval to link height !!!! not link_h, but link_h - self_h
        limvals = (0, link_h)
        surplus_h = self._get_theo_size(buttonsize, dragsize, link_h,
                                       surplus=True)[1]
        length = link.get_fus_size()[1] - surplus_h  # compute proper height
        super(LiftY, self).__init__(length, limvals, text, elements,
                                    normal_params,finish=False)
        self._add_buttons()
        self._linked = link
        self.finish()
        e_right = link.get_fus_rect().right
        l_width = self.get_fus_size()[0]
        x = e_right - l_width - style.LIFT_MARGINS[0]
        y = link.get_fus_rect().top + style.LIFT_MARGINS[1]
        self.set_topleft((x, y))
        self._drag_element.place_at(self.limvals[0])

    def _reaction_wheel(self, event):
        if self.active_wheel:
            if self.father.collide(event.pos, self.father.current_state_key):
                self._drag_element.shift(parameters.WHEEL_LIFT_SHIFT)

    def _reaction_unwheel(self, event):
        if self.active_wheel:
            if self.father.collide(event.pos, self.father.current_state_key):
                self._drag_element.shift(-parameters.WHEEL_LIFT_SHIFT)

    def get_value(self):
        return int(SliderY.get_value(self))

    def finish(self):
        SliderY.finish(self)
        self._finish_add()

    def misc_refresh(self):
        SliderY.misc_refresh(self)
        self._refresh_limvals()

    def _refresh_limvals(self, fact=1.):
        linked_family = fact * self._linked.get_family_rect().height
        selfh = self.get_fus_size()[1]
        uplim = max(1, linked_family - selfh)
        self.limvals = (0, uplim)

    def _setup(self, width=None, dragsize=None):
        if width is None: width = style.LIFT_BUTTON_SIZE[0]
        if dragsize is None: dragsize = style.LIFT_DRAG_SIZE
        self._drag_element = DraggerLiftY(self)
        self._height = width
        painter = functions.obtain_valid_painter(
            painterstyle.DEF_PAINTER,
            pressed=True,
            color=style.DEF_COLOR2,
            size=(
                width,
                self._length +
                dragsize[1] +
                style.LIFT_MARGINS[1] +
                1))
        self.set_painter(painter)
        self._drag_element.set_painter(
            painterstyle.DEF_PAINTER(
                size=dragsize),
            autopress=False)
        try:
            self._drag_element.set_center((self.get_fus_center()[0], None))
        except AttributeError:  # state is ghost state, and has no fusionner
            self._drag_element.set_center((self.get_ghost_center()[0], None))
        self._drag_element.set_free(y=False)
        Ghost.fit_children(self)

    def _add_buttons(self, size=None):
        size = style.SMALL_SIZE if size is None else size
        self._plus = Plus()
        self._minus = Minus()
        self._plus.finish()
        self._minus.finish()
        self._plus.drag = self._drag_element
        self._minus.drag = self._drag_element
        reac_plus_time = ConstantReaction(constants.THORPY_EVENT,
                                     self._plus._reaction_time,
                                     {"id":constants.EVENT_TIME},
                                     reac_name=constants.REAC_MOUSE_REPEAT)
        self.add_reaction(reac_plus_time)
        reac_minus_time = ConstantReaction(constants.THORPY_EVENT,
                                     self._minus._reaction_time,
                                     {"id":constants.EVENT_TIME},
                                     reac_name=constants.REAC_MOUSE_REPEAT+0.1)
        self.add_reaction(reac_minus_time)
        self.add_elements([self._plus, self._minus])
        # reactions to mouse press:
        reac_pluspress2 = ConstantReaction(constants.THORPY_EVENT,
                                       self._drag_element.shift,
                                       {"el": self._plus,
                                        "id": constants.EVENT_PRESS},
                                       {"sign":parameters.CLICK_LIFT_SHIFT},
                                       reac_name=constants.REAC_PRESSED2)
        self.add_reaction(reac_pluspress2)
        reac_minuspress2 = ConstantReaction(constants.THORPY_EVENT,
                                    self._drag_element.shift,
                                    {"el": self._minus,
                                     "id": constants.EVENT_PRESS},
                                    {"sign":-parameters.CLICK_LIFT_SHIFT},
                                    reac_name=constants.REAC_PRESSED2+0.1)
        self.add_reaction(reac_minuspress2)

    def _finish_add(self, size=None):
        size = style.LIFT_BUTTON_SIZE if size is None else size
        rect = self.get_fus_rect()
        pos = (rect.centerx, rect.bottom + style.BUTTON_MARGINS[1] + size[1]/2)
        self._minus.set_center(pos)
        pos = (rect.centerx, rect.top - style.BUTTON_MARGINS[1] - size[1]/2)
        self._plus.set_center(pos)
        Ghost.fit_children(self)
        self._add_buttons_reactions()


class LiftDirViewerY(LiftY):

    def _setup(self, width=None, dragsize=None):
        width = style.LIFT_BUTTON_SIZE[0] if width is None else width
        dragsize = style.LIFT_DRAG_SIZE if dragsize is None else dragsize
        self._drag_element = DraggerDirViewerY(self)
        self._height = width
        painter = functions.obtain_valid_painter(
            painterstyle.DEF_PAINTER,
            color=style.DEF_COLOR2,
            pressed=True,
            size=(width,
                  self._length + dragsize[1] + style.LIFT_MARGINS[1] + 1))
        self.set_painter(painter)
        self._drag_element.set_painter(painterstyle.DEF_PAINTER(size=dragsize),
                                       autopress=False)
        self.current_state.ghost_rect.height = self._length
        try:
            self._drag_element.set_center((self.get_fus_center()[0], None))
        except AttributeError:  # state is ghost state, and has no fusionner
            self._drag_element.set_center((self.get_ghost_center()[0], None))
        self._drag_element.set_free(y=False)
        Ghost.fit_children(self)

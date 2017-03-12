from thorpy.elements.togglable import Togglable
from thorpy.elements.checker import Checker
from thorpy.miscgui.reaction import ConstantReaction
from thorpy.miscgui import constants

def get_dict(elements):
    dic = {}
    for e in elements:
        dic[e] = e.get_text()
    return dic

class RadioPool(object):

    def __init__(self, elements, first_value, always_value=True):
        for e in elements:
            assert isinstance(e, Checker)
            reac = ConstantReaction(constants.THORPY_EVENT, self.refresh,
                        event_args={"id":constants.EVENT_PRESS,
                                    "el":e},
                        params={"selected":e})
            e.add_reaction(reac)
            reac2 = ConstantReaction(constants.THORPY_EVENT, self.refresh,
                        event_args={"id":constants.EVENT_PRESS,
                                    "el":e._name_element},
                        params={"selected":e})
            e.add_reaction(reac2)
        self.elements = elements
        self._selected = None
        self.always_value = always_value
        if self.always_value:
            if not first_value:
                raise Exception("If always_value is true, first_value must be set")
        self.function = None
        if first_value:
            self._selected = first_value
            self._selected.set_value(True)


    def refresh(self, selected):
        for e in self.elements:
            if (e is not selected) and (e is not selected._name_element):
                if e.get_value() is True:
                    e.active = True
                    e._name_element.active = True
                    e.set_value(False)
                    e.unblit_and_reblit()
        self._selected = selected
        if self.always_value:
            self._selected.set_value(True)
            self._selected.unblit_and_reblit()
            self._selected.active = False
            self._selected._name_element.active = False
        if self.function:
            self.function()

    def get_selected(self):
        if self._selected:
            if self._selected.get_value() is True:
                return self._selected

class TogglablePool(object):

    def __init__(self, elements, first_value=None, always_value=False):
        for e in elements:
            assert isinstance(e, Togglable)
            reac = ConstantReaction(constants.THORPY_EVENT, self.refresh,
                        event_args={"id":constants.EVENT_TOGGLE,
                                    "el":e},
                        params={"selected":e})
            e.add_reaction(reac)
        self.elements = elements
        self._selected = None
        self.always_value = always_value
        if self.always_value:
            if not first_value:
                raise Exception("If always_value is true, first_value must be set")
        if first_value:
            self._selected = first_value
##            first_value._press()
            #
            first_value.change_state(constants.STATE_PRESSED)
            first_value._hovered = True
            sn = first_value.current_state_key
            if sn in first_value._states_hover:
                first_value.current_state.fusionner.img = first_value._hover_imgs[sn]
                first_value._updates[sn].center = first_value.get_fus_center(sn)
            first_value._count += 1
            first_value.toggled = True
        self.function = None

    def refresh(self, selected):
        for e in self.elements:
            if e is not selected:
                if e.current_state_key == constants.STATE_PRESSED:
                    e.active = True
                    e._force_unpress()
                    e._hovered = False
                    e._unhover()
        self._selected = selected
        if self.always_value:
            self._selected.active = False
        if self.function:
            self.function()

    def get_selected(self):
        if self._selected:
            if self._selected.current_state_key == constants.STATE_PRESSED:
                return self._selected
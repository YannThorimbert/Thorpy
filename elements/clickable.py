from pygame.event import post, Event

from thorpy.elements.pressable import Pressable
from thorpy.elements.hoverable import Hoverable
from thorpy.miscgui.constants import STATE_NORMAL, STATE_PRESSED, EVENT_PRESS, EVENT_UNPRESS, THORPY_EVENT


class Clickable(Pressable, Hoverable):
    """Clickable Element (Pressable and hoverable)"""

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None, finish=True):
        """Pressable and hoverable element.
        <text>: the text of the element.
        """
        super(Clickable, self).__init__(text, elements, normal_params,
                                        press_params,finish=False)
        self.normal_params.polite_set("states hover",
                                      list([STATE_NORMAL, STATE_PRESSED]))
        if finish:
            self.finish()

    def finish(self):
        Pressable.finish(self)
        self._set_hovered_states_auto()
##        Hoverable.finish(self)

    def _remove_help(self):
        if self._help_element:
            self._help_element.unblit()
            self._help_element.update()
            self._help_element.set_recursive("visible", False)
            self._waited = 0

    def _press(self):
        state_ok = self.current_state == self._states[STATE_NORMAL]
        if state_ok:
            self.change_state(STATE_PRESSED)
            self._hover()
            ev_press = Event(THORPY_EVENT, id=EVENT_PRESS, el=self)
            post(ev_press)
            self._remove_help()

    def _unpress(self):
        self.change_state(STATE_NORMAL)
        ev_unpress = Event(THORPY_EVENT, id=EVENT_UNPRESS, el=self)
        post(ev_unpress)

    def _reaction_unpress(self, pygame_event):
        state_ok = self.current_state == self._states[STATE_PRESSED]
        if state_ok:
            self._unpress()
            if self.collide(pygame_event.pos, STATE_PRESSED):
                self._hover()
                self.run_user_func()
            else:
                self._unhover()

    def _reaction_unpress_key(self):
        state_ok = self.current_state == self._states[STATE_PRESSED]
        if state_ok:
            self._unpress()
            self._hover()
            self.run_user_func()

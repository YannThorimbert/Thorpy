from pygame.event import Event, post

from thorpy.elements.clickable import Clickable
from thorpy.miscgui import constants


class Togglable(Clickable):
    """Mouse-togglable element"""

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None):
        super(Togglable, self).__init__(text, elements, normal_params,
                                        press_params)
        self._count = 0
        self.toggled = False

    def _reaction_press(self, event):
        if self._count < 1:
            tag = constants.STATE_NORMAL
        else:
            tag = constants.STATE_PRESSED
        if self.collide(event.pos, tag):
            self._press()

    def _press(self):
        Clickable._press(self)
        self._count += 1
        if not self.toggled:
            ev_tog = Event(constants.THORPY_EVENT, id=constants.EVENT_TOGGLE,
                            el=self)
            post(ev_tog)
            self.toggled = True
##            print("posted t")

    def _force_unpress(self):
        self._count = 0
        Clickable._unpress(self)
##        self._unhover_noblit()
        ev_untog = Event(constants.THORPY_EVENT,
                        id=constants.EVENT_UNTOGGLE, el=self)
        post(ev_untog)
        self.toggled = False
##        print("posted u")

    def _unpress(self):
        if self._count == 2:
            self._force_unpress()

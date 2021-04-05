from pygame.locals import KEYDOWN, KEYUP

from thorpy.elements.pressable import Pressable
from thorpy.miscgui.constants import STATE_NORMAL, STATE_PRESSED


class KeyPressable(Pressable):
    """Keyboard pressable element"""

    def __init__(self, key, text="", elements=None, normal_params=None,
                 press_params=None, type_=KEYDOWN, untyp=KEYUP, finish=True):
        """Keyboard pressable element
        <key>: the pygame keyboard key for press event."""
        super(KeyPressable, self).__init__(text, elements, normal_params,
                                           press_params, finish=False)
        self._set_press_reaction(type_, args=dict({"key": key}))
        self._set_unpress_reaction(untyp, args=dict({"key": key}))
        if finish:
            self.finish()

    def _reaction_press(self, event):
        if self.current_state_key == STATE_NORMAL:
            Pressable._press(self)

    def _reaction_unpress(self, event):
        if self.current_state_key == STATE_PRESSED:
            Pressable._unpress(self)

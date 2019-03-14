from pygame.locals import KEYDOWN

from thorpy.elements.pressable import Pressable
from thorpy.miscgui.constants import STATE_NORMAL, STATE_PRESSED, REAC_UNPRESS


class KeyTogglable(Pressable):
    """Keyboard togglable element"""

    def __init__(self, key, text="", elements=None, normal_params=None,
                 press_params=None, type_=KEYDOWN, finish=True):
        """Keyboard togglable element
        <key>: the pygame keyboard key for press event."""
        super(KeyTogglable, self).__init__(text, elements, normal_params,
                                           press_params, finish=False)
        self._set_press_reaction(type_, args=dict({"key": key}))
##        self.set_key(key, type_)
        self._reactions.pop(REAC_UNPRESS)
        if finish:
            self.finish()

    def set_key(self, key, event_type=KEYDOWN):
        self._set_press_reaction(event_type, args=dict({"key": key}))

    def _reaction_press(self, event):
        if self.current_state_key == STATE_NORMAL:
            Pressable._press(self)
        elif self.current_state_key == STATE_PRESSED:
            Pressable._unpress(self)
            self.run_user_func()

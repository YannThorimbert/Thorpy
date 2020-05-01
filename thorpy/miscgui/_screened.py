"""Module for creating _Screened objects, that are designed to be blitted on
the screen.
"""
from pygame import display


class _Screened(object):
    """Object that is designed to be blitted on the screen. Implements
    methods for setting the screen clips.
    """

    def __init__(self):
        """Object that is designed to be blitted on the screen."""
##        self.surface = display.get_surface()
        self._old_clips = [None]  # fifo

    def _add_old_clip(self):
        """Add the current clip of the screen to the list of previous clips.
        """
        self._old_clips.insert(0, self.surface.get_clip())

    def _unclip_screen(self):
        """Restore the oldest of the previous clips as the clip of the screen,
        and removes it from the previous clips list.
        """
        self.surface.set_clip(self._old_clips.pop(0))

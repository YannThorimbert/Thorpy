"""Module defining default keyboard behaviour."""

import pygame
from pygame.locals import *

from thorpy.miscgui.functions import debug_msg



MODIFIERS = [K_RSHIFT,
             K_LSHIFT,
             K_RCTRL,
             K_LCTRL,
             K_RALT,
             K_LALT,
             K_RMETA,
             K_LMETA]

QWERTZ_SPECIALS = {(K_RALT, K_3): K_HASH,                        # "#"
                   (K_RALT, K_2): K_AT,                          # "@"
                   (K_LSHIFT, K_MINUS): K_QUESTION,              # "?"
                   (K_LSHIFT, K_PERIOD): K_COLON,                # ":"
                   (K_LSHIFT, K_COMMA): K_SEMICOLON,             # ";"
                   (K_LSHIFT, K_7): K_SLASH,                     # "/"
                   (K_LSHIFT, K_LESS): K_GREATER,                # ">"
                   (K_LSHIFT, K_3): K_ASTERISK,                  # "*"
                   }
SPECIALS = {}


QWERTZ_CHANGES = {K_z: K_y,
                  K_y: K_z,
                  K_SLASH: K_MINUS}  # example
CHANGES = {}


def set_qwertz():
    global SPECIALS, CHANGES
    SPECIALS = QWERTZ_SPECIALS.copy()
    CHANGES = QWERTZ_CHANGES.copy()

def set_default():
    global SPECIALS, CHANGES
    SPECIALS = {}
    CHANGES = {}

class Keyer(object):
    # Penser a permettre les set blocked et allowed

    def __init__(self, specials=None, modifiers=None, changes=None):
        if not specials:
            specials = SPECIALS
        if not modifiers:
            modifiers = MODIFIERS
        if not changes:
            changes = CHANGES
        self.specials = specials
        self.changes = changes
        self.modifiers = modifiers

    def _get_changed(self, key):
        """Performs the 'translation' between <key> and its corresponding value
        according to self.changes's dict.
        """
        changed = self.changes.get(key)
        if changed:
            return changed
        else:
            return key

    def _more_than_256(self, key):
        key = pygame.key.name(key)
        if key.startswith("["):
            if key.endswith("]"):
                return key[1:-1]
        return key

    def get_char_from_key(self, key):
        """<default> is returned if no character can be found from <key>"""
        pressed = pygame.key.get_pressed()
        pygame.event.pump()
        for (ka, kb) in self.specials:  # handle combinations
            if pressed[ka]:
                if kb == key:
                    key = self.specials[(ka, kb)]
                    if key < 256:
                        return chr(key)
        key = self._get_changed(key)
        if pressed[K_LSHIFT]:  # handle caps
            if key >= 32 and key <= 126:
                key -= 32
        debug_msg("key interpretation :", key, pygame.key.name(key))
        if key < 256:
            return chr(key)
        else:
            return self._more_than_256(key)

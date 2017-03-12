"""State with no graphical existence"""
from pygame.rect import Rect


def get_same_state(state):
    tl = state.ghost_rect.topleft
    size = state.ghost_rect.size
    return _GhostState(tl, size)


class _GhostState(object):

    def __init__(self, topleft=(0, 0), size=(0, 0)):
        self.ghost_rect = Rect(topleft, size)

    def set_ghost_rect(self, topleft, size):
        self.ghost_rect.topleft = topleft
        self.ghost_rect.size = size

    def set_topleft(self, topleft):
        self.ghost_rect.topleft = topleft

    def move(self, shift):
        """Move and refresh using set_topleft"""
        pos_x = shift[0] + self.ghost_rect.x
        pos_y = shift[1] + self.ghost_rect.y
        self.set_topleft((pos_x, pos_y))

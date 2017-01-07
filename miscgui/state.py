"""Couple of fusionner, position and ghost rect"""

from thorpy.miscgui._ghoststate import _GhostState
from thorpy._utils.rectscomputing import get_rel_pos_topleft

from thorpy.miscgui.title import Title
from thorpy.painting.painters.painter import Painter
from thorpy.painting.fusionner import _Fusionner

def get_void_state():
    title = Title("")
    painter = Painter(None)
    fusionner = _Fusionner(painter, title)
    return State(fusionner)


class State(_GhostState):

    """
    Triplet of fusionner, position and ghost rect.
    Note that the ghost rect must be an inflation of the fusionner's one, i.e
    they share a common center coordinate.
    """

    def __init__(self, fusionner, topleft=(0, 0), inflation=(0, 0)):
        """inflation is negative if ghost is bigger than img"""
        super(State, self).__init__(topleft, (0, 0))
        self.fusionner = fusionner
        self.inflation = inflation
        self.ghost_rect = self.get_ghost_from_fus()

    def compute_inflation(self):
        semi_infl = get_rel_pos_topleft(self.fusionner.rect, self.ghost_rect)
        return (2 * semi_infl[0], 2 * semi_infl[1])

    def set_ghost_rect(self, topleft, size):
        _GhostState.set_ghost_rect(self, topleft, size)
        self.inflation = self.compute_inflation()

    def get_anti_inflation(self):
        return (-self.inflation[0], -self.inflation[1])

    def get_ghost_from_fus(self):
        """Returns inflated fusionner rect according to self.inflation."""
        return self.fusionner.rect.inflate(self.get_anti_inflation())

    def set_topleft(self, topleft):
        """Refresh the ghost rect and the fusionner rect too."""
        self.ghost_rect.topleft = topleft
        # replace fusionner into the center
        self.fusionner.rect.center = self.ghost_rect.center

    def refresh_ghost_rect(self):
        self.ghost_rect = self.get_ghost_from_fus()

    def recenter_fusionner(self):
        self.fusionner.rect.center = self.ghost_rect.center

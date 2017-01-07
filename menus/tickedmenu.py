import pygame

from thorpy.menus.basicmenu import BasicMenu
from thorpy.miscgui import constants


class TickedMenu(BasicMenu):
    """Post time since last frame"""

    def post_time_event(self):
        tick_ = self.clock.get_time()
        event = pygame.event.Event(constants.THORPY_EVENT,
                                   id=constants.EVENT_TIME,
                                   tick=tick_)
        pygame.event.post(event)

    def react_to_all_events(self):
##        self.clock_tick(self.fps)
        self.post_time_event()
        for event in pygame.event.get():
            self.treatement(event)

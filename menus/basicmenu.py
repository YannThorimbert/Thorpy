import pygame

from thorpy.miscgui import functions, parameters
from thorpy.miscgui import application



class BasicMenu(object):

    def __init__(self, elements=None, fps=45):
        if not elements:
            elements = []
        self._elements = [] #will be set in self.set_elements
        self.set_elements(elements)
        self.fps = fps
        self.leave = False
        self.population = self.get_population()
        self.events = self.get_events()
        self.finish_population()
        self.time_before_kill = None
        self.clock = pygame.time.Clock()
        if application.TICK_BUSY:
            self.clock_tick = self.clock.tick_busy_loop
        else:
            self.clock_tick = self.clock.tick
        self.something_to_add = []
        self.ask_for_refresh = False
        pygame.key.set_repeat(parameters.KEY_DELAY, parameters.KEY_INTERVAL)

    def kill_after(self, duration_in_frames):
        self.time_before_kill = duration_in_frames

    def rebuild(self, elements=None):
        self.__init__(elements)

    def refresh(self):
        self.population = self.get_population()
        self.events = self.get_events()

    def finish_population(self):
        """Control that all elements have been finished"""
        for e in self.population:
            if not(e._finished):
                functions.debug_msg(str(e) + " was not _finished !\
                                                Automatic finish.")
                e.finish()

    def refresh_population(self, painting=False, placing=True, one_wheel=True):
        """Calls element's refresh functions. <painting> enable graphical
        refreshment.
        Caution : misc_refresh method of elements is called if placing is True.
        """
        wheeled = None
        for e in self.population:
            if hasattr(e, "active_wheel"):
                if e.active_wheel:
                    if wheeled:
                        functions.debug_msg(str(e) + " is not the only wheel-active.")
                        if one_wheel:
                            e.active_wheel = False
                            onstants.debug_msg(str(e) + " wheel was deactivated.")
                    else:
                        wheeled = True
            if painting:  # used for debug
                e.redraw()
            if placing:
                if hasattr(e, "misc_refresh"):
                    e.misc_refresh()

    def get_population(self):
        pop = []
        for e in self._elements:
            pop.append(e)
            pop.extend(e.get_descendants())
        return set(pop)

    def add_to_population(self, element):
        self._elements.append(element)
        self.refresh()

    def remove_from_population(self, element):
        self._elements.remove(element)
        self.refresh()

    def get_events(self):
        """Returns a dictionnary of type:
        events[event_a] = [element1, element2, ... ].
        """
        events = {}
        for element in self.population:
            for reaction in element._reactions:
                event = reaction.reacts_to
                if event in events:
                    events[event].append(element)
                else:
                    events[event] = [element]
        for event in events:
            events[event] = set(events[event])
        return events

    def freeze(self):
        """Freezes all self's elements."""
        for el in self._elements:
            el.freeze()

    def set_elements(self, elements):
        """Assign the right value to self._elements"""
        if isinstance(elements, list):
            self._elements = elements
        else:
            self._elements = list([elements])

    def blit_and_update(self):
        for e in self._elements:
            e.blit()
            e.update()

    def react(self, event):
        elements = self.events.get(event.type, [])
        for element in elements:
            element.react(event)

    def block_unused_events(self):
        """! This disable the possibility to handle unexpected events"""
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.QUIT)
        for event in self.events:
            pygame.event.set_allowed(event)

    def treatement(self, event):
        if event.type == pygame.QUIT:
            pygame.font.quit()
            pygame.quit()
            exit()
        else:
            self.react(event)

    def set_leave(self):
        self.leave = True

    def react_to_all_events(self):
##        self.clock_tick(self.fps)
        for event in pygame.event.get():
            if not event in self.ignore:
                self.treatement(event)

    def play(self, preblit=True):
        functions.set_current_menu(self)
        if preblit:
            self.blit_and_update()
        while not self.leave:
            if self.time_before_kill is not None:
                self.time_before_kill -= 1
                if self.time_before_kill < 0:
                    self.leave = True
                    break
            if application.SHOW_FPS:
                print(self.clock.get_fps())
            self.clock_tick(self.fps)
            self.react_to_all_events()


def interactive_pause(max_time_in_seconds, element=None, fps=45):
    if element is None:
        element = Ghost()
    menu = BasicMenu(element, fps=fps)
    menu.kill_after(menu.fps * max_time_in_seconds)
    menu.play()
    return menu.kill_after

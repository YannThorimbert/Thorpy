import pygame
import thorpy

def writing():
    thorpy.parameters.KEY_DELAY = 30
    thorpy.parameters.KEY_INTERVAL = 100
    pygame.key.set_repeat(30,500)

def playing(fps):
    value = 1000//fps
    thorpy.parameters.KEY_DELAY = value
    thorpy.parameters.KEY_INTERVAL = value
    pygame.key.set_repeat(value,value)

class Commands:

    def __init__(self, element, delta_i=-1):
        self.e = element
        self._initialize()
        self.last_key_action = -float("inf")
        self.i = 0
        self.delta_i = delta_i
        self.cam_shift = [0,0]
        self.reac = {}
        self.refresh = None

    def _initialize(self):
        self.reac_keydown = thorpy.Reaction(pygame.KEYDOWN, self.func_keydown)
        self.e.add_reaction(self.reac_keydown)
        #
        self.reac_time = thorpy.ConstantReaction(thorpy.constants.THORPY_EVENT,
                                            self.func_time,
                                            {"id":thorpy.constants.EVENT_TIME})
        self.e.add_reaction(self.reac_time)

    def func_keydown(self, e):
        if self.i > self.last_key_action + self.delta_i:
            self.last_key_action = self.i
            reaction = self.reac.get(e.key)
            if reaction:
                reaction()

    def func_time(self):
        if self.refresh:
            self.refresh()
        self.i += 1

    def add_reaction(self, key, func):
        if key in self.reac:
            raise Exception("There is already a func for this key")
        self.reac[key] = func

    def default_func(self):
        pass
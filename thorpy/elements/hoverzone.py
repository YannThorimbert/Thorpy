from pygame import MOUSEMOTION
from pygame.mouse import get_pos as mouse_pos

from thorpy.elements.ghost import Ghost
from thorpy.elements.element import Element
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, functions, parameters

class HoverZone(Ghost):
    """Ghost element designed to react to mouse hovering - can post hover events
    ."""

    @staticmethod
    def make(zone=None, elements=None):
        hz = HoverZone(zone, elements)
        hz.finish()
        return hz

    def __init__(self, hover_zone=None, elements=None, normal_params=None):
        """Ghost element designed to react to mouse hovering - can post hover events
        .
        <hover_zone>: a pygame rect defining the hovering zone."""
        Ghost.__init__(self, elements, normal_params)
        self._hovered = False
        self.set_hover(MOUSEMOTION)
        self._help_element = None
        self._waited = 0
        self._help_wait_time = parameters.HELP_WAIT_TIME
        self._help_pos = None
        self._help_reaction = None
        self._help_blitted = False
        self.visible = False
        if hover_zone:
            self.set_hover_zone(hover_zone)
        self.surface = functions.get_screen()

    def set_hover_zone(self, rect, state=None):
        self.set_ghost_rect(rect.topleft, rect.size, state)

    def set_hover(self, event, args=None):
        """Set the <event> which makes the element hovered if <args> are the
        right ones.
        <event> : a pygame event.
        <args> : a dictionnary.
        """
        if not args:
            args = {}
        reac_hover = Reaction(event, self._reaction_hover, args,
                              reac_name=constants.REAC_HOVER)
        self.add_reaction(reac_hover)

    def _reaction_help(self, event): #set self help element visible ou pas.
        """Reaction to EVENT_TIME event"""
        if self._hovered:
            self._waited += event.tick
            if self._waited > self._help_wait_time/2.:  # then must switch
                self._waited = -float("inf")
                if not(self._help_pos):
                    r = self._help_element.get_fus_rect()
                    jail_rect = self._help_element.get_jail_rect()
                    if not jail_rect:
                        jail_rect = self.surface.get_rect()
                    mouse_topleft = mouse_pos()
                    r.topleft = mouse_topleft
                    if jail_rect.contains(r):
                        self._help_element.set_topleft(mouse_pos())
                    else:
                        #clamping
                        r = r.clamp(jail_rect)
                        self._help_element.set_topleft(r.topleft)
                self._help_element.set_recursive("visible", True)
                self._help_element.blit()
                self._help_blitted = True
                self._help_element.update()
        else:# then the helper has been blitted and must be unblitted
            if self._waited < 0:
                self._help_element.unblit()
                self._help_blitted = False
                self._help_element.update()
                self._help_element.set_recursive("visible", False)
                self._waited = 0
                self.remove_reaction(self._help_reaction)

    def _remove_help(self):
        if self._help_element:
            self._help_element.unblit()
            self._help_blitted = False
            self._help_element.update()
            self._help_element.set_recursive("visible", False)
            self._waited = 0
        ##            if self._help_reaction in self._reactions:
        ##                self.remove_reaction(self._help_reaction)

    def _reaction_hover(self, pygame_event):
        """Normally, reacts to pygame.MOUSEMOTION, but can be redefined."""
        if self._hovered and not self._help_blitted:
            self._waited = 0
        elif self._hovered and self._help_blitted:
            self._remove_help()
        beeing_hovered = self.collide(pygame_event.pos, self.current_state_key)
        if not self._hovered and beeing_hovered:  # can only change to True
            self._hover()
            if self._help_element:
                self.add_reaction(self._help_reaction)
                functions.add_element_to_current_menu(self) #refresh reaction
        elif self._hovered and not(beeing_hovered):  # can only change to False
            self._unhover()

    def _hover(self):
        self._hovered = True

    def _unhover(self):
        self._hovered = False

    def add_basic_help(self, text, wait_time=None, jail=None):
        helper = Element(text,finish=False)
        helper._is_in_family = False
        helper.set_style("help")
        helper.finish()
        helper.scale_to_title()
        if wait_time is None:
            wait_time=self._help_wait_time
        helper.set_help_of(self, self._help_wait_time)
        if jail:
            helper.set_jailed(jail)

    def remove_help(self):
        if self._help_element:
            self.remove_elements([self._help_element])
            self.remove_reaction(self._help_reaction)

    def get_storer_rect(self):
        import pygame
        return pygame.Rect(0, 0, 0, 0)
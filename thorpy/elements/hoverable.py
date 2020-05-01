from pygame import MOUSEMOTION
from pygame.mouse import get_pos as mouse_pos

from thorpy.elements.element import Element
from thorpy.elements.pressable import Pressable
from thorpy.elements._hoverutils import _hovergetter as hovergetter
from thorpy._utils.images import change_color_on_img as ccoi
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, functions, parameters, style

class Hoverable(Element):
    """Hoverable Element."""

    def __init__(self, text="", elements=None, normal_params=None, finish=True):
        """Hoverable Element."""
        super(Hoverable, self).__init__(text, elements, normal_params, finish=False)
        self._hover_imgs = {}
        self._normal_imgs = {}
        self._updates = {}
        self._hovered = False
        self.set_hover(MOUSEMOTION)
        self._states_hover = self.normal_params.params.get(
            "states hover",
            [constants.STATE_NORMAL])
        self._help_element = None
        self._waited = 0
        self._help_wait_time = parameters.HELP_WAIT_TIME
        self._help_pos = None
        self._help_reaction = None
        self._help_blitted = False
        if finish:
            self.finish()

    def finish(self):
        Element.finish(self)
        self._set_hovered_states_auto()

    def reinit(self):
        self.set_hover(MOUSEMOTION)
        self.set_hovered_states(self._states_hover)

    def set_title(self, title, state=None, center_title=True):
        Element.set_title(self, title, state, center_title)
        self.set_hovered_states(self._states_hover)

    def set_text(self, text=None, state=None, center_title=True, size=None,
                cut=-1):
        Pressable.set_text(self, text, state, center_title, size, cut)
        self.set_hovered_states(self._states_hover)

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        Element.set_font_color(self, color, state, center_title)
        self.set_hovered_states(self._states_hover)

    def set_font_color_hover(self, color):
        """set _hover font color"""
        self.set_hovered_states(self._states_hover, "text highlight", color)

    def set_font_size(self, size, state=None, center_title=True):
        """set font color"""
        Element.set_font_size(self, size, state, center_title)
        self.set_hovered_states(self._states_hover)

    def set_font(self, fontname, state=None, center_title=True):
        """set font for a given state"""
        Element.set_font(self, fontname, state, center_title)
        self.set_hovered_states(self._states_hover)

    def replace_img_color(self, source, target, state=None, center=True,
                          preserve=False):
        """replace colors"""
        Element.replace_img_color(self, source, target, state, center,
                                  preserve)
        self.set_hovered_states(self._states_hover)

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

    def _reaction_help(self, event):
        """Reaction to EVENT_TIME event"""
        if self._hovered:
            self._waited += event.tick
            #/ 2 because Clock.get_time() returns time between two last iters.
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
        sn = self.current_state_key
        if sn in self._states_hover:
            self.unblit()
            self.current_state.fusionner.img = self._hover_imgs[sn]
            self.blit()
            self._updates[sn].center = self.get_fus_center(sn)
            self.update()

##    def _unhover_noblit(self):
##        sn = self.current_state_key
##        self._hovered = False
##        self.unblit()
##        self.current_state.fusionner.img = self._normal_imgs[sn]
##        self.blit()
##        self._updates[sn].center = self.get_fus_center(sn)
##        self.update()


    def _unhover(self):
        sn = self.current_state_key
        self._hovered = False
        self.unblit()
        self.current_state.fusionner.img = self._normal_imgs[sn]
        self.blit()
        self._updates[sn].center = self.get_fus_center(sn)
        self.update()

    def _set_hovered_states_auto(self, color=style.COLOR_TXT_HOVER):
        if color is None: color=style.COLOR_TXT_HOVER
        params = self.normal_params.params.get("params hover", color)
        states = self.normal_params.params.get("states hover")
        states = [constants.STATE_NORMAL] if not states else states
        type_ = self.normal_params.params.get("typ hover", "painter")
        self.set_hovered_states(states, type_, params)

    def set_hovered_states(self, states=None, mode="painter",
                           params=style.COLOR_TXT_HOVER):
        """
        Add or set an image for all the _states in <states> when they are
        _hovered. <states> is a list of _states numbers.

        Values for <mode>:
            'painter' : the fusionner related to <state> will be used, and so
                        the painter if it exists. The color used for the title's
                        writer will be <params>.

            'text highlight' : just like 'painter'.

            'text illuminate' : performs an illumination of the title.

            'all highlighted' : change the whole color of the element.

            'image' : directly assign an image, whose value is <params>. It is
                      up to you to adapt the element's other properties if
                      needed.

            'change color' : use per-pixel color change. Minimal <params> value:
                             {'source" : <your source color>,
                              'target' : <your target color>}
                 See element.replace_img_color for the other possible params.

            'redraw' : use element's redraw method. <param> must be a
                       dictionnary containing the following keys:
                        - 'painter' : storing the painter you want to be used;
                        - 'params' : a dictionnary storing the params to use
                          with the painter.
        If something else than the above strings is passed as <mode>, the image
        used will be the return value of <mode> used as a function, taking
        <params> as parameters.
        """
        self._states_hover = list()
        if not states:
            return
        if states == "all":
            states = self._states.keys()
        for state in states:
            self.set_hovered_state(state, mode, params)


    def set_size(self, size, state=None, center_title=True, adapt_text=True,
                 cut=None, margins=style.MARGINS):
        """scale"""
        Element.set_size(self, size, state, center_title, adapt_text, cut,
                         margins)
        self.set_hovered_states(self._states_hover)

    def scale_to_title(self, margins=None, state=None):
        """scale to content"""
        margins = style.MARGINS if margins is None else margins
        Element.scale_to_title(self, margins, state)
        self.set_hovered_states(self._states_hover)

    def redraw(self, state=None, painter=None, title=None, refresh_title=False):
        """Changes element style (default : "classic" )"""
        Element.redraw(self, state, painter, title, refresh_title)
        self.set_hovered_states(self._states_hover)

    def set_hovered_state(self, state, mode="painter", params=None):
        """
        Add or set an image for <state> when it is _hovered.
        Values for <mode>:
            'painter' : the fusionner related to <state> will be used, and so
                        the painter if it exists. The color used for the title's
                        writer will be <params>

            'text highlight' : just like 'painter'.

            'text illuminate' : performs an illumination of the title.

            'all highlighted' : change the whole color of the element. <params>
                                = (<color_text>, <color_bulk>).

            'image' : directly assign an image, whose value is <params>. It is
                      up to you to adapt the element's other properties if
                      needed.

            'change color' : use per-pixel color change. Minimal <params> value:
                             {'source" : <your source color>,
                              'target' : <your target color>}
                 See element.replace_img_color for the other possible params.

            'redraw' : use element's redraw method. <param> must be a
                       dictionnary containing the following keys:
                        - 'painter' : storing the painter you want to be used;
                        - 'params' : a dictionnary storing the params to use
                          with the painter.
        If something else than the above strings is passed as <mode>, the image
        used will be the return value of <mode> used as a function, taking
        <params> as parameters.
        """
        params = style.COLOR_TXT_HOVER if params is None else params
        self._normal_imgs[state] = self._states[state].fusionner.img #why copy?
        self._states_hover.append(state)
        if mode == "text highlight":  # auto higlight
            self._hover_imgs[state] = hovergetter.get_img_highlighted(self, state,
                                                               params)
        elif mode == "text illuminate":
            self._hover_imgs[state] = hovergetter.get_illuminated_title(self, state,
                                                                 params)
        elif mode == "all highlighted":
            self._hover_imgs[state] = hovergetter.get_all_highlighted_title(self,
                                                                     state,
                                                                     params)
        elif mode == "image":  # assign existing image
            self._hover_imgs[state] = params
        elif mode == "change color":
            self._hover_imgs[state] = ccoi(self._states[state].fusionner.img, **params)
        elif mode == "redraw":
            self._hover_imgs[state] = hovergetter.get_img_redraw(self, state, params)
        elif mode == "painter":
            self._hover_imgs[state] = hovergetter.get_img_painter(self, state, params)
        else:  # use function
            self._hover_imgs[state] = mode(**params)
        self._updates[state] = self._hover_imgs[state].get_rect()

    def get_image_hover(self, state=constants.STATE_NORMAL):
        return self._hover_imgs[state]

    def remove_hovered_state(self, statename):
        self._states_hover.remove(statename)
        self._hover_imgs.pop(statename)
        self._normal_imgs.pop(statename)
        self._updates.pop(statename)

    def remove_all_hovered_states(self):
        for state in self._states_hover:
            self.remove_hovered_state(state)

    def add_basic_help(self, text, wait_time=None, jail=None):
        helper = Element(text,finish=False)
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

    def get_image(self, state=constants.STATE_NORMAL, hovered=False):
        if hovered:
            return self._hover_imgs[state]
        else:
            return self._states[state].fusionner.img

    def set_image(self, img, state=constants.STATE_NORMAL, hovered=False):
        if hovered:
            self._hover_imgs[state] = img
        else:
            self._states[state].fusionner.img = img
            self._normal_imgs[state] = img

    @staticmethod
    def make_hoverable(element, normal_params=None):
        """self.imgs[ONE_STATE] is the hovering img to place when hovering element
        while it is in state ONE_STATE. In that case, self.current_state.img =
        self._hover_imgs[ONE_STATE]. When unhovering, the self._normal_imgs[ONE_STATE] is
        recovered in self.current_state.img.

        Note that at initialization, two fusions are used in standard hovering :
        one for getting _hovered image, another.
        """
        from thorpy._utils.functions import fusion_dicts
        hoverable = Hoverable(normal_params=normal_params)
        d = fusion_dicts(element.__dict__, hoverable.__dict__)
        hoverable.__dict__ = d
        hoverable.reinit()
        return hoverable

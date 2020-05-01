import pygame
from pygame import Rect
from pygame import display

from thorpy.miscgui import constants, functions
from thorpy.miscgui.state import get_void_state
from thorpy.miscgui._ghoststate import _GhostState
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui.initializer import init_params
from thorpy.miscgui.storage import _set_center as storage_set_center
from thorpy.miscgui.storage import Storer


class Ghost(object):
    """
    Element of an application that have no graphical existence, though its
    children might be graphicals.

    This is the base class for all the Elements.
    """
    _current_id = 0 #variable storing the id of the element

    @classmethod
    def make(cls, elements=None):
        g = cls(elements=elements)
        g.finish()
        return g

    def __init__(self, elements=None, normal_params=None, finish=True):
        """
        Element of an application that have no graphical existence, though its
        children might be graphicals. This is the base class for all the Elements.

        <elements>: list of the children elements.
        """
        self.get_size = self.get_fus_size
        self.surface = display.get_surface()
        if not elements:
            elements = []
        self.normal_params = init_params(normal_params)
        """State can be anything useful for user"""
        self._reactions = []
        self._blit_before = []
        self._blit_after = []
        # elements whose this reacter instance is an element
        self.father = None
        # init elements
        self._elements = []
        self.add_elements(elements)
        # init _states
        self._states = {}
        self._states[constants.STATE_NORMAL] = _GhostState()
        self.current_state = self._states[constants.STATE_NORMAL]
        self.current_state_key = constants.STATE_NORMAL
        # init user function
        self.visible = False
        self.user_func = self.normal_params.params.get("user func")
        self.user_params = self.normal_params.params.get("user params", {})
        self.active = True
        self._finished = False
        self._jail = None
        self._lock_jail = False
        self.rank = constants.DEFAULT_RANK
        self.click_quit = None
        self._lift = None
        self._jail = None
        self._overframe = None #used for shadows. Indicate that element can clip outside of its parent's clip
        self._is_in_family = True
        self.message = None
        self.id = Ghost._current_id
        Ghost._current_id += 1
        if finish:
            self.finish()


    def finish(self):
        self._finished = True

    def is_finished(self):
        return self._finished

    def set_blit_before(self, element):
        """Transfer <element> from self._elements to self._blit_before.
        <element> : can either be an instance of Ghost or a string.

        Note that this is useful when self is blitted and it must be blitted
        after <element>. If one blits <element> alone (i.e not by blitting self)
        , then <element> will of course appear as blitted after self.
        """
        if not element in self._elements:
            element = self.get_elements_by_text[element]
            if len(element) > 0:
                element = element[0]
        if not element:
            raise Exception("No element found to store in blit_before.")
        if element in self._blit_before:
            functions.debug_msg(element, " was already in self._blit_before.")
        else:
            self._blit_before.append(element)
            self._blit_after.remove(element)

    def unset_blit_before(self, element):
        if not element in self._elements:
            element = self.get_elements_by_text[element]
            if len(element) > 0:
                element = element[0]
        if not element:
            raise Exception("No element found to store in blit_before.")
        self._blit_before.remove(element)
        self._blit_after.append(element)

    def get_elements(self):
        return self._elements

    def run_user_func(self):
        if self.user_func:
            functions.debug_msg("run_user_func",
                                self.user_func,
                                self.user_params)
            self.user_func(**self.user_params)

    def change_state(self, key):
        """Change state to self._states[key]"""
        self.current_state = self._states[key]
        self.current_state_key = key
        ev = pygame.event.Event(constants.THORPY_EVENT,
                                id=constants.EVENT_CHANGE_STATE,
                                el=self)
        pygame.event.post(ev)

    def set_visible(self, value):
        pass

    def clamp(self, other):
        """<other> can either be a rect or another element"""
        r = self.get_fus_rect()
        if isinstance(other, pygame.Rect):
            r.clamp_ip(other)
        else:
            r.clamp_ip(other.get_fus_rect())
        self.set_center(r.center)

    def add_state(self, key, state=None):
        """Add state"""
        if not key in self._states:
            if not state:
                state = get_void_state()
            self._states[key] = state
        else:
            raise Exception(str(key) + " is already a state.")

    def get_state(self, key=None):
        """Returns the state corresponding to key.
        Default key=None returns current state.
        """
        if not key:
            return self.current_state
        else:
            return self._states[key]

    def get_states(self):
        return self._states

    def append_element(self, e):
        if e in self._elements:
            functions.debug_msg(e, " is already in ", self)
            raise Exception("Element already in parent :", e, " is already in ", self)
        else:
            self._elements.append(e)
            self._blit_after.append(e)
            e.father = self

    def insert_element(self, e):
        if e in self._elements:
            functions.debug_msg(e, " is already in ", self)
            raise Exception("Element already in parent.")
        else:
            self._elements.insert(0, e)
            self._blit_after.insert(0, e)
            e.father = self

    def add_elements(self, elements, insert=False):
        """Use this method instead of .append, because it handles parents.
        If <insert>, use insert method instead of append, insert in first pos.

        Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        if not elements:
            return
        elif len(elements) == 1:
            self.add_element(elements[0], insert)
        else:
            if insert:
                for e in elements:
                    self.insert_element(e)
            else:
                for e in elements:
                    self.append_element(e)

    def add_element(self, e, insert=False):
        if insert:
            self.insert_element(e)
        else:
            self.append_element(e)


    def remove_elements(self, elements):
        """Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        els = tuple(elements)
        for i in range(len(els)):
            self._elements.remove(els[i])
            if els[i] in self._blit_after:
                self._blit_after.remove(els[i])
            else:
                self._blit_before.remove(els[i])
            els[i].father = None

    def remove_all_elements(self):
        """Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        while self._elements:
            self.remove_elements([self._elements[0]])

    def sort_children_by_rank(self):
        self._elements = sorted(self._elements, key=lambda x: x.rank)
        self._blit_before = sorted(self._blit_before, key=lambda x: x.rank)
        self._blit_after = sorted(self._blit_after, key=lambda x: x.rank)

    def _deny_child(self, child):
        """The difference with a normal element remove is that the child
        continues to see its father, though its father doesn't see it anymore.
        """
        if child.father is not self and child.father is not None:
            functions.debug_msg("Attention, stealing child" + str(child) +\
                                " from " + str(child.father) + " to "+str(self))
        child.father = self
        while child in self.get_elements():
            self.remove_elements([child])
        assert child not in self.get_elements()


    def unblit(self, rect=None):
        for el in self._elements:
            el.unblit(rect)

    def replace_element(self, old, new, preserve_pos=True):
        """Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu()."""
        if preserve_pos:
            pos = old.get_fus_rect().topleft
            new.set_topleft(pos)
        for i in range(len(self._elements)):
            if self._elements[i] is old:
                self._elements[i] = new
        for i in range(len(self._blit_after)):
            if self._blit_after[i] is old:
                self._blit_after[i] = new
        for i in range(len(self._blit_before)):
            if self._blit_before[i] is old:
                self._blit_before[i] = new
        #exception si existe pas!!!?

    def replace_element_by_text(self, text, new_element, preserve_pos=True):
        old = self.get_elements_by_text(text)
        if old:
            old = old[0]
        else:
            raise Exception("No element found with text: " + text)
        if preserve_pos:
            pos = old.get_fus_rect().topleft
            new_element.set_topleft(pos)
        for i in range(len(self._elements)):
            if self._elements[i].get_text() == text:
                new_element.father = self
                self._elements[i] = new_element


    def set_active(self, value):
        self.active = value


    def get_ancesters(self):
        """Returns ancester sorted by age"""
        parents = list()
        if self.father:
            parents = self.father.get_ancesters()
            parents.append(self.father)
        return parents

    def get_oldest_ancester(self):
        ancester = self.get_ancesters()
        if ancester:
            return ancester[0]
        else:
            return self

    def get_oldest_children_ancester(self):
        """Returns the oldest ancester that have a father. In other words,
        returns the oldest of self's ancesters who is itself the child of some
        element.
        """
        ancesters = self.get_ancesters()
        if ancesters:
            for a in ancesters:
                if a.father:
                    return a
        return self

    def get_descendants(self, accu=None):
        """Returns all the descendants (children) of self.
        <accu> : initial descendance (set to None for normal use).
        """
        if not accu:
            accu = []
        accu.extend(self._elements)
        for e in self._elements:
            e.get_descendants(accu)
        return set(accu)

    def react(self, event):
        if self.active:
            for reaction in self._reactions:
##                print(reaction, reaction.reac_name)
                reaction._try_activation(event)

    def get_ghost_topleft(self, state=None):
        """get topleft"""
        if not state:
            state = self.current_state_key
        return self._states[state].ghost_rect.topleft

    def get_ghost_size(self, state=None):
        """get size"""
        if not state:
            state = self.current_state_key
        return self._states[state].ghost_rect.size

    def get_ghost_center(self, state=None):
        """get center"""
        if not state:
            state = self.current_state_key
        return self._states[state].ghost_rect.center

    def get_ghost_rect(self, state=None):
        """get rect"""
        if not state:
            state = self.current_state_key
        return self._states[state].ghost_rect.copy()

    def get_storer_rect(self):
        return self.get_ghost_rect().copy()

    def get_storer_size(self):
        return self.get_storer_rect().size

    def get_storer_center(self):
        return self.get_storer_rect().center

    def get_storer_topleft(self):
        return self.get_storer_rect().topleft

    def get_rect(self, state=None):
        return self.get_fus_rect(state)

    def get_fus_rect(self, state=None):
        """get rect"""
        return self.get_ghost_rect(state)

    def get_fus_topleft(self, state=None):
        """get topleft"""
        return self.get_ghost_topleft(state)

    def get_fus_size(self, state=None):
        """get size"""
        return self.get_ghost_size(state)

    def get_fus_center(self, state=None):
        """get center"""
        return self.get_ghost_center(state)

    def move(self, shift):
        """Move all the _states with the shift"""
        for state in self._states:
            self._states[state].move(shift)
        for el in self._elements:
            el.move(shift)

    def get_fus_rects(self, state=None):
        """Returns a list containing the fus rect of all self's elements."""
        rects = []
        for e in self._blit_before:
            rects.extend(e.get_fus_rects(state))
        for e in self._blit_after:
            rects.extend(e.get_fus_rects(state))
        return rects

##    def unblit_and_reblit_func(self, func, **kwargs):
##        """Unblit and update the element, then calls a function, and finally
##        blit and update the element.
##        Faster than unblit(), update(), func(), blit(), update().
##        <func> : the function to be called before reblitting the element.
##        """
##        rects = self.get_fus_rects()
##        rect = rects[0].unionall(rects[1:]) #handle case where len(rects) = 0or1
##        func(**kwargs)
##        a = self.get_oldest_ancester()
##        a.partial_blit(exception=self, rect=rect)
##        pygame.display.update(rect)
##        self.blit()
##        self.update()

##    def unblit_and_reblit_func(self, func, **kwargs):
##        """Unblit and update the element, then calls a function, and finally
##        blit and update the element.
##        Faster than unblit(), update(), func(), blit(), update().
##        <func> : the function to be called before reblitting the element.
##        """
##        func(**kwargs)
##        a = self.get_oldest_ancester()
##        a.blit()
##        pygame.display.flip()
##
##    def unblit_and_reblit(self):
##        self.unblit()
##        self.blit()
####        self.update()
##        pygame.display.flip()

    def unblit_and_reblit_func(self, func, **kwargs):
        """Unblit and update the element, then calls a function, and finally
        blit and update the element.
        Faster than unblit(), update(), func(), blit(), update().
        <func> : the function to be called before reblitting the element.
        """
        rects = self.get_fus_rects()
        rect = rects[0].unionall(rects[1:]) #handle case where len(rects) = 0or1
        func(**kwargs)
        a = self.get_oldest_ancester()
        a.partial_blit(exception=self, rect=rect)
        pygame.display.update(rect)
        self.blit()
        self.update()

    def unblit_and_reblit(self):
        self.unblit()
        self.blit()
        self.update()

    def get_jail_rect(self):
        return None

    def set_location(self, factors, func="set_topleft",
                     state=constants.STATE_NORMAL):
        """Set the element location relatively to the windows size.

        <factors> : A couple of number in the range [0,1] that represent the
                    x and y fraction of the screen where the element has to be
                    placed.
        <func> : If you want to set the topleft location, use 'set_topleft'
                 If you want to set the center location, use 'set_center'

        One could also use any other location-setting function that can be be
        called as func((x,y)).
        """
        W, H = functions.get_screen_size()
        x = W * factors[0]
        y = H * factors[1]
        getattr(self, func)((x, y))

    def get_location(self, ref="topleft", state=constants.STATE_NORMAL):
        """Returns the element location relatively to the windows size.
        <ref> : Reference point, can be any 2D attribute of a pygame Rect.
        """
        rect = self.get_fus_rect()
        point = getattr(rect, ref)
        W, H = functions.get_screen_size()
        factor_x = float(point[0]) / W
        factor_y = float(point[1]) / H
        return (factor_x, factor_y)

    def stick_to(self, target, target_side, self_side, align=True):
        """Sides must be either 'top', 'bottom, 'left' or 'right'.
        This function moves self in order to make its <self_side> just next to
        target's <target_side>.

        Note that unless <align> = True, this does not move self along the
        orthogonal axis: e.g, stick_to(target_element, 'right', 'left') will
        move self such that self.left = target.right (using storers rects), but
        self.top might not be target.top. Then this is up to the user to move
        self on the vertical axis once self is sticked to target.

        <target> can either be an element, "screen" or a rect.
        """
        r = self.get_storer_rect()
        topleft = r.topleft
        size = r.size
        if target == "screen":
            W, H = functions.get_screen_size()
            t = Rect(0, 0, W, H)
        elif isinstance(target, Rect):
            t = target
        else:
            t = target.get_storer_rect()
        target_topleft = t.topleft
        target_size = t.size
        if target_side == "left":
            sx = topleft[0]
            tx = target_topleft[0]
            if self_side == "right":
                sx += size[0]
            self.move((tx - sx, 0))
        elif target_side == "right":
            sx = topleft[0]
            tx = target_topleft[0] + target_size[0]
            if self_side == "right":
                sx += size[0]
            self.move((tx - sx, 0))
        elif target_side == "left":
            sx = topleft[0]
            tx = target_topleft[0]
            if self_side == "right":
                sx += size[0]
            self.move((tx - sx, 0))
        elif target_side == "bottom":
            sy = topleft[1]
            ty = target_topleft[1] + target_size[1]
            if self_side == "bottom":
                sy += size[1]
            self.move((0, ty - sy))
        elif target_side == "top":
            sy = topleft[1]
            ty = target_topleft[1]
            if self_side == "bottom":
                sy += size[1]
            self.move((0, ty - sy))
        else:
            raise Exception("not possible")
        if align:
            if target_side == "top" or target_side == "bottom":
                self.set_center((t.centerx, None))
            else:
                self.set_center((None, t.centery))

    def set_topleft(self, pos, state=constants.STATE_NORMAL):
        """Set all the states'topleft to pos, using state <state> as reference.

        The values of pos that are None won't influe the new position : for
        example, set_topleft((23, None)) will place the element's left at x=23,
        ant let its top position unchanged.
        """
        x_shift = 0
        y_shift = 0
        left, top = pos
        if left is not None:
            x_shift = left - self._states[state].ghost_rect.left
        if top is not None:
            y_shift = top - self._states[state].ghost_rect.top
        self.move((x_shift, y_shift))

    def set_center_pos(self, pos, state=constants.STATE_NORMAL):
        self.set_center(pos, state)

    def set_center(self, pos, state=constants.STATE_NORMAL):
        """Set all the states'centers to pos, using state <state> as reference.

        The values of pos that are None won't influe the new position : for
        example, set_center((23, None)) will place the element's center at x=23,
        ant let its y position unchanged.
        """
        x_shift = 0
        y_shift = 0
        center_x, center_y = pos
        if center_x is not None:
##            x_shift = center_x - self._states[state].ghost_rect.centerx
            x_shift = center_x - self.get_storer_rect().centerx
        if center_y is not None:
##            y_shift = center_y - self._states[state].ghost_rect.centery
            y_shift = center_y - self.get_storer_rect().centery
        self.move((x_shift, y_shift))

    def collide(self, pos, state=constants.STATE_NORMAL):
        """Returns True if <pos> is inside self's rect, for state <state>."""
        rect = self.get_ghost_rect(state)
        if self._jail:
            jail_rect = self._jail.get_fus_rect()
            rect = rect.clip(jail_rect)
        return rect.collidepoint(pos)

    def get_reaction(self, reaction_name):
        for r in self._reactions:
            if r.reac_name == reaction_name:
                return r

    def get_reaction_by_event_type(self, event_type):
        for r in self._reactions:
            if r.reacts_to == event_type:
                return r



    def add_reaction(self, reaction, index=None):
        """If reaction's name is not None and already exists in self._reactions,
        it will be replaced. Otherwise the reaction is appended to
        self._reactions.

        Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        if reaction.reac_name is None:
            self._reactions.append(reaction)
        else:
            index_reaction = None
            for (i, r) in enumerate(self._reactions):
                if r.reac_name == reaction.reac_name:
                    functions.debug_msg("Reaction conflict:", r.reac_name)
                    index_reaction = i
                    break
            if index_reaction is None:
                self._reactions.append(reaction)
            else:
                self._reactions[index_reaction] = reaction
        if index:
            if index == -1:
                index = len(self._reactions)
            self.set_reaction_index(index, reaction)

    def add_reactions(self, reactions):
        """<reactions> : a list of Reactions or ConstantReactions instances.
        If reaction's name is not None and already exists in self._reactions,
        it will be replaced. Otherwise the reaction is appended to
        self._reactions.

        Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        for reaction in reactions:
            self.add_reaction(reaction)

    def recursive_deactivate_all_reactions(self):
        self.deactivate_all_reactions()
        for e in self.get_descendants():
            e.deactivate_all_reactions()

    def deactivate_all_reactions(self):
        for reaction in self._reactions:
            reaction.event = -1

    def deactivate_reaction(self, reaction):
        if not isinstance(reaction, Reaction):
            reac = self.get_reaction(reaction)
            if not reac:
                raise Exception("No reaction with name '" + str(reaction) +\
                                "' found while deactivating reaction.")
            reaction = reac
        reaction.reacts_to = -1

    def set_reaction_index(self, index, reaction):
        if not isinstance(reaction, Reaction):
            reaction = self.get_reaction(reaction)
        self.remove_reaction(reaction)
        self._reactions.insert(index, reaction)

    def remove_reaction(self, reaction):
        """Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        if not isinstance(reaction, Reaction):
            reaction = self.get_reaction(reaction)
        self._reactions.remove(reaction)

    def remove_all_reactions(self):
        """Remember : if you want the changes to affect the current menu,
        call thorpy.functions.refresh_current_menu().
        """
        self._reactions = []

    def set_ghost_rect(self, topleft, size, state=None):
        if state is None:
            for state in self._states:
                self._states[state].set_ghost_rect(topleft, size)
        else:
            self._states[state].set_ghost_rect(topleft, size)

    def redraw(self, *args):
        pass


    def _set_last(self):
        """Set self as last element of father's elements. If self is in the
        blit_before, then it will stay in blit_before. Else it will stay in
        blit_after. In both cases, it will also be the last element.
        If self has no father, do nothing.
        """
        if self.father:
            father = self.father
            before = False
            if self in father._blit_before:
                before = True
            father.remove_elements([self])
            father.add_elements([self])
            if before:
                father.set_blit_before(self)

    def _set_branch_last(self):
        self._set_last()
        if self.father:
            self.father._set_last()

# *********** BLITTING FUNCTIONS **************
    def blit(self):
        """Not to blit itself, but childrens"""
        for e in self._blit_before:
            e.blit()
        for e in self._blit_after:
            e.blit()

    def partial_blit(self, exception, rect):
        """Blit only parts that are within <rect>."""
        for e in self._blit_before:
            if not(exception == e):
                e.partial_blit(exception, rect)
        if self.visible:
            if not (exception == self):
                self._clip_screen(rect)
                self.solo_blit()
                self._unclip_screen()
        for e in self._blit_after:
            if not(exception == e):
                e.partial_blit(exception, rect)


    def _blit_debug(self, tim=0, ghost=True, fus=True, stor=True):
        """
        draw rects, flip screen and eventually sleep.
        red : storer
        green : ghost
        blue : fusionner
        """
        if stor:
            pygame.draw.rect(self.surface, (255, 0, 0), self.get_storer_rect())
        if ghost:
            pygame.draw.rect(self.surface, (0, 255, 0), self.get_ghost_rect())
        if fus:
            pygame.draw.rect(self.surface, (0, 0, 255), self.get_fus_rect())
        pygame.display.flip()
        if tim > 0:
            import time
            time.sleep(tim)

    def _recurs_blit_debug(self, tim=0, ghost=True, fus=True, stor=True,
                           exception=None, screenshot=True):
        if exception == None:
            self._blit_debug(tim, ghost, fus, stor)
        for e in self._elements:
            e._recurs_blit_debug(tim, ghost, fus, stor, None, False)
        if screenshot:
            functions.get_current_application().update()
            functions.get_current_application().save_screenshot()

    def update(self):
        """Recursive update of self's elements, i.e the elements themselves will
        call this function to update their own children.
        """
        for e in self._elements:
            e.update()

    def solo_update(self):
        """Updates only self.get_fus_rect()."""
        pygame.display.update(self.get_fus_rect())

# *********** END OF BLITTING FUNCTIONS **************

    def get_family_rect(self, state=None, only_children=False):
        if not state:
            state = self.current_state_key
        dr = [e.get_fus_rect(state) for e in self.get_descendants() if e.visible and e._is_in_family]
        if not dr:
            return pygame.Rect(0,0,0,0)
        else:
            if only_children:
                return dr[0].unionall(dr)
            else:
                return self._states[state].ghost_rect.unionall(dr)

    def fit_children(self, state=None):
        """Scale ghost_rect to englobe childrens."""
        if state is None:
            for state in self._states:
                Ghost.fit_children(self, state)
        else:
            fr = self.get_family_rect(state)
            self.set_ghost_rect((fr.x, fr.y), (fr.w, fr.h), state=state)

    def set_recursive(self, attribute, value):
        """Recursive set of <attribute> to <value>, for self and all self's
        elements. All childrens must have <attribute> in their attributes"""
        self.__setattr__(attribute, value)
        for e in self._elements:
            e.set_recursive(attribute, value)

    def call_recursive(self, func, dict_params):
        """Recursive call of the method <func> called with params <dict_params>,
        for self and all self's elements.
        """
        self.func(**dict_params)
        for e in self._elements:
            e.call_recursive(func, dict_params)

    def set_as_exiter(self):
        """Set the effect of self as a program exiter."""
        self.user_func = functions.quit_func

    def set_as_menu_exiter(self):
        """Set the effect of self as a current menu exiter."""
        self.user_func = functions.quit_menu_func

    def center(self, x_shift=None, y_shift=None, element=None,
               axis=(True, True)):
        """Centers self's center on <element>'s center.

        If <element> = None, center self on self.surface's center.

        Optionnal shift arguments can be passed in order to shift self after
        centering.

        Optionnal axis argument can be passed, on the form (bool, bool), and
        is used to filter the centering. The components whose axis have False
        value will be unchanged.
        """
        if not element:
            center = self.surface.get_rect().center
        elif element == "screen":
            center = functions.get_screen().get_rect().center
        else:
            center = element.get_storer_center()
        x = center[0]
        y = center[1]
        if x_shift is not None:
            x += x_shift
        if y_shift is not None:
            y += y_shift
        if not axis[0]:
            x = None
        if not axis[1]:
            y = None
        self.set_center((x, y))

    def recenter(self, x=True, y=False):
        """Recenter self on self.father"""
        if self.father:
            self.center(element=self.father, axis=(x,y))
        else:
            self.center(axis=(x,y))

    def storage_center(self, x_shift=None, y_shift=None, element=None,
                       axis=(True,True)):
        """Centers self's center on <element>'s center using self's storer rect.

        If <element> = None, center self on self.surface's center.

        Optionnal shift arguments can be passed in order to shift self after
        centering.

        Optionnal axis argument can be passed, on the form (bool, bool), and
        is used to filter the centering. The components whose axis have False
        value will be unchanged.
        """
        if not element:
            center = self.surface.get_rect().center
        else:
            center = element.get_storer_center()
        x = center[0]
        y = center[1]
        if x_shift:
            x += x_shift
        if y_shift:
            y += y_shift
        storage_set_center(self, (x, y))

    def freeze(self):
        """Save memory by deleting fusionner's painter and writer.
        This means that the element aesthetics will not be modifiable after the
        call of this function."""
        for state in self._states:
            self._states[state].fusionner.painter = None
            self._states[state].fusionner.title._writer = None

    def recursive_freeze(self):
        """Like self.freeze, but doing this also for all descendants."""
        self.freeze()
        for e in self._elements:
            e.freeze()

    def get_text(self):
        return ""

    def get_full_txt(self):
        return self.normal_params.params.get("txt", "")

    def get_elements_by_text(self, text):
        """Returns all self's element whose text is <text>."""
        return [e for e in self.get_elements() if e.get_text() == text]

    def get_element_by_id(self, id_):
        for e in self.get_elements():
            if e.id == id_:
                return e

    def get_descendant_by_id(self, id_):
        for e in self.get_descendants():
            if e.id == id_:
                return e

    def infos(self):
        text = self.get_text()
        if text.startswith("no name : "):
            text = "<No text>"
        return "*** Element Description: ***" + "\n" +\
                "Class: " + str(self.__class__) + "\n" +\
                "Adress: " + str(self) + "\n" +\
                "Text: " + text + "\n" +\
                "ID: " + str(self.id)

    def store(self, autosize=True):
        storer = Storer(self)
        if autosize:
            storer.autoset_framesize()
        else:
            storer.center()

    def set_jailed(self, jail):
        pass

    def get_help_rect(self):
        return self.get_ghost_rect()

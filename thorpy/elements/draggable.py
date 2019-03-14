"""
Clickable element that can be dragged with the mouse.
"""

from pygame.locals import MOUSEMOTION
from pygame.event import post, Event

from thorpy.elements.clickable import Clickable
from thorpy.elements.togglable import Togglable
##from thorpy.painting.mousecursor import change_cursor
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, style


class BasicDraggable(object):

    def set_free(self, x=1., y=1.):
        if x:
            x = 1.
        else:
            x = 0.
        if y:
            y = 1.
        else:
            y = 0.
        self._constraints = (x, y)

    def _drag_move(self, event):
        ev_drag = Event(constants.THORPY_EVENT, id=constants.EVENT_DRAG, el=self)
        post(ev_drag)
        self.move((self._constraints[0] * event.rel[0],
                   self._constraints[1] * event.rel[1]))

    def _reaction_drag_transp(self, event):
        self.unblit_and_reblit_func(func=self._drag_move, event=event)

class Draggable(Clickable, BasicDraggable):
    """Clickable that can be dragged/dropped."""

    #Inherits from Togglable not for graphical, but logical reasons :
    #   _hover and _press reactions.

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None, finish=True):
        """Clickable that can be dragged/dropped."""
        super(Draggable, self).__init__(text, elements, normal_params,
                                        press_params, finish=False)
        # not polite set, because of standard _press painter args
        self.press_params.params["painter args"] = {"pressed": False,
                                                    "size": style.SIZE}
        reac_motion = Reaction(MOUSEMOTION, self._reaction_drag,
                               reac_name=constants.REAC_MOTION)
        self.add_reaction(reac_motion)
        self._constraints = (1., 1.)
        if finish:
            self.finish()


    def _reaction_drag(self, event):
        if self.current_state_key == constants.STATE_PRESSED:
            self._reaction_drag_transp(event)


class ClickDraggable(Togglable, BasicDraggable):
    """Togglable clickable that can be dragged/dropped according to its state
    pressed/unpressed.
    """
    #Inherits from Togglable not for graphical, but logical reasons :
    #   _hover and _press reactions.

    def __init__(self, text="", elements=None, normal_params=None,
                 press_params=None):
        """Togglable clickable that can be dragged/dropped according to its state
        pressed/unpressed.
        """
        super(ClickDraggable, self).__init__(text, elements, normal_params,
                                        press_params)
        # not polite, because of standard _press painter args
        self.press_params.params["painter args"] = {"pressed": False,
                                                    "size": style.SIZE}
        reac_motion = Reaction(MOUSEMOTION, self._reaction_drag,
                               reac_name=constants.REAC_MOTION)
        self.add_reaction(reac_motion)
        self._constraints = (1., 1.)


    def _reaction_drag(self, event):
        if self.current_state_key == constants.STATE_PRESSED:
            self._reaction_drag_transp(event)

##    @staticmethod
##    def set_draggable(element, normal_params=None):
##        """self.imgs[ONE_STATE] is the hovering img to place when hovering element
##        while it is in state ONE_STATE. In that case, self.current_state.img =
##        self._imgs[ONE_STATE]. When unhovering, the self._normal_imgs[ONE_STATE] is
##        recovered in self.current_state.img.
##
##        Note that at initialization, two fusions are used in standard hovering :
##        one for getting _hovered image, another"""
##        from thorpy._utils.functions import fusion_dicts
##        draggable = ClickDraggable(normal_params=normal_params)
##        d = fusion_dicts(element.__dict__, draggable.__dict__)
##        draggable.__dict__ = d
##        reac_motion = Reaction(MOUSEMOTION, draggable._reaction_drag,
##                               name=REAC_MOTION)
##        draggable.add_reaction(reac_motion)
##        return draggable

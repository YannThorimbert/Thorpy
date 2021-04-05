from thorpy.elements.element import Element
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui.initializer import Initializer
from thorpy.miscgui.state import State
from thorpy.miscgui import constants, parameters, style, painterstyle

class _Cursor(Element):

    def __init__(self,
                 father,
                 fact=None,
                 thickness=None,
                 color=None):
        fact = style.CURS_FACT if fact is None else fact
        thickness = style.CURS_THICK if thickness is None else thickness
        color = style.CURS_COLOR if color is None else color
        self.father = father
        self._fact = fact  # should be 0 if img is used
        cursor_size = (thickness, self._fact*self.father._iwriter.get_zone().h)
        normal_painter = painterstyle.CURSOR_PAINTER(size=cursor_size,
                                                     color=color)
        timed_painter = painterstyle.CURSOR_PAINTER(
            size=cursor_size,
            color=constants.TRANSPARENT)
        super(_Cursor, self).__init__(finish=False)
        self.normal_params.params["painter"] = normal_painter
        self.time_params = Initializer()
        self.time_params.params["painter"] = timed_painter
        reac_time = Reaction(constants.THORPY_EVENT,
                             self._reaction_time,
                             {"id":constants.EVENT_TIME},
                             reac_name=constants.REAC_TIME)
        self.add_reaction(reac_time)
        self.switch_time = parameters.CURSOR_INTERVAL  # switch time in ms
        self._switch = 0  # time [ms] from last state switch
        self._activated = False
        self._original_blit = self.blit
        self.init_space = 0

    def finish(self):
        Element.finish(self)
        time_state = State(self.time_params.get_fusionner())
        self.add_state(constants.REAC_TIME, time_state)
        self.set_init_pos()
        self.change_state(constants.REAC_TIME)

    def exit(self):
        self._activated = False
        self.change_state(constants.REAC_TIME)
        self.unblit()
        self.update()

    def set_topleft(self, pos, state=constants.STATE_NORMAL):
        left, top = pos
        w = self._states[state].fusionner.rect.width
        zone = self.father._iwriter.get_zone()
        if left + w > zone.right:
            left = zone.right - w
        Element.set_topleft(self, (left, top), state)

    def set_init_pos(self):
        """Set cursor to initial position"""
        pos = self.father._iwriter._get_cursor_pos()
        zone = self.father._iwriter.get_zone()
        x = pos[0] + self.init_space
        y = zone.y + (1. - self._fact) / 2 * zone.h
        self.set_topleft((x, y))

##    def switch_state(self):
##        """Switch REAC_TIME and STATE_NORMAL states"""
##        if self.current_state_key == constants.REAC_TIME:
##            self.change_state(constants.STATE_NORMAL)
##            self.solo_blit()
##        else:
##            self.change_state(constants.REAC_TIME)
##            r = self.get_fus_rect()
##            self.father.unblit(r)
##            self.father.partial_blit(self, r)
##        self.solo_update()

    def switch_state(self):
        """Switch REAC_TIME and STATE_NORMAL states"""
        if self.current_state_key == constants.REAC_TIME:
            self.change_state(constants.STATE_NORMAL)
        else:
            self.change_state(constants.REAC_TIME)
        self.father.unblit()
        self.father.blit()
        self.father.update()

    def _reaction_time(self, event):
        """Reaction to EVENT_TIME event"""
        if self._activated:
            self._switch += event.tick
            if self._switch > self.switch_time:  # then must switch
                self._switch = 0
                self.switch_state()

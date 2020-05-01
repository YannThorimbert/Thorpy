"""Inserter"""
# ! to forbid other element to react during insert, they should not be in
# the same menu as the inserter, and maybe use _hide_mouse = True

from pygame import event, K_ESCAPE, K_RETURN, K_BACKSPACE, KEYDOWN, K_LEFT, K_RIGHT
from pygame.mouse import set_visible as mouse_set_visible
from pygame.key import set_repeat as key_set_repeat

from thorpy.elements.clickable import Clickable
from thorpy.elements._inserterutils._insertwriter import _InsertWriter
from thorpy.elements._inserterutils._cursor import _Cursor
from thorpy.painting.mousecursor import change_cursor
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui.keyer import Keyer
from thorpy.miscgui import constants, functions, parameters, style, painterstyle

class Inserter(Clickable):
    """Element fo text insertion."""

    @staticmethod
    def make(name="", elements=None, value="", size=(None,None)):
        i = Inserter(name, elements, value=value, size=size,finish=False)
        i.finish()
        return i

    def __init__(self,
                 name="",
                 elements=None,
                 normal_params=None,
                 press_params=None,
                 value="",
                 size=(None, None),
                 namestyle=None,
                 varlink_func=None,
                 quit_on_click=False,
                 value_type=str,
                 finish=True):
        """Element fo text insertion.
        <name>: text of the title before the inserter.
        <value>: initial text inside the inserter.
        <size>: if not (None,None), a 2-tuple specifying the size of the text
            insertion zone.
        <quit_on_click>: if True, make the inserter lose focus when mouse click
            outside its area.
        """
        namestyle=style.STYLE_INSERTER_NAME if namestyle is None else namestyle
        if size[0] is None:
            s0 = style.SIZE[0]
        else:
            s0 = size[0]
        if size[1] is None:
            s1 = style.Y_SMALL_SIZE
        else:
            s1 = size[1]
        size = (s0, s1)
        self.cursor = None
        super(Inserter, self).__init__("", elements, normal_params,
                                       press_params,finish=False)
        self._name_element = self._get_name_element(name, namestyle)
        self.add_elements([self._name_element])
        self._iwriter = _InsertWriter(value)
        self.add_elements([self._iwriter])
        self.quit_on_click = quit_on_click
        self._value_type = value_type
        painter = functions.obtain_valid_painter(painterstyle.INSERTER_PAINTER,
                                                 color=style.DEF_COLOR2,
                                                 pressed=True,
                                                 size=(s0,s1))
        self.set_painter(painter)
        self.normal_params.polite_set("states hover",
                                      [constants.STATE_NORMAL,
                                       constants.STATE_PRESSED])
        self.press_params.polite_set("states hover",
                                     [constants.STATE_NORMAL,
                                      constants.STATE_PRESSED])
        self._activated = False
        self._value = value
        self._inserted = self._value
        self._cursor_index = len(self._inserted)
        reac_keypress = Reaction(KEYDOWN, self._reaction_keydown,
                                 reac_name=constants.REAC_KEYPRESS)
        self.add_reaction(reac_keypress)
        self._keyer = Keyer()
        self._hide_mouse = self.normal_params.params.get("hide mouse", False)
        self._varlink_func = varlink_func
        self.repeat_delay = parameters.KEY_DELAY
        self.repeat_interval = parameters.KEY_INTERVAL
        self.deactivate_on_focus = []
        self.auto_resize = True
        self.numeric_only = False
        self.int_only = False
        if finish:
            self.finish()

    def set_key_repeat(delay, interval):
        """Set delay to None for no repeat."""
        self.repeat_delay = delay
        self.repeat_interval = interval

    def make_small_enough(self, word):
        while not self._iwriter._is_small_enough(word) and word:
            word = word[:-1]

    def finish(self):
        Clickable.finish(self)
        # cursor is initialized in finish because _iwriter needs self.fusionner
        #   to initialize...
        self.make_small_enough(self._inserted)
        if not self._iwriter._is_small_enough(self._inserted):
            functions.debug_msg("Inserter is too small for value", self._inserted)
            if self.auto_resize:
                self.set_size(self._iwriter.get_rect().inflate((2,2)).size)
        self._iwriter.refresh_img()
        self.cursor = _Cursor(self)
        self.add_elements(list([self.cursor]))
        self._refresh_pos()
        self.cursor.finish()
        self._name_element.user_func = self.enter

    def scale_to_title(self, **kwargs):
        pass

    def fit_children(self, **kwargs):
        pass

    def _get_name_element(self, name, namestyle):
        painter = functions.obtain_valid_painter(
            painterstyle.INSERTER_NAME_PAINTER,
            size=style.SIZE)
        el = Clickable(name,finish=False)
        el.set_painter(painter)
        if namestyle:
            el.set_style(namestyle)
        el.finish()
        return el

    def unblit(self, rect=None):
        self._name_element.unblit(rect)
        Clickable.unblit(self, rect)

    def _hover(self):
        Clickable._hover(self)
        change_cursor(constants.CURSOR_TEXT)

    def _unhover(self):
        if not self._activated:
            Clickable._unhover(self)
        change_cursor(constants.CURSOR_NORMAL)

    def transp_blit(self):
        a = self.get_oldest_children_ancester()
        r = self.get_storer_rect()
        a.unblit(r)
        a.partial_blit(None, r)

    def K_RETURN_pressed(self):
        if self._activated:
            self._value = self._inserted
            self.exit()
            functions.debug_msg("'" + self._inserted + "'", " inserted")

    def _reaction_keydown(self, pygame_event):
        if self._activated:
            if pygame_event.type == KEYDOWN:
                if pygame_event.key == K_ESCAPE:
                    self.exit()
                elif pygame_event.key == K_RETURN:  # way to exit saving insertion
                    self.K_RETURN_pressed()
                elif pygame_event.key == K_BACKSPACE:
                    if self._cursor_index > 0:
                        before = self._inserted[0:self._cursor_index-1]
                        after = self._inserted[self._cursor_index:]
                        self._inserted = before + after
                        self._cursor_index -= 1
                        self._urbu()
                # if this is a modifier, the next char will be handled by the
                # keyer...
                elif pygame_event.key == K_LEFT:
                    if self._cursor_index > 1:
                        self._cursor_index -= 1
                        self._urbu()
                elif pygame_event.key == K_RIGHT:
                    if self._cursor_index < len(self._inserted):
                        self._cursor_index += 1
                        self._urbu()
                elif not pygame_event.key in self._keyer.modifiers:
                    char = self._keyer.get_char_from_key(pygame_event.key)
                    if self.numeric_only:
                        if self.int_only and not char.isnumeric():
                            return
                        elif not(char.isnumeric()) and char != ".":
                            return
                    before = self._inserted[0:self._cursor_index]
                    after = self._inserted[self._cursor_index:]
                    new_word = before + char + after
                    if self._iwriter._is_small_enough(new_word):
                        self._inserted = new_word
                        self._cursor_index += 1
                        self._urbu()

    def _urbu(self, graphical=True):
        """Unblit, Refresh cursor pos, Blit, Update.
        Returns True if the text img has been refreshed.
        """
##        a = self.get_oldest_children_ancester()
##        r = self.get_storer_rect()
##        a.unblit(r)
        if graphical:
            self.unblit()
        txt_refreshed = self._refresh_cursor_pos()  # refreshes iwriter's img!
##        a.partial_blit(None, r)
        if graphical:
            self.blit()
            self.update()
        return txt_refreshed

    def _reaction_press(self, pygame_event):
        Clickable._reaction_press(self, pygame_event)
        if self.current_state_key == constants.STATE_PRESSED:
            self.enter()
        elif self._activated:
            if not self.quit_on_click:
                self._value = self._inserted
            self.exit()

    def enter(self):
        for e in self.deactivate_on_focus:
            e.active = False
        functions.debug_msg("Entering inserter ", self)
        if self.repeat_delay is not None:
            key_set_repeat(self.repeat_delay, self.repeat_interval)
        if self._hide_mouse:
            mouse_set_visible(False)
        self._activated = True
        self.cursor._activated = True

    def focus(self): #alias for enter
        self.enter()

    def exit(self):
        key_set_repeat(parameters.KEY_DELAY, parameters.KEY_INTERVAL)
        if self._activated:
            functions.debug_msg("Leaving inserter ", self)
            self._inserted = self._value
            self._urbu()
            mouse_set_visible(True)
            self.cursor.exit()
            self._activated = False
            event_quit = event.Event(constants.THORPY_EVENT,
                                   id=constants.EVENT_INSERT,
                                   el=self,
                                   value=self._value)
            event.post(event_quit)
            change_cursor(constants.CURSOR_NORMAL)
            if self._varlink_func:
                self._varlink_func(self._value)

        for e in self.deactivate_on_focus:
            e.active = True

    def _refresh_cursor_pos(self):
        """Refresh position of the cursor. Used when inserted text changes.
        Also refreshes iwriter's image! Is used through self._urbu().
        Returns True if the text img has been refreshed.
        """
        txt_refreshed = True
        if self._iwriter.refresh_img() == -1:  # text too large
            txt_refreshed = False
            self._inserted = self._inserted[:-1]
        pos = self._iwriter._get_cursor_pos()
        self.cursor.set_topleft(pos)
        return txt_refreshed

    def _refresh_pos(self):
        """Refresh position of the whole element."""
        self._iwriter._refresh_pos()
        l = self.get_fus_topleft()[0]
        (x, y) = self.get_fus_center()
        l -= self._name_element.get_fus_size()[0] + style.NAME_SPACING
        self._name_element.set_center((None, y))
        self._name_element.set_topleft((l, None))

    def get_storer_rect(self):
        return self.get_family_rect(constants.STATE_NORMAL)

    def get_value(self):
        try:
            return self._value_type(self._inserted)
        except ValueError:
            functions.debug_msg("type of self._inserted is not " + \
                                str(self._value_type))
            return self._value_type()

    def set_value(self, value, refresh_draw=False):
        self.make_small_enough(value)
        if self._iwriter._is_small_enough(value):
            self._inserted = value
            self._cursor_index = len(value)
            self._urbu(graphical=refresh_draw)
        else:
            self.set_size(self._iwriter.get_rect().size)
            #raise Exception("Cannot insert value in inserter:", value)

    def set_font_color(self, color, state=None, center_title=True):
        """set font color for a given state"""
        Clickable.set_font_color(self, color, state, center_title)
        self._name_element.set_font_color(color, state, center_title)

    def set_font_size(self, size, state=None, center_title=True):
        """set font color for a given state"""
        Clickable.set_font_size(self, size, state, center_title)
        self._name_element.set_font_size(size, state, center_title)

    def set_iwriter_font_size(self, size, state=None, center_title=True):
        self._iwriter.set_font_size(size, state, center_title)

    def set_font(self, fontname, state=None, center_title=True):
        """set font for a given state"""
        Element.set_font(self, fontname, state, center_title)
        self.set_hovered_states(self._states_hover)

    def set_font_effects(self, biu, state=None, center=True, preserve=False):
        """biu = tuple : (bold, italic, underline)"""
        CLickable.set_font_effects(self, bio, state, center, preserve)
        self._name_element.set_font_effects(biu, state, center, preserve)

    def get_help_rect(self):
        return self._name_element.get_help_rect()

    def get_text(self):
        return self._name_element.get_text()

    def set_active(self, value):
        self.active = value #deactivate text insertion
        self.cursor.active = value #deactivate cursor
        self._name_element.active = value #deactivate hoverable title

    def set_visible(self, value):
        self.visible = value #deactivate text insertion
        self.cursor.visible = value #deactivate cursor
        self._name_element.visible = value #deactivate hoverable title

##    def reac_click(self, e):


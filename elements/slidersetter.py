from thorpy.elements.ghost import Ghost
from thorpy.elements.slider import _SliderXSetter
from thorpy.elements.element import Element
from thorpy.miscgui import functions, style, painterstyle
from thorpy.miscgui import storage


class SliderXSetter(Ghost):
    """Set of text, slider and value"""

    @staticmethod
    def make(length, limvals=None, text="", type_=float, initial_value=None):
        s = SliderXSetter(length, limvals, text, initial_value=initial_value,
                            type_=type_, finish=False)
        s.finish()
        return s

    def __init__(self,
                 length,
                 limvals=None,
                 text="",
                 elements=None,
                 normal_params=None,
                 namestyle=None,
                 valuestyle=None,
                 type_=float,
                 initial_value=None,
                 finish=True):
        """Slider for choosing a value.
        <length>: single int value specifying the length of slider in pixels.
        <limvals>: 2-tuple specifying the min and max values.
        <text>: text preceeding the element.
        <type_>: the type of the number to be chosen (e.g int or float)
        <initial_value>: the initial value. If None, set to minimum value.
        """
        namestyle = style.STYLE_SLIDER_NAME if namestyle is None else namestyle
        valuestyle=style.STYLE_SLIDER_VALUE if valuestyle is None else valuestyle
        Ghost.__init__(self, elements, normal_params, finish=False)
        self._slider_el=_SliderXSetter(length, limvals, "",
                                        initial_value=initial_value)
        self.add_elements([self._slider_el])
        self._value_type = type_
        self._round_decimals = 2
        self._name_element = self._get_name_element(text, namestyle) #herite de setter
        self._value_element = self._get_value_element(valuestyle)
        self.add_elements([self._name_element, self._value_element])
        self._name_element.rank = 1
        self._slider_el.rank = 2
        self._value_element.rank = 3
        self.sort_children_by_rank()
        self._storer_rect = None
        self._refresh_pos()
        self.limvals = self._slider_el.limvals
        if finish:
            self.finish()

    def finish(self):
        Ghost.finish(self)
        self._refresh_pos()
        self._slider_el._drag_element.set_setter()
        value = str(self._slider_el.get_value())
        self._value_element.set_text(value)

    def set_font_color(self, color):
        self._name_element.set_font_color(color)

    def set_font_size(self, size):
        self._name_element.set_font_size(size)

    def set_value(self, value):
        self._slider_el.get_dragger().place_at(value)
        self.refresh_value()

    def show_value(self, show_value):
        self._value_element.visible = show_value

    def _get_name_element(self, name, namestyle):
        painter = functions.obtain_valid_painter(
            painterstyle.CHECKER_NAME_PAINTER,
            size=style.SIZE)
        el = Element(name,finish=False)
        el.set_painter(painter)
        if namestyle:
            el.set_style(namestyle)
        el.finish()
        return el

    def _get_value_element(self, valuestyle):
        painter = functions.obtain_valid_painter(
            painterstyle.CHECKER_VALUE_PAINTER,
            size=style.CHECK_SIZE)
        el = Element(str(self.get_value()),finish=False)
        el.set_painter(painter)
        if valuestyle:
            el.set_style(valuestyle)
        el.finish()
        return el

    def _refresh_pos(self):
        storage.store(self, mode="h")
        self.fit_children()

    def refresh_value(self):
        self._value_element.unblit()
        self._value_element.update()
        value = str(self.get_value())
        self._value_element.set_text(value)
        self._value_element.blit()
        self._value_element.update()

    def get_value(self):
        value = self._slider_el.get_value()
        return self._value_type(value)

    def get_storer_rect(self): #!!! normalement rien besoin
        tmp = self.get_value()
        self._value_element.set_text(str(self._slider_el.limvals[1]))
        rect = self.get_family_rect()
        self._value_element.set_text(str(tmp))
        return rect

    def get_slider(self):
        return self._slider_el

    def get_dragger(self):
        return self.get_slider().get_dragger()

##    def set_font_color(self, color, state=None, center_title=True):
##        """set font color for a given state"""
##        self._name_element.set_font_color(color, state, center_title)
##
##    def set_font_size(self, size, state=None, center_title=True):
##        """set font size for a given state"""
##        SliderX.set_font_size(self, size, state, center_title)
##        self._name_element.set_font_size(size, state, center_title)
##
##    def set_font_effects(self, biu, state=None, center=True, preserve=False):
##        """biu = tuple : (bold, italic, underline)"""
##        SliderX.set_font_effects(self, bio, state, center, preserve)
##        self._name_element.set_font_effects(biu, state, center, preserve)

##    def pix_to_val(self, pix, x0): #!!!!!
##        value = SliderX.pix_to_val(self, pix, x0)
##        if self._value_type is float:
##            return round(value, self._round_decimals)
##        elif self._value_type is int:
##            return int(round(value))

    def get_help_rect(self):
        return self._name_element.get_help_rect()

    def set_active(self, value):
        self.active = value
        self._slider_el.set_active(value)
        self._slider_el._drag_element.set_active(value)

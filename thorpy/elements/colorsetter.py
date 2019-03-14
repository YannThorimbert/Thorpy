from thorpy.elements.box import Box
from thorpy.elements.element import Element
from thorpy.elements.slidersetter import SliderXSetter
from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui.reaction import ConstantReaction
from thorpy.miscgui import painterstyle
from thorpy.miscgui import constants, functions

def get_example_element(color, size):
    painter_frame = functions.obtain_valid_painter(painterstyle.DEF_PAINTER,
                                                   pressed=True,
                                                   size=size)
    if painter_frame.clip:
        color_size = painter_frame.clip.size
    else:
        color_size = size
    painter_example = BasicFrame(size=color_size, color=color)
    example = Element(finish=False)
    example.set_painter(painter_example)
    example.finish()
    frame = Element(elements=[example],finish=False)
    frame.set_painter(painter_frame)
    frame.finish()
    example.set_center(frame.get_fus_center())
    return frame


class ColorSetter(Box):
    """Box in which three sliders and a visualization square provide a way to
    define a color."""

    @staticmethod
    def make(text="", elements=None, size=None, color_size=(50,50),
                value=(255,0,0)):
        cs = ColorSetter(text, elements, size=size, color_size=color_size,
                        value=value, finish=False)
        cs.finish()
        return cs


    def __init__(self,
                 text="",
                 elements=None,
                 normal_params=None,
                 storer_params=None,
                 size=None,
                 put_lift=True,
                 color_size=(50, 50),
                 value=(255, 0, 0),
                 color_limvals=(0, 255),
                 finish=True):
        """Box in which three sliders and a visualization square provide a way to
        define a color.
        <text>: title text for the color box.
        <size>: if not None, force the size of the box.
        <color_size>: the size of the color visualization rect.
        <value>: 3-tuple defining the initial color value.
        """
        Box.__init__(self, elements, normal_params, storer_params, size,
                     put_lift, finish=False)
        self._color_size = color_size
        self._r_element = SliderXSetter(100, text="R: ", type_=int,
                               limvals=color_limvals, initial_value=value[0])
        self._r_element.finish()
        self._g_element = SliderXSetter(100, text="G: ", type_=int,
                               limvals=color_limvals, initial_value=value[1])
        self._g_element.finish()
        self._b_element = SliderXSetter(100, text="B: ", type_=int,
                               limvals=color_limvals, initial_value=value[2])
        self._b_element.finish()
        reac_red= ConstantReaction(constants.THORPY_EVENT,
                                   self.refresh,
                                   {"id":constants.EVENT_SLIDE,
                                    "el":self._r_element},
                                   reac_name="setcolorred")
        reac_green= ConstantReaction(constants.THORPY_EVENT,
                                     self.refresh,
                                     {"id":constants.EVENT_SLIDE,
                                      "el":self._g_element},
                                     reac_name="setcolorgreen")
        reac_blue= ConstantReaction(constants.THORPY_EVENT,
                                    self.refresh,
                                    {"id":constants.EVENT_SLIDE,
                                     "el":self._b_element},
                                    reac_name="setcolorblue")
        self.add_reactions([reac_red, reac_green, reac_blue])
        self._example_element = get_example_element(value, color_size)
        self.add_elements([self._r_element, self._g_element, self._b_element,
                           self._example_element])
        if finish:
            self.finish()


    def get_color(self):
        r = self._r_element.get_value()
        g = self._g_element.get_value()
        b = self._b_element.get_value()
        return (r, g, b)

    def refresh(self):
##        print("setting color", self.get_color())
        self._example_element._elements[0].set_main_color(self.get_color())
        self._example_element._elements[0].blit()
        self._example_element._elements[0].update()

    def get_value(self):
        return self.get_color()

    def set_value(self, new_color):
        self._r_element.set_value(new_color[0])
        self._g_element.set_value(new_color[1])
        self._b_element.set_value(new_color[2])
        self._example_element._elements[0].set_main_color(new_color)

    def store(self, size=None):
        Box.store(self, size)
        left = min([e.get_fus_rect().left for e in [self._r_element,
                                                    self._g_element,
                                                    self._b_element]])
        self._r_element.set_topleft((left,None))
        self._g_element.set_topleft((left,None))
        self._b_element.set_topleft((left,None))

    def get_help_rect(self):
        return self._example_element.get_help_rect()


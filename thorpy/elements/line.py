from thorpy.elements.element import Element
from thorpy.painting.painters.classicframe import ClassicFrame

class Line(Element):
    """Vertical or horizontal graphical separation Line."""

    @staticmethod
    def make(size, type_="h", color=None, pressed=True):
        """Vertical or horizontal graphical separation Line.
        <size>: the size in pixel (single int value).
        <type>: either 'horizontal', 'h' or 'vertical', 'v'.
        <color>: a 3 or 4-tuple specifying the color.
        <pressed>: if True, the line looks pressed.
        """
        line = Line(size, type_, color, pressed, finish=False)
        line.finish()
        return line

    def __init__(self, size, type_, color=None, pressed=True, finish=True):
        """Vertical or horizontal graphical separation Line.
        <size>: the size in pixel (single int value).
        <type>: either 'horizontal', 'h' or 'vertical', 'v'.
        <color>: a 3 or 4-tuple specifying the color.
        <pressed>: if True, the line looks pressed.
        """
        Element.__init__(self, finish=False)
        self.size = size
        self.type = type_
        if type_ == "horizontal" or type_ == "h":
            size = (size, 2)
        elif type_ == "vertical" or type_ == "v":
            size = (2, size)
        painter = ClassicFrame(size, color, pressed)
        self.set_painter(painter)
        if finish:
            self.finish()

    def copy(self):
        return Line(self.size, self.type)
from thorpy.elements.element import Element
from thorpy.miscgui.storage import Storer, store
from thorpy.miscgui import functions, style, painterstyle


class Box(Element):
    """Box containing other elements."""

    @staticmethod
    def make(elements, size=None):
        box = Box(elements=elements, size=size, finish=False)
        box.finish()
        return box

    def __init__(self, elements=None, normal_params=None,
                 storer_params=None, size=None, put_lift=True, finish=True):
        """Box containing other elements.
        <bartext>: the text of the box bar. If no text, no bar is added.
        <size>: if not None, force the size of the box. Else the box
            automatically fit children."""
        Element.__init__(self, "", elements, normal_params, finish=False)
        self.storer_params = storer_params
        if self.storer_params is None:
            self.storer_params = dict()
        self._size = size
        self._has_lift = False
        self._put_lift = put_lift
        painter = functions.obtain_valid_painter(painterstyle.BOX_PAINTER,
                                                 pressed=True,
                                                 size=size,
                                                 radius_ext=style.BOX_RADIUS)
        self.set_painter(painter)
        if finish:
            self.finish()

    def add_lift(self, axis="vertical", type_="normal"):
        Element.add_lift(self, axis, type_)
        self._has_lift = True

    def store(self, size=None):
        """
        size:
            'auto' or None : autoset_framesize
            elif size : set_size and center.
        """
        size = self._size if not size else size
        storer = Storer(self, **self.storer_params)
        if size and not size == "auto":
            self.set_size(size)
            storer.center()
        elif size == "auto" or size is None:
            storer.autoset_framesize()
        (x, y) = self.is_family_bigger()
        if y and not self._put_lift:
            self.add_lift("vertical")
##            self._lift.active_wheel = True
            self._lift.active_wheel = False
        self.set_prison()

    def set_size(self, size, state=None, center_title=True, adapt_text=True,
                 cut=None, margins=None, refresh_title=False):
        if margins is None: margins=style.MARGINS
        Element.set_size(self, size, state, center_title, adapt_text, cut, margins,
                         refresh_title)
        if self._lift:
            self.remove_elements([self._lift])
            self.refresh_lift()

    def finish(self):
        Element.finish(self)
        self.store()



class BarBox(Element):

    def __init__(self, elements=None, normal_params=None, height=None):
        Element.__init__(self, "", elements, normal_params)
        h = max([e.get_storer_rect().height for e in self.get_elements()]) + 2
        store(self, mode="h", x=1, y=h/2, align="center")
        if self.father:
            w = self.father.get_storer_rect().width
        else:
            w = functions.get_screen_size()[0]
        size = (w, h)
        painter = functions.obtain_valid_painter(painterstyle.BOX_PAINTER,
                                                 pressed=True,
                                                 size=size,
                                                 radius=style.BOX_RADIUS)
        self.set_painter(painter)

    def set_standard_style(self):
        from thorpy.painting.fusionner import _Fusionner
        for e in self.get_elements():
            painter = functions.obtain_valid_painter(painterstyle.BASIC_PAINTER,
                                    size=e.get_fus_rect().size)
            fusionner = _Fusionner(painter, e.get_title())
            e.set_image(fusionner.img)
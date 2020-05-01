"""Provide functions and a class to store and order elements"""
from pygame import Rect

from thorpy.miscgui import style
from thorpy.miscgui.functions import get_screen

def _set_topleft(el, pos):
    """Set element <el>'s topleft using its storer_rect as reference."""
    left, top = pos
    x_shift = 0
    y_shift = 0
    if left is not None:
        x_shift = left - el.get_storer_rect().left
    if top is not None:
        y_shift = top - el.get_storer_rect().top
    el.move((x_shift, y_shift))

def _set_center(el, pos):
    """Set element <el>'s center using its storer_rect as reference."""
    center_x, center_y = pos
    x_shift = 0
    y_shift = 0
    if center_x is not None:
        x_shift = center_x - el.get_storer_rect().centerx
    if center_y is not None:
        y_shift = center_y - el.get_storer_rect().centery
    el.move((x_shift, y_shift))

def v_store(rect, children, xcoord=None, ystart="auto", margin=None,
             gap=None, align="center"):
    children = [c for c in children]
    children = sorted(children, key=lambda x: x.rank)
    if not children:
        return rect
    margin = style.MARGINS[1] if margin is None else margin
    gap = style.GAPS[1] if gap is None else gap
    (xc, yc) = rect.center
    (x0, y0) = rect.topleft
    xc = xc if xcoord is None else xcoord
    if ystart is None or ystart == "auto":
        y = y0 + margin - gap
    else:
        y = ystart
    previous_size = 0
    for e in children:
##        print(" el", e.id, e.get_storer_rect())
        y += previous_size + gap
        if align == "left":
            _set_topleft(e, (xc,y))
        elif align == "center":
            _set_center(e, (xc, None))  # only move x
            _set_topleft(e, (None, y))  # only move y
        elif align == "right":
            _set_topleft(e, (xc - e.get_storer_rect().width, y))
        elif align is None:
            _set_topleft(e, (None, y))  # only move y
        else:
            raise Exception("Align mode unknown.")
        previous_size = e.get_storer_rect().height
    bottom = children[-1].get_storer_rect().bottom + margin
    top = children[0].get_storer_rect().top - margin
    height = bottom - top
    if ystart == "auto":
        fr = rect
        cr = children[0].get_storer_rect()
        yshift = fr.top - cr.top + (fr.height - height)//2
        for e in children:
            e.move((0, yshift))
    return height

def h_store(rect, children, ycoord=None, xstart="auto", margin=None, gap=None,
             align="center"):
    children = [c for c in children]
    children = sorted(children, key=lambda x: x.rank)
    if not children:
        return rect
    margin = style.MARGINS[0] if margin is None else margin
    gap = style.GAPS[0] if gap is None else gap
    (xc, yc) = rect.center
    (x0, y0) = rect.topleft
    yc = yc if ycoord is None else ycoord
    if xstart is None or xstart == "auto":
        x = x0 + margin - gap
    else:
        x = xstart
    previous_size = 0
    for e in children:
        x += previous_size + gap
        if align == "top":
            _set_topleft(e, (x,yc))
        elif align == "center":
            _set_center(e, (None, yc))  # only move x
            _set_topleft(e, (x, None))  # only move y
        elif align == "bottom":
            _set_topleft(e, (x, yc - e.get_storer_rect().height))
        elif align is None:
            _set_topleft(e, (None, yc))  # only move y
        else:
            raise Exception("Align mode unknown.")
        previous_size = e.get_storer_rect().width
    left = children[0].get_storer_rect().left - margin
    right = children[-1].get_storer_rect().right + margin
    width = right - left
    if xstart == "auto":
        fr = rect
        cr = children[0].get_storer_rect()
        xshift = fr.left - cr.left + (fr.width - width)//2
        for e in children:
            e.move((xshift, 0))
    return width

def store(frame, elements=None, mode="v", x="auto", y="auto", margin=None,
            gap=None, align="center"):
    """
    <frame> can be either an element, a pygame.Rect or "screen"
    <elements>=None, None (default) will store the children of <frame>
    <mode>="v", can be either "v" ("vertical") or "h" ("horizontal")
    <x>="auto", x coordinate begin
    <y>="auto", y coordinate begin
    <margin>=None, the margin to be used (this is a single value)
    <gap>=None, the gap to be used (this is a single value)
    <align>="center", "top" or "bottom"
    """
    #frame argument handling
    if frame == "screen":
        frame = get_screen().get_rect()
    if isinstance(frame, Rect):
        rect = frame
        if elements is None:
            elements = []
##    elif frame.__class__.__name__ == "Box":
##        raise Exception("You cannot call store on a Box instance."+\
##                            "The Box element has its own store method.")
    else:
        if elements is None:
            elements = frame.get_elements()
        rect = frame.get_storer_rect()
    #end frame arg handling
    if mode == "v" or mode == "vertical":
        x = None if x == "auto" else x
        size = v_store(rect, elements, x, y, margin, gap, align)
    elif mode == "h" or mode == "horizontal":
        y = None if y == "auto" else y
        size = h_store(rect, elements, y, x, margin, gap, align)
    else:
        raise Exception("Store mode unknown.")
    return size

class Storer:
    """Store and order elements of an element"""

    def __init__(self, element, children=None, mode=None, margins=None,
                  gaps=None, align=None):
        if children is None:
            children = element.get_elements()
            children = [c for c in children]
        margins = style.MARGINS if margins is None else margins
        gaps = style.GAPS if gaps is None else gaps
        mode = style.STORE_MODE if mode is None else mode
        align = style.STORE_ALIGN if align is None else align
        self._element = element
        self._mode = mode
        self._margins = margins
        self._gaps = gaps
        self._elements = children
        self._align = align

    def get_max_element_size(self):
        """Return max height and max width in all self._elements"""
        sizes_x = list()
        sizes_y = list()
        for e in self._elements:
            size = e.get_storer_size()
            sizes_x.append(size[0])
            sizes_y.append(size[1])
        return (max(sizes_x), max(sizes_y))

    def get_elements_size(self):
        """Get size taken by elements only"""
        h = 0
        w = 0
        for e in self._elements:
##            size = e.get_storer_size()
            size = e.get_storer_rect().size
            w += size[0]
            h += size[1]
        return (w, h)

    def get_size(self, axis):
        """Get whole size needed along axis (0 or 1)"""
        n = len(self._elements)
        elts = self.get_elements_size()[axis]
        margins = 2 * self._margins[axis]
        gaps = (n - 1) * self._gaps[axis]
        return elts + margins + gaps

    def get_content_size(self):
        """Get whole size needed"""
        (wmax, hmax) = self.get_max_element_size()
        if self._mode == "vertical":
            w = wmax
            h = self.get_size(1)
        elif self._mode == "horizontal":
            w = self.get_size(0)
            h = hmax
        return (w, h)

    def get_axis(self):  # could be done simply with a dict
        if self._mode == "vertical":
            return 1
        elif self._mode == "horizontal":
            return 0

    def autoset_framesize(self, state=None):
        """Adapt the size to the elements and store them.
        Use this if the father needs to be resized, while the elements are
        not stored so you cannot use fit_children.
        """
        n = len(self._elements)
        # **** axis size ****
        axis = self.get_axis()
        margins_size = 2 * self._margins[axis] #total margin size
        gaps_size = (n - 1) * self._gaps[axis] #total gaps size
        elements_size = self.get_elements_size()[axis] #total content size
        size_axis = margins_size + gaps_size + elements_size
        # **** antiaxis size ****
        aaxis = int(not axis) #anti-axis
        m_aa = 2 * self._margins[aaxis] #total antiaxis margins size
##        g_aa = (n - 1) * self._gaps[aaxis] #total antiaxis gaps size
        g_aa = 0
        e_aa = self.get_max_element_size()[aaxis] #max antiaxis size
        size_aaxis = e_aa + m_aa + g_aa
        # **** set size ****
        if self._mode == "vertical":
            size = (size_aaxis, size_axis)
        elif self._mode == "horizontal":
            size = (size_axis, size_aaxis)
        self._element.set_size(size, state)
        self.center()  # sort elements

    def center(self):
        """Center the elements (align), either vertically or horizontally"""
        if self._mode == "vertical":
            margin = self._margins[0]
            gap = self._gaps[0]
            y = None
            if self._align == "center":
                x="auto"
            elif self._align == "left":
                x=self._element.get_storer_rect().left + self._margins[0]
            elif self._align == "right":
                x=self._element.get_storer_rect().right - self._margins[0]
        elif self._mode == "horizontal":
            margin = self._margins[1]
            gap = self._gaps[1]
            x = None
            if self._align == "center":
                y="auto"
            elif self._align == "top":
                y=self._element.get_storer_rect().top + self._margins[0]
            elif self._align == "bottom":
                y=self._element.get_storer_rect().bottom - self._margins[0]
        size=store(frame=self._element,
                      elements=self._elements,
                      mode=self._mode,
                      x=x,
                      y=y,
                      margin=margin,
                      gap=gap,
                      align=self._align)

    def _debug_control_collisions(self):
        d = {tuple(e.get_storer_rect()):e for e in self._elements}
        for e in self._elements:
            dn = d.copy()
            dn.pop(tuple(e.get_storer_rect()))
        self._element.blit()
        self._element._recurs_blit_debug(ghost=True, stor=False, fus=False, exception=1)
        self._element._path_element._blit_debug()
        from thorpy.miscgui import functions
        functions.get_current_application().save_screenshot()

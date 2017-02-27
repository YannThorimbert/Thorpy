"""Handle a Title to use with an Element."""
from pygame.rect import Rect

from thorpy._utils.strhandler import get_between_keys
from thorpy.miscgui.constants import SYNTAX_BEG, SYNTAX_END, SYNTAX_FIRST, SYNTAX_LAST
from thorpy.miscgui import style, painterstyle


class Title(object):
    """A Title is a set of str and position in order to produce a surface, using
    line spacing, align mode and cut word string as parameters."""

    def __init__(self, text, writer=None, pos=None, space=None, align=None,
                 cut_word=None):
        """
        <text> is the text to be produced. Markers can be used (see
            constants.SYNTAX_*)
        <writer> is the writer used to produce the text.
        <pos> is the relative position to painter.img.
        <space> is the interline spacing.
        <align> can be 'left', 'right' or 'center'.
        <cut_word> is the terminating string used if the text is too long to fit
        the dimensions.
        """
        pos=style.TITLE_POS if pos is None else pos
        space=style.TITLE_SPACE if space is None else space
        align=style.TITLE_ALIGN if align is None else align
        cut_word=style.CUT_WORD if cut_word is None else cut_word
        t = get_between_keys(
            text,
            SYNTAX_BEG,
            SYNTAX_END,
            SYNTAX_FIRST,
            SYNTAX_LAST)
        if t:
            self._text = t
        else:
            self._text = text
        if writer is None:
            self._writer = painterstyle.WRITER()
        else:
            self._writer = writer
        self._pos = pos
        self._space = space
        if not self._space:
            self._space = self._writer.font.get_linesize()
        self._align = align
        self._cut_word = cut_word
        self._lines = None
        self._imgs = None
        self.refresh_imgs()

    def get_height(self, n):
        h = self._writer.get_height()
        return n * h + (n - 1) * self._space

    def get_rect(self, real=False):
        """self.imgs might not include all the text if the text is too large,
        real=True means that the size limit is not taken into account.

        Set real to True if you want the rect that WOULD have the title if there
        were not size limits.
        """
        if real:
            self.set_text(self._text, size=None)
        rects = [i.get_rect() for i in self._imgs]
        widths = [r.width for r in rects]
        heigths = [r.height for r in rects]
        w = max(widths)
        h = sum(heigths) + (len(heigths) - 1) * self._space
        return Rect(self._pos, (w, h))

    def _suppress_lines(self, lines, size):
        (w, h) = size
        lines = self._writer.get_lines(lines, w)
        while self.get_height(len(lines)) > h:
            if not lines:
                return [""]
            else:
                lines.pop()
        if not lines:
            lines = [""]
        return lines

    def set_text(self, new_txt, size=None, cut=False):
        """Set the text and refresh the image"""
        self._text = new_txt
        lines = new_txt.split("\n")
        if size:
            l1 = len(lines)
            if not cut or cut == -1:
                lines = self._suppress_lines(lines, size)
            cutted = (len(lines) != l1)
            (self._imgs,
             self._lines) = self._writer.get_imgs_sized(lines,
                                                      size[0],
                                                      self._cut_word,
                                                      cutted)
        else:
            self._imgs = self._writer.get_imgs(lines)
            self._lines = lines
        if len(self._imgs) != len(self._lines):
            raise Exception("problem with title")

    def blit_on(self, surface):
        (x, y) = self._pos
        r = self.get_rect()
        if len(self._lines) != len(self._imgs):
            raise
        for i in self._imgs:
            if self._align is "left":
                x = self._pos[0]
            elif self._align is "center":
                x = (r.width - i.get_width()) / 2
            elif self._align is "right":
                x = r.width - i.get_width()
##            print(self._align, x)
            surface.blit(i, (x, y))
            y += self._space + i.get_height()

    def center_on(self, rect):
        """Set the pos in order to centralize the text onto rect"""
        r = self.get_rect()
        if isinstance(rect, tuple):
            rect = Rect((0, 0), rect)
        x_shift = rect.w - r.width
        y_shift = rect.h - r.height
        self._pos = (x_shift / 2, y_shift / 2)

    def set_pos_from_element(self, element, x_shift, y_shift):
        """Set the pos with x and y the relative coord. to element's rect"""
        self._pos = (element.rect.x + x_shift, element.rect.y + y_shift)

    def move(self, shift):
        """Shifts the position"""
        self._pos = (self._pos[0] + shift[0], self._pos[1] + shift[1])

    def get_imgs_and_lines(self, size=None):
        if not size:
            return (self._writer.get_imgs(self._text), self._lines)
        else:
            return self._writer.get_imgs_sized(self._text, size, self._cut_word)

    def get_imgs(self, size=None):
        if not size:
            return self._writer.get_imgs(self._text)
        else:
            return self._writer.get_imgs_sized(self._text, size, self._cut_word)[0]

    def set_params(self, dic,  refresh=True, size=None, cut=False):
        """Example : title.set_params({'align' : 'right', 'space' : 10})."""
        for key in dic:
            if not key.startswith("_"):
                real_key = "_" + key
            else:
                real_key = key
            setattr(self, real_key, dic[key])
        if refresh:
            self.refresh_imgs(size, cut)

    def set_writer(self, writer, refresh=True, size=None, cut=False):
        self._writer = writer
        if refresh:
            self.refresh_imgs(size, cut)

    def refresh_imgs(self, size=None, cut=False):
        """Reproduce an image using the writer"""
        self.set_text(self._text, size, cut)

    def get_text(self, get_lines=True):
        if get_lines:
            return self._lines
        else:
            return self._text

##from thorpy import Writer, Title


##class RichText(object):
##    """Handles font color, font size and indentation."""
##    def __init__(self, default_font_size=thorpy.style.FONT_SIZE,
##                        default_font_color=thorpy.style.FONT_COLOR,
##                        indent="    ",
##                        meta="*/",
##                        font_name=None):
##        self.fs = default_font_size
##        self.fc = default_font_color
##        self.default_fs = default_font_size
##        self.default_fc = default_font_color
##        self.indent = indent
##        self.paragraphs = [""]
##        self.colors = {"r":(255,0,0),"g":(0,255,0),"b":(0,0,255),"k":(0,0,0),
##                        "w":(255,255,255)}
##        self.writer = Writer(font_name,self.fc,self.fs)
##
##    def paragraph(self,*text):
##        """Add a new paragraph"""
##        content = self.indent
##        for t in text:
##            content += t
##        self.paragraphs.append(content)
##
##    def more(self, *text):
##        """Append to the current paragraph"""
##        for t in text:
##            self.paragraphs[-1] += t
##
##    #**<color>: r, g, b, k, y, w or any (r,g,b) tuple
##    #**s<n> : e.g **s12
##    #**d : all default
##
##    def apply_effect(self, command):
##        if command == "d":
##            self.fc = self.default_fc
##            self.fs = self.default_fs
##        elif command[0] == "(" and command[-1] == ")":
##            rgb = command[1:len(command)-1]
##            rgb = tuple([int(val) for val in rgb.split(",")])
##            self.fc = rgb
##        elif command in self.colors:
##            self.fc = self.colors[command]
##        elif command[0] == "s":
##            size = int(command[1:])
##            self.fs = size
##        self.refresh
##
##    def get_title(self,text): #add bold and font name
##        self.writer.set_color(self.fc)
##        self.writer.set_size(self.fs)
##        return Title(text, self.writer)
##
##    def render_text(self, text):
##        fs = self.fs #we start with default size and color
##        fc = self.fc
##        i = 0
##        imgs = []
##        current_text = ""
##        while True:
##            c = text[i]
##            current_text += c
##            if c == "*":
##                try:
##                    is_command = c[i+1] == "*"
##                except:
##                    is_command = False
##                if is_command:
##                    title = self.get_title(current_text)
##                    imgs
##                    space = text[i+2,::].find(" ")
##                    command = text[i+2:space]
##                    self.apply_effect(command)
##                    i += len(command)
##                    continue
##            img = self.writer.get_imgs(c)
##            imgs.append()
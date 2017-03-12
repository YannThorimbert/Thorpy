"""Can transform string to image, using defined font and style"""
import pygame.font

from thorpy.miscgui import constants, style


def get_font_heigth(font_name="Century", size=12):
    return pygame.font.SysFont(font_name, size).get_height()

def get_font_name(font_name, proposed_fonts=None):
    if proposed_fonts is None: proposed_fonts=style.FONTS
    if isinstance(font_name, list):
        proposed_fonts = list(font_name)
        font_name = proposed_fonts[0]
    if not font_name:
        font_name = proposed_fonts[0]
    if font_name in constants.AVAILABLE_FONTS:
        return font_name
    else:
        try:
            ok = True
            pygame.font.SysFont(font_name, 12)
        except:
            ok = False
        if ok:
            return font_name
        else:
            for font in style.FONTS:
                if font in constants.AVAILABLE_FONTS:
                    return font
    return pygame.font.get_default_font()


class BasicWriter(object):
    """Can transform string to image, using defined font and style"""

    def __init__(self,
                 font_name=None,
                 color=None,
                 size=None,
                 italic=None,
                 bold=None,
                 underline=None,
                 aa=None,
                 bckgr_color=None):
        if color is None:
            color = style.FONT_COLOR
        if size is None:
            size = style.FONT_SIZE
        if italic is None:
            italic = style.ITALIC
        if bold is None:
            bold = style.BOLD
        if underline is None:
            underline = style.UNDERLINE
        if aa is None:
            aa = style.FONT_AA
        if bckgr_color is None:
            bckgr_color = style.FONT_BCKGR
        self.font_name = get_font_name(font_name)
        self.color = color
        self.size = size
        self.italic = italic
        self.bold = bold
        self.underline = underline
        self.aa = aa
##        self.font = pygame.font.Font(self.font_name, self.size)
        self.font = pygame.font.SysFont(self.font_name, self.size, self.bold,
                                        self.italic)
        self.bckgr_color = bckgr_color

    def set_font(self, new_font):
        """set color"""
        self.font_name = get_font_name(new_font)
        self.refresh_font()

    def set_color(self, new_color):
        """set color"""
        self.color = new_color
        self.refresh_font()

    def set_size(self, new_size):
        """set size"""
        self.size = new_size
        self.refresh_font()

    def set_effects(self, bold=False, italic=False, underline=False):
        """Doesn't work with all fonts"""
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.refresh_effects()

    def get_imgs(self, text):
        """Returns a surface image of the txt"""
        if self.bckgr_color:
            return self.font.render(text, self.aa, self.color, self.bckgr_color)
        else:
            return self.font.render(text, self.aa, self.color)

# def get_img_sized(self, text, size, end=".."):
##        """Cut <txt> appending <end> if it is too big for <size> [px]"""
# if self.get_width(text) > size:
##            text = text[:-1]
# while self.get_width(text + end) > size:
##                text = text[:-1]
# return self.get_img(text + end)
# else:
# return self.get_img(text)

    def get_height(self):
        """Returns the height in pixel of this writer's font"""
        return self.font.get_height()

    def get_width(self, text):
        """Returns the width in pixel of the text with this writer"""
        return self.font.size(text)[0]

    def get_size(self, text):
        """ """
        return self.font.size(text)

    def refresh_effects(self):
        """ """
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)
        self.refresh_font()

    def refresh_font(self):
        """ """
        self.font = pygame.font.SysFont(self.font_name, self.size)


class Writer(BasicWriter):

    def get_line_sized(self, text, size, cut_word=".."):
        """Cut <txt> appending <end> if it is too big for <size> [px]"""
        if self.get_width(text) > size:
            text = text[:-1]
            while self.get_width(text + cut_word) > size:
                text = text[:-1]
                if not text:
                    return ""
            return text + cut_word
        else:
            return text

    def get_lines(self, lines, width):
        """Return list of lines with no line whose width is bigger than size"""
        if not isinstance(width, int) and not isinstance(width, float):
            raise Exception("Size must be an int or a float")
        too_long = False
        while True:
            for i in range(len(lines)):
                text = lines[i]
                if self.get_width(text) >= width:
                    too_long = True
                    splitted = text.split(" ")
                    if len(splitted) > 1:
                        last_word = str(splitted[-1])
                        lines[i] = " ".join(splitted[:-1])
                        if i + 1 < len(lines):
                            lines[i + 1] = last_word + " " + lines[i + 1]
                        else:
                            lines.append(last_word)
                    else:
                        too_long = False
            if not(too_long):
                break
            else:
                too_long = False
        return lines

    def get_imgs_sized(self, lines, width, cut_word, cutted):
        text = str(lines[-1])
        lines[-1] = self.get_line_sized(text, width, cut_word)
        if lines[-1] == text and cutted:
            lines[-
                  1] = self.get_line_sized(str(lines[-
                                                     1]) +
                                           cut_word, width, cut_word)
        return (self.get_imgs(lines), lines)

    def get_imgs(self, txts):
        """Returns a surface image of the text.
        <txt> can be either a string or a list of strings.
        """
        imgs = []
        if isinstance(txts, str):
            txts = [txts]
        for t in txts:
            if self.bckgr_color:
                imgs.append(self.font.render(t, self.aa, self.color,
                                             self.bckgr_color))
            else:
                imgs.append(self.font.render(t, self.aa, self.color))
        if not imgs:
            imgs.append(self.font.render("", self.aa, self.color))
        return imgs

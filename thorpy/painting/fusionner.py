"""Used to produce a graphical Element"""
from pygame.rect import Rect

from thorpy.miscgui import style
from thorpy.miscgui.title import Title


class _Fusionner(object):
    """Put painter and title together to produce an image, using painter's
    properties.
    """

    def __init__(self, painter, title):
        self.painter = painter
        self.title = title
        self.img = self.get_fusion()
        self.rect = Rect((0, 0), self.painter.size)

    def scale_to_title(self, margins=None, center_title=True,
                       refresh_title=True):
        margins = style.MARGINS if margins is None else margins
        size_txt = self.title.get_rect(True).size
        size = (size_txt[0] + 2*margins[0] + 1,
                size_txt[1] + 2*margins[1] + 1)
        self.painter.size = size
        self.refresh(center_title, refresh_title)

    def get_fusion(self, center_title=True, title=None):
        """Fusion the painter.img and the title.img and returns this fusion."""
        if not title:
            title = self.title
        return self.painter.get_fusion(title, center_title)

    def get_hover_fusion(self, center_title=True, writer=None, color=None):
        """Returns images corresponding to self.title._lines, with <writer> as
        writer. Default arg writer=None, means that title's writer is used.
        """
        color = style.COLOR_TXT_HOVER if color is None else color
        if not writer:
            writer = self.title._writer
        #
        pos = self.title._pos
        space = self.title._space
        align = self.title._align
        cut_word = self.title._cut_word
        lines = self.title._lines
        old_col = self.title._writer.color
        #
        writer.set_color(color)
        title = Title("", writer, pos, space, align, cut_word)
        title._lines = lines
        title._imgs = title._writer.get_imgs(lines)
        title._text = self.title._text
        img = self.get_fusion(center_title, title)
        writer.set_color(old_col)
        return img

    def refresh(self, center_title=True, refresh_title=True):
        """Fusion the painter.img and the title.img into self.img"""
        if refresh_title:
            self.title.refresh_imgs()
        self.painter.refresh_clip()
        self.img = self.get_fusion(center_title)
        self.refresh_rect()

    def refresh_rect(self):
        self.rect.size = self.img.get_size()


class FusionnerText(_Fusionner):

    def __init__(self, title):
        self.title = title
        self.img = self.get_fusion()
        img_size = self.img.get_size()
        self.rect = Rect((0, 0), img_size)

    def get_hover_fusion(self, center_title=None, writer=None, color=None):
        color=style.COLOR_TXT_HOVER if color is None else color
        old_col = self.title._writer.color
        if len(self.title._lines) != len(self.title._imgs):
            raise Exception("title problem")
        self.title._writer.set_color(color)
        img = self.title.get_imgs()[0] #only simple text use it, not multisimple text
        self.title._writer.set_color(old_col)
        return img

    def get_fusion(self, center_title=None, writer=None):#writer unused for compatibilty reasons
        return self.title._imgs[0]

    def refresh(self, center_title=None, refresh_title=True):
        if refresh_title:
            self.title.refresh_imgs()
        self.img = self.get_fusion()
        self.refresh_rect()

    def scale_to_title(self, margins=None, center_title=True,
                       refresh_title=True):
        pass

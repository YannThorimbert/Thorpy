from thorpy.painting.writer import Writer
from thorpy.elements.text import OneLineText
from thorpy.miscgui import style


class _InsertWriter(OneLineText):

    def __init__(self, text="", margin=None, writer=None,finish=True):
        margin = style.INSERTWRITER_MARGIN if margin is None else margin
        OneLineText.__init__(self, text,finish=False)
        self.margin = margin
        if not writer:
            self.writer = Writer()
        else:
            self.writer = writer
        if finish:
            self.finish()

    def get_zone(self):
        return self.father.get_clip()
# return self.father.get_fus_rect()

    def _is_small_enough(self, word):
        w = self.current_state.fusionner.title._writer.get_width(word)
        if w + self.margin >= self.get_zone().width:
            return False
        return True

    def refresh_img(self):
        """Refresh self's text. Returns -1 if the text is too large."""
        text = self.father._inserted
        txt_img = self.writer.get_imgs(text)[0]
        if txt_img.get_size()[0] + self.margin >= self.get_zone().width:
            return -1
        self.set_text(text)

    def _refresh_pos(self):
        zone = self.get_zone()
        y = (zone.height - self.writer.get_height()) / 2
        self.set_topleft((zone.x + self.margin, zone.y + y))

    def _get_cursor_pos(self):
        text = self.father._inserted[0:self.father._cursor_index]
        w = self.current_state.fusionner.title._writer.get_width(text)
        zone = self.get_zone()
        curs_height = self.father.cursor.get_fus_size()[1]
        y = zone.y + (zone.h - curs_height) / 2
        return (zone.x + self.margin + w, y)

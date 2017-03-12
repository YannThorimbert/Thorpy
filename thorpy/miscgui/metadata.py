import json, pygame

import thorpy.miscgui.theme as theme


class MetaDataManager(object):

    def __init__(self, data=None):
        if data is None: data = {}
        self.data = data

    def write_data(self, fn):
        json.dump(self.data, open(fn,'w'))

    def read_data(self, fn):
        try:
            self.data = json.load(open(fn))
        except:
            return None
        return True

    def load_font_data(self, fn):
        font = self.data.get("font")
        if font:
            theme.add_font(font)
        font_size = self.data.get("font_size")
        if font_size:
            theme.set_font_sizes(font_size)

    def get_display_data(self, fn, w, h, flags):
        W,H = self.data.get("screen_w"), self.data.get("screen_h")
        fullscreen = self.data.get("fullscreen")
        flags = flags
        if fullscreen:
            flags |= pygame.FULLSCREEN
        if W is None: W = w
        if H is None: H = h
        return W,H,flags

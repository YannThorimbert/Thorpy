from thorpy.painting.writer import Writer
from thorpy._utils.images import load_image
from thorpy.miscgui import functions, style


class _DirViewer(object):

    def __init__(self,
                 files,
                 size,
                 writer=None,
                 writer_hover=None,
                 gap=None,
                 x=None,
                 folders=None,
                 fold_img=None):
        gap = style.DIRVIEWER_GAP if gap is None else gap
        x = style.DIRVIEWER_X if x is None else x
        self.files = files
        self.size = size
        if writer:
            self.writer = writer
        else:
            self.writer = Writer()
        if writer_hover:
            self.writer_hover = writer_hover
        else:
            self.writer_hover = Writer(color=(255, 0, 0))
        self.gap = gap
        self.elh = self.writer.get_height()
        self.pix_0 = 0
        self.x = x
        self._hovered = -1
        if folders:
            self.folders = folders
        else:
            self.folders = []
        self.N = len(self.files) + len(self.folders)
        if fold_img:
            self.fold_img = fold_img
        elif self.folders:
            self.fold_img = load_image(filename=style.FOLDER_IMG,
                                       colorkey=style.FOLDER_IMG_COLORKEY)
        if fold_img and (self.x is None):
            self.x = self.fold_img.get_width()
        elif self.x is None:
            self.x = 25
        self.folders_separated = True
        self.sort()


    def sort(self):
        if self.folders_separated:
            new_files = list(self.folders)
            for f in self.files:
                if not(f in self.folders):
                    new_files.append(f)
            self.files = new_files

    def control(self):
        if self.pix_0 < 0:
            raise ValueError("DirViewer's pix_0 is negative" + str(self.pix_0))
        elif self.get_n() - 1 > self.N:
            raise ValueError(
                "DirViewer's pix_0 is too large" + str(self.pix_0))

    def get_n(self):
        """Returns index of the first text to be blitted"""
        n = float(self.pix_0 - self.gap) / (self.elh + self.gap)
        n = int(n + 1.)
        return max(n - 1, 0)

    def get_y(self, n):
        """Returns y-coord of the n-th text to be blitted"""
        return n * (self.gap + self.elh) - self.pix_0

    def get_n_at_y(self, y):
        """Returns index of the element at coord y"""
        return int((y + self.pix_0) / (self.gap + self.elh))

    def get_at_pix(self, x, y):
        """Returns the index of text in position (x, y)"""
        if x < 0 or x > self.size[0]:
            return None
        elif y < 0 or y > self.size[1]:
            return None
        else:
            return self.get_n_at_y(y)

    def get_txt_at_pix(self, x, y):
        index = self.get_at_pix(x, y)
        try:
            if index is not None:
                return self.files[index]
            else:
                return None
        except IndexError:
            return None

    def blit_on(self, surface, cursor, pos):
        """Blit the files texts on self.surface, not on browser!!"""
        i = self.get_n()
        y = self.get_y(i)
        _hovered = self.get_at_pix(cursor[0], cursor[1])
        while y < self.size[1] and i < self.N:
            text = [self.files[i]]
            if i == _hovered:
                txt_img = self.writer_hover.get_imgs(text)[0]
            else:
                txt_img = self.writer.get_imgs(text)[0]
            if text in self.folders:
                surface.blit(self.fold_img, (pos[0] + 2, pos[1] + y))
            surface.blit(txt_img, (pos[0] + self.x, pos[1] + y))
            i += 1
            y += self.elh + self.gap

    def get_real_size(self):
        w = self.size[0]
        L = len(self.files)
        h = L * self.elh + (L - 1) * self.gap
        return (w, h)


class _HeavyDirViewer(_DirViewer):
    """Like _DirViewer, but pre-store img txts in memory (slower at
    initialization, faster at run).
    """

    def __init__(self, files, size,
                 writer=None,
                 writer_hover=None,
                 gap=None,
                 x=None,
                 folders=None,
                 fold_img=None):
        _DirViewer.__init__(self, files, size, writer, writer_hover, gap, x,
                           folders, fold_img)
        self.txt_imgs = self.get_txt_imgs()

    def get_txt_imgs(self):
        imgs = list()
        for f in self.files:
            txt_img = self.writer.get_img(f)
            imgs.append(txt_img)
        return imgs

    def blit_on(self, surface, cursor, pos=None):
        """Blit the files texts on self.surface, not on browser!!"""
        if pos:
            functions.debug_msg(
                "pos argument used for heavy dirviewer, but not handled.")
        i = self.get_n()
        y = self.get_y(i)
        _hovered = self.get_at_pix(cursor[0], cursor[1])
        while y < self.size[1] and i < self.N:
            text = self.files[i]
            if i == _hovered:
                txt_img = self.writer_hover.get_img(text)
            else:
                txt_img = self.txt_imgs[i]
            surface.blit(txt_img, (self.x, y))
            i += 1
            y += self.elh + self.gap

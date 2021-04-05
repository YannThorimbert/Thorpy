import os

from thorpy.elements.text import OneLineText
from thorpy.elements.clickable import Clickable
from thorpy.miscgui.storage import h_store
from thorpy.miscgui import functions, style

class PathElement(OneLineText):

    def __init__(self, father, abspath,finish=True):
        OneLineText.__init__(self)
        self.father = father
        self._path = father.path
        self.abspath = abspath
        self._n = None
        self._path_list = self._get_strs()
        self._path = "".join(self._path_list)
        if finish:
            self.finish()

    def finish(self):
        OneLineText.finish(self)

    def _get_strs(self):
        if self.abspath:
            path = os.path.abspath(self._path)
        else:
            path = str(self._path)
        path = os.path.normpath(path)
        path = path.split(os.sep)
        path = [s+"/" for s in path]
        return path

    def _reaction_path(self, n):
        if n != self._n:
            self._path_list = self._path_list[0:n+1]
            self._path = "".join(self._path_list)
            ycoord = self._elements[0].get_storer_rect().centery
            self._set_path_elements(ycoord)
            functions.refresh_current_menu()
            self.father._refresh_ddlf()
            self.father.unblit()
            self.father.blit()
            self.father.update()
            if self.father.folders:
                self.father._clicked = ""
                inserted = self._path_list[-1]
                self.father._refresh_select(inserted)


    def _set_path_elements(self, ycoord=None):
        self.remove_all_elements()
        i = 0
        for s in self._path_list:
            e = Clickable(s)
            e.set_style("text")
            e.normal_params.params["font_size"] = style.PATH_FONT_SIZE
            e.press_params.params["font_size"] = style.PATH_FONT_SIZE
            e.finish()
            e.user_func = self._reaction_path
            e.user_params = {"n" : i}
            e.set_jailed(self.father)
##            e._lock_jail = True #so that in the future jail will always stay self.father
            self.add_elements([e])
            i += 1
        father = self
        if self.father.is_finished():
            father = self.father
        fr = father.get_storer_rect()
        wtot = h_store(fr, self._elements, gap=0, xstart="auto", ycoord=ycoord)
        if wtot > fr.width:
            h_store(fr, self._elements, gap=0, ycoord=ycoord,
                        xstart=fr.right - wtot-2)
        self._n = len(self._elements)

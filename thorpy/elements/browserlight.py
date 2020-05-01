# -*- coding: utf-8 -*-

from __future__ import division

from os import listdir
from os.path import isdir

from thorpy.elements.element import Element
from thorpy.elements.inserter import Inserter
from thorpy.elements.ddlf import DropDownListFast
from thorpy.elements.text import OneLineText
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, functions, parameters, style, painterstyle

class BrowserLight(Element):
    """File and folder browser for a given directory."""

    @staticmethod
    def make(path="./", ddl_size=None, folders=True, files=True, file_types=None, text=""):
        browser = BrowserLight(path, ddl_size, folders=folders, files=files,
                            file_types=file_types, text=text, finish=False)
        browser.finish()
        return browser

    def __init__(self,
                 path="./",
                 ddl_size=None,
                 normal_params=None,
                 folders=True,
                 files=True,
                 file_types=None,
                 text="",
                 finish=True):
        """File and folder browser.
        <path>: the path of the folder in which browser browse files.
        <ddl_size>: if not None, force the size of the dropdown list of files.
        <folders>: if True, displays folders to user.
        <files>: if True, displays file to user.
        <file_types>: if not None, pass a list of files formats that you wand to
            be valid for user choice.
        <text>: title text of the browser.
        """
        ddl_size = style.BROWSERLIGHT_DDL_SIZE if ddl_size is None else ddl_size
        super(BrowserLight, self).__init__(normal_params=normal_params,finish=False)
        self.path = path
        self._ddl_size = ddl_size
        if not hasattr(file_types, "__iter__") and file_types is not None:
            raise ValueError("Files types must be a sequence.")
        self.file_types = file_types
        # DropDownListFast
        actual_folders, actual_files = self._get_folders_and_files()
        actual_files = self._filter_files(actual_files)
        if not folders:
            actual_folders = None
        if not files:
            actual_files = []
        self._ddlf = DropDownListFast(size=self._ddl_size, titles=actual_files,
                                      folders=actual_folders,finish=False)
        # selection button
        inserter_width = 3 * ddl_size[0] // 4
##        if inserter_width > style.MAX_INSERTER_WIDTH:
##            inserter_width = style.MAX_INSERTER_WIDTH
        self._selected = Inserter("Selected : ", size=(inserter_width, None))
        if isinstance(text, str):
            self.text_element = OneLineText(text)
        else:
            self.text_element = text
        self.add_elements([self.text_element, self._ddlf, self._selected])
        reac_pressed = Reaction(parameters.BUTTON_UNPRESS_EVENT,
                                self._reaction_press,
                                reac_name=constants.REAC_PRESSED)
        self._ddlf.finish()
        self.add_reaction(reac_pressed)
        self._clicked = None
        self._something_selected = False
        painter = functions.obtain_valid_painter(painterstyle.BOX_PAINTER,
                                                 pressed=True,
##                                                 color=style.DEF_COLOR2,
                                                 radius=style.BOX_RADIUS)
        self.set_painter(painter)
        self._refresh_ddlf_lift()
        if finish:
            self.finish()

    def finish(self):
        Element.finish(self)
        self.store()
        self.text_element.set_center((self.get_fus_rect().centerx, None))
        self.set_prison()

    def _refresh_ddlf_lift(self):
        if self._ddlf._lift:
            functions.remove_element(self._ddlf._lift)
        if self._ddlf.get_family_rect().height > self._ddlf.get_fus_rect().height:
            self._ddlf.add_lift()
        functions.refresh_current_menu()

    def _refresh_select(self, inserted=None):
        self._selected._value = self.path + self._clicked + "/"
        inserted = self._clicked if inserted is None else inserted
        _iwriter = self._selected._iwriter
        writer = _iwriter.current_state.fusionner.title._writer
        size = _iwriter.get_zone().width - 2*_iwriter.margin
        self._selected._inserted = writer.get_line_sized(inserted, size)
        txt_refreshed = self._selected._urbu()
        self._something_selected = True

    def _reaction_press(self, event):
        x, y = self._ddlf._get_dirviewer_coords(event.pos)
        if not self._ddlf._lift or x < self._ddlf._dv.size[0] - self._ddlf._lift.get_fus_size()[0]:
            self._clicked = self._ddlf._dv.get_txt_at_pix(x, y)
            if self._clicked:
                self._refresh_select()

    def get_value(self):
        return self._selected._value

    def _get_folders_and_files(self):
        try:
            titles = listdir(self.path)
        except:
            print("Access denied to this folder/file. Try running\
                                 the script as administrator.")
            return [], []
        folders = []
        files = []
        for title in titles:
            if isdir(self.path + title + "/"):
                folders.append(title)
            else:
                files.append(title)
        return folders, files

    def list_folder_and_files(self):
        return self._ddlf._dv.folders, self._ddlf._dv.files

    def _filter_files(self, files):
        if self.file_types is not None:
            new_files = []
            for title in files:
                if not isdir(title):
                    for extension in self.file_types:
                        if title.endswith(extension):
                            new_files.append(title)
            return new_files
        else:
            return files

    def get_help_rect(self):
        return self._selected.get_help_rect()

    def get_dirviewer(self):
        return self._ddlf
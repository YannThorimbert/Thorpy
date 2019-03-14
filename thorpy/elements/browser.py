# -*- coding: utf-8 -*-
import os

import pygame

from thorpy.elements.browserlight import BrowserLight
from thorpy.elements._explorerutils._pathelement import PathElement
from thorpy.elements.element import Element
from thorpy.elements.inserter import Inserter
from thorpy.elements.ddlf import DropDownListFast
from thorpy.elements.text import OneLineText
from thorpy.miscgui.storage import Storer
from thorpy.miscgui.reaction import Reaction
from thorpy.miscgui import constants, functions, parameters, style, painterstyle

class Browser(BrowserLight):
    """File and folder browser."""

    @staticmethod
    def make(path="./", ddl_size=None, folders=True, files=True, file_types=None, text=""):
        browser = Browser(path, ddl_size, folders=folders, files=files,
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
        """File and folder browser for a.
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
        self.path = self.set_path(path)
        self.last_done_path = str(self.path)
        self._ddl_size = ddl_size
        self.file_types = file_types
        self.folders = folders
        self.files = files
        # DropDownListFast
        actual_folders, actual_files = self._get_folders_and_files()
        actual_files = self._filter_files(actual_files)
        if not folders:
            actual_folders = None
        if not files:
            actual_files = []
        self._ddlf = DropDownListFast(size=self._ddl_size, titles=actual_files,
                                      folders=actual_folders, has_lift=True,
                                      finish=False)
##        self._ddlf.finish()
        # selection button
        inserter_width = 3*ddl_size[0]//4
##        if inserter_width > style.MAX_INSERTER_WIDTH:
##            inserter_width = style.MAX_INSERTER_WIDTH
        self._selected = Inserter("Selected : ", size=(inserter_width, None))
        if isinstance(text, str):
            self.text_element = OneLineText(text)
        else:
            self.text_element = text
        self._path_element = PathElement(father=self, abspath=True)
        self.add_elements([self.text_element, self._path_element, self._ddlf,
                           self._selected])
        reac_pressed = Reaction(parameters.BUTTON_UNPRESS_EVENT,
                                self._reaction_press,
                                {"button":1},
                                reac_name=constants.REAC_PRESSED)
##        self._ddlf._force_lift = True
        self._ddlf.finish()
        self.add_reaction(reac_pressed)
        self._clicked = None
        self._something_selected = False
        painter = functions.obtain_valid_painter(painterstyle.BOX_PAINTER,
                                                 pressed=True,
                                                 radius=style.BOX_RADIUS)
        self.set_painter(painter)
        self._last_click = -2 * parameters.DOUBLE_CLICK_DELAY
        if finish:
            self.finish()

    def finish(self):
        self._path_element._set_path_elements()
        Element.finish(self)
        self.store()
        centerx = self.get_fus_rect().centerx
        self.text_element.set_center((centerx, None))
        ycoord = self._path_element._elements[0].get_storer_rect().centery
        self._path_element._set_path_elements(ycoord)
        self.set_prison()

    def set_path(self, path):
        path = os.path.normpath(path)
        if path[-1] == os.path.sep:
            return path
        else:
            return path + os.path.sep

##    def store(self):
####        r = self.get_family_rect()
####        self.set_size((r.width, r.height))
##        storer = Storer(self, margins=style.BROWSERLIGHT_STORE_MARGINS,
##                        gaps=style.BROWSERLIGHT_STORE_GAPS)
##        storer.autoset_framesize()

##    def _refresh_ddlf_lift(self):
##        if self._ddlf._lift:
##            functions.remove_element(self._ddlf._lift)
##        if self._ddlf.get_family_rect().height > self._ddlf.get_fus_rect().height:
##            self._ddlf.add_lift()
##        functions.refresh_current_menu()

    def _refresh_ddlf(self):
        self.path = self._path_element._path
        actual_folders, actual_files = self._get_folders_and_files()
        actual_files = self._filter_files(actual_files)
        if not self.folders:
            actual_folders = None
        if not self.files:
            actual_files = []
        self._ddlf._dv = self._ddlf._get_dirviewer(titles=actual_files,
                                                   size=self._ddl_size,
                                                   folders=actual_folders)
        self._refresh_ddlf_lift()

    def _go_to_dir(self, selected):
        self._path_element._path = selected
        self._path_element._path_list = self._path_element._get_strs()
        ycoord = self._path_element._elements[0].get_storer_rect().centery
        self._path_element._set_path_elements(ycoord)
        functions.refresh_current_menu()
        self._refresh_ddlf()
        self.unblit()
        self.blit()
        self.update()

    def _reaction_press(self, event):
        hit_lift = False
        if self._ddlf._lift:
            if self._ddlf._lift.get_fus_rect().collidepoint(event.pos):
                hit_lift = True
        if not hit_lift:
            BrowserLight._reaction_press(self, event)
            selected = self.get_value()
            tick = pygame.time.get_ticks()
            if os.path.isdir(selected):
                if tick - self._last_click < parameters.DOUBLE_CLICK_DELAY:
                    self._go_to_dir(selected)
            self._last_click = tick
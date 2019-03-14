from os.path import normpath, basename

from thorpy.elements.clickable import Clickable
from thorpy.miscgui import constants, parameters, style
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.miscgui.launchers import launcher as launchmod
DONE, CANCEL, CLICK_QUIT = launchmod.DONE, launchmod.CANCEL, launchmod.CLICK_QUIT


class BrowserLauncher(Clickable):

    @staticmethod
    def make(browser, const_text="", var_text="", show_select=True,
                click_cancel=False, text_ok="Ok", text_cancel="Cancel",
                size=None):
        if size is None: size=style.MAKE_SIZE
        bl = BrowserLauncher(browser, const_text, var_text, show_select,
                                click_cancel, text_ok, text_cancel,finish=False)
        bl.finish()
        bl._make_size(size)
        return bl

    def __init__(self,
                 browser,
                 const_text="",
                 var_text="",
                 show_select=True,
                 click_cancel=False,
                 text_ok="Ok",
                 text_cancel="Cancel",
                 finish=True):
        self.recenter=True
        self.const_text = const_text
        self.var_text = var_text
        self.click_cancel = click_cancel
##        self.max_chars = float("inf")
        self.max_chars = 30
        self.cut_text = ".."
        self.show_select = show_select
        self.launcher = None
        self.unlaunch_func = None
        box = launchmod.make_ok_cancel_box([browser], text_ok, text_cancel)
        self.launched = box
        self.browser = browser
        Clickable.__init__(self, self.const_text+self.var_text,finish=False)
        if finish:
            self.finish()

    def finish(self):
        Clickable.finish(self)
        self._set_launcher()

    def _set_launcher(self):
        launcher = launchmod.Launcher(self.launched, launching=self)
        reac_enter = ConstantReaction(constants.THORPY_EVENT,
                             launcher.launch,
                             {"id": constants.EVENT_UNPRESS, "el":self})
##                             reac_name="reac_launch")
        reac_done = ConstantReaction(constants.THORPY_EVENT,
                             self.unlaunch,
                             {"id": constants.EVENT_DONE, "el":self.launched},
                             {"what": DONE})
##                             reac_name="reac_done")
        reac_cancel = ConstantReaction(constants.THORPY_EVENT,
                         self.unlaunch,
                         {"id": constants.EVENT_CANCEL, "el":self.launched},
                         {"what": CANCEL})
##                         reac_name="reac_cancel")
        if self.click_cancel:
            reac_click_cancel = Reaction(parameters.MOUSEBUTTONUP,
                                    launchmod.func_click_quit,
                                    params={"launcher":self,"what":CLICK_QUIT},
                                    reac_name="reac_click_cancel")
            self.launched.add_reaction(reac_click_cancel)
        self.add_reaction(reac_enter)
        self.launched.add_reaction(reac_done)
        self.launched.add_reaction(reac_cancel)
        self.launcher = launcher

    def unlaunch(self, what):
        if what == DONE:
            self.default_unlaunch_done()
            self.browser.last_done_path = str(self.browser.path)
        else:
            self.browser._go_to_dir(self.browser.last_done_path)
        self.launcher.unlaunch(what)


    def default_unlaunch_done(self):
        if self.browser._something_selected and self.show_select:
            text = normpath(self.browser._selected._inserted)
            self.var_text = basename(text)
            text = self.const_text+self.var_text
            if len(text) > self.max_chars:
                text = text[:self.max_chars-len(self.cut_text)] + self.cut_text
            self.set_text(text)
            self.scale_to_title()
            if self.recenter:
                self.center(element=self.father, axis=(True,False))

##        if self.browser._something_selected and self.show_select:
##            text = normpath(self.browser._selected._inserted)
##            text = basename(text)
##            self._file_element.set_text(text,
##                          size=(self.file_width, self.get_fus_rect().h),
##                          cut=True)

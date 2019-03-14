import pygame
from thorpy.elements.clickable import Clickable
from thorpy.elements.ddlf import DropDownListFast
from thorpy.miscgui import constants, parameters, style
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.miscgui.launchers import launcher as launchmod

DONE, CANCEL, CLICK_QUIT = launchmod.DONE, launchmod.CANCEL, launchmod.CLICK_QUIT


class DropDownListLauncher(Clickable):

    @staticmethod
    def make(const_text="",
             var_text="",
             titles=None,
             ddlf_size="auto",
             show_select=True,
             click_cancel=True,
             size=None):
        if size is None: size=style.MAKE_SIZE
        ddll = DropDownListLauncher(const_text, var_text, titles, ddlf_size,
                                    show_select, click_cancel,finish=False)
        ddll.finish()
        ddll._make_size(size)
        return ddll

    def __init__(self,
                 const_text="",
                 var_text="",
                 titles=None,
                 ddlf_size="auto",
                 show_select=True,
                 click_cancel=True,
                 finish=True):
        self.recenter = True
        self.const_text = const_text
        self.var_text = var_text
        self.click_cancel = click_cancel
##        self.max_chars = float("inf")
        self.max_chars = 30
        self.cut_text = ".."
        self.unlaunch_func = None
        ddlf_size = style.DDL_SIZE if ddlf_size is None else ddlf_size
        if not isinstance(titles, DropDownListFast):
            titles = [] if titles is None else titles
            self.launched = DropDownListFast(size=ddlf_size, titles=titles, x=2)
        else:
            self.launched = titles
        self.show_select = show_select
        self.launcher = None
        Clickable.__init__(self, self.const_text+self.var_text,finish=False)
        if finish:
            self.finish()

    def finish(self):
        Clickable.finish(self)
        self._set_launcher()

    def get_value(self):
        return self.var_text

    def set_value(self, text):
        old = self.var_text
        if isinstance(text, list):
            self.var_text = text[0]
        else:
            self.var_text = text
        if old != self.var_text:
            self.refresh()

    def _set_launcher(self):
        launcher = launchmod.Launcher(self.launched, launching=self)
        reac_enter = ConstantReaction(constants.THORPY_EVENT,
                             launcher.launch,
                             {"id": constants.EVENT_UNPRESS, "el":self})
##                             reac_name="reac_launch")
        reac_done = ConstantReaction(constants.THORPY_EVENT,
                             self.unlaunch,
                             {"id": constants.EVENT_DDL, "el":self.launched})
##                             reac_name="reac_done")
        if self.click_cancel:
            reac_cancel = Reaction(parameters.MOUSEBUTTONUP,
                                    launchmod.func_click_quit,
                                    params={"launcher":launcher, "what":CLICK_QUIT})
##                                    reac_name="reac_cancel")
            self.launched.add_reaction(reac_cancel)
        self.add_reaction(reac_enter)
        self.launched.add_reaction(reac_done)
        def func_before():
            self.launched.stick_to(self, "bottom", "top")
            self.launched.blit()
            self.launched.update()
        launcher.func_before = func_before
        self.launcher = launcher

    def refresh(self):
        text = self.const_text+self.var_text
        if len(text) > self.max_chars:
            text = text[:self.max_chars-len(self.cut_text)] + self.cut_text
        self.set_text(text)
        self.scale_to_title()
        if self.recenter:
            self.center(element=self.father, axis=(True,False))


    def default_unlaunch(self):
        if self.show_select and self.launched._clicked:
            self.var_text = self.launched._clicked
            self.refresh()
        self.launcher.unlaunch(CANCEL)
        ##            self._file_element.set_text(text,
##                          size=(self.file_width, self.get_fus_rect().h),
##                          cut=True)

    def unlaunch(self):
        ev = pygame.event.Event(constants.THORPY_EVENT, id=constants.EVENT_DDL,
                                el=self, value=self.launched._clicked)
        pygame.event.post(ev)
        if not self.unlaunch_func:
            self.default_unlaunch()
        else:
            self.unlaunch_func()

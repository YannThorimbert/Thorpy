from os.path import normpath, basename

from thorpy.elements.clickable import Clickable
from thorpy.miscgui import constants, parameters, style
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.miscgui.launchers import launcher as launchmod
from thorpy.elements.paramsetter import ParamSetter
from thorpy.elements._wrappers import make_text

DONE, CANCEL, CLICK_QUIT = launchmod.DONE, launchmod.CANCEL, launchmod.CLICK_QUIT

def _get_title(title):
    if not title:
        return None
    if isinstance(title, str):
        return make_text(title, style.TITLE_FONT_SIZE, style.TITLE_FONT_COLOR)
    else:
        return title

class ParamSetterLauncher(Clickable):

    @staticmethod
    def make(params, text="", title=None, click_cancel=False, text_ok="Ok",
                text_cancel="Cancel", paramsetter_elements=None,
                size=None):
        if size is None: size=style.MAKE_SIZE
        psl = ParamSetterLauncher(params, text, title, click_cancel, text_ok,
                                    text_cancel, paramsetter_elements, finish=False)
        psl.finish()
        psl._make_size(size)
        return psl

    def __init__(self,
                 params,
                 text="",
                 title=None,
                 click_cancel=False,
                 text_ok="Ok",
                 text_cancel="Cancel",
                 paramsetter_elements=None,
                 finish=True):
        """params can either be a varset or a paramsetter.
        title can either be a string or an element."""
        if isinstance(params, ParamSetter):
            self.paramsetter = params
        else:
            self.paramsetter = ParamSetter(params, elements=paramsetter_elements)
        self.click_cancel = click_cancel
        self.max_chars = float("inf")
        self.cut_text = ".."
        self.launcher = None
        e_title = _get_title(title)
        if e_title:
            elements = [e_title, self.paramsetter]
        else:
            elements = [self.paramsetter]
        box = launchmod.make_ok_cancel_box(elements, text_ok, text_cancel)
        self.launched = box
        Clickable.__init__(self, text, finish=False)
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
                             self._unlaunch_done,
                             {"id": constants.EVENT_DONE, "el":self.launched})
##                             reac_name="reac_done")
        reac_cancel = ConstantReaction(constants.THORPY_EVENT,
                         self._unlaunch_cancel,
                         {"id": constants.EVENT_CANCEL, "el":self.launched})
##                         reac_name="reac_cancel")
        if self.click_cancel:
            reac_click_cancel = Reaction(parameters.MOUSEBUTTONUP,
                                    self._unlaunch_click_cancel,
                                    params={"launcher":launcher})
##                                    reac_name="reac_click_cancel")
            self.launched.add_reaction(reac_click_cancel)
        self.add_reaction(reac_enter)
        self.launched.add_reaction(reac_done)
        self.launched.add_reaction(reac_cancel)
        self.launcher = launcher

    def _unlaunch_cancel(self, what=CANCEL):
        self.paramsetter.reinit_handlers()
        self.launcher.unlaunch(what)

    def _unlaunch_click_cancel(event, launcher):
        if not launcher.launched.collide(event.pos):
            self._unlaunch_cancel(CLICK_QUIT)

    def _unlaunch_done(self):
        self.paramsetter.save()
        self.launcher.unlaunch(DONE)

##        if self.browser._something_selected and self.show_select:
##            text = normpath(self.browser._selected._inserted)
##            text = basename(text)
##            self._file_element.set_text(text,
##                          size=(self.file_width, self.get_fus_rect().h),
##                          cut=True)

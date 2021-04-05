from thorpy.elements.clickable import Clickable
from thorpy.elements.colorsetter import ColorSetter, get_example_element
from thorpy.miscgui import constants, parameters, style
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.miscgui.launchers import launcher as launchmod
from thorpy.miscgui.storage import store
from thorpy.elements.element import Element

DONE, CANCEL, CLICK_QUIT = launchmod.DONE, launchmod.CANCEL, launchmod.CLICK_QUIT


class ColorSetterLauncher(Clickable):

    @staticmethod
    def make(colorsetter,
             text="",
             show_select=True,
             click_cancel=False):
        cs = ColorSetterLauncher(colorsetter, text, show_select, click_cancel,
                                    finish=False)
        cs.finish()
        return cs

    def __init__(self,
                 colorsetter,
                 text="",
                 show_select=True,
                 click_cancel=False,
                 finish=True):
        self.text = text
        self.show_select = show_select
        self.click_cancel = click_cancel
        if not isinstance(colorsetter, ColorSetter):
            self.colorsetter = ColorSetter.make(self.text, value=colorsetter)
        else:
            self.colorsetter = colorsetter
        self.old_color = self.colorsetter.get_value()
        self.launched = launchmod.make_ok_cancel_box([self.colorsetter], "Ok", "Cancel") #!!! text
        self.launcher = None
        self.e_color = get_example_element(self.colorsetter.get_color(), (20,20))
        self.e_text = Element(self.text,finish=False)
        self.e_text.set_style("text")
        self.e_text.finish()
        self.unlaunch_func = None
        Clickable.__init__(self, elements=[self.e_text, self.e_color],finish=False)
        if finish:
            self.finish()

    def finish(self):
        Clickable.finish(self)
##        self.e_color.stick_to(self, "right", "right")
##        self.e_color.move((-2,0))
        store(self, mode="h")
        self.fit_children()
        self._set_launcher()


    def get_value(self):
        return self.colorsetter.get_value()

    def set_value(self, value):
        self.colorsetter.set_value(value)
        self.refresh()

    def refresh(self):
        color = self.colorsetter.get_value()
        self.e_color.get_elements()[0].set_main_color(color)
        self.old_color = color

    def _set_launcher(self):
        launcher = launchmod.Launcher(self.launched, launching=self)
        reac_enter = ConstantReaction(constants.THORPY_EVENT,
                             launcher.launch,
                             {"id": constants.EVENT_UNPRESS, "el":self})
##                             reac_name="reac_launch")
        reac_done = ConstantReaction(constants.THORPY_EVENT,
                             self.unlaunch,
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
##                                    reac_name="reac_cancel")
            self.launched.add_reaction(reac_click_cancel)
        self.launched.add_reaction(reac_cancel)
        self.add_reaction(reac_enter)
        self.launched.add_reaction(reac_done)
        self.launcher = launcher

    def _unlaunch_cancel(self, what=CANCEL):
        self.colorsetter.set_value(self.old_color)
        self.launcher.unlaunch(what)

    def _unlaunch_click_cancel(event, launcher):
        if not launcher.launched.collide(event.pos):
            self._unlaunch_cancel(CLICK_QUIT)

    def default_unlaunch(self):
        self.refresh()
        self.launcher.unlaunch(DONE)
        ##            self._file_element.set_text(text,
##                          size=(self.file_width, self.get_fus_rect().h),
##                          cut=True)

    def unlaunch(self):
        if not self.unlaunch_func:
            self.default_unlaunch()
        else:
            self.unlaunch_func()

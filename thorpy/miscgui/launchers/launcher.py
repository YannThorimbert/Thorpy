"""It is elements' responsibilities to handle event in order to call launch
and unlaunch. However a default behaviour can be set using launch()."""
import pygame
from pygame import event

from thorpy.miscgui import constants, functions, parameters
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.elements.box import Box
from thorpy.elements._wrappers import make_button
from thorpy.elements.ghost import Ghost
from thorpy.elements.line import Line
from thorpy.elements._wrappers import make_stored_ghost
from thorpy.menus.tickedmenu import TickedMenu

DONE, CANCEL, CLICK_QUIT = constants.LAUNCH_DONE, constants.LAUNCH_CANCEL, constants.LAUNCH_CLICK_QUIT

def func_click_quit(event, launcher, what):
    if not launcher.launched.collide(event.pos):
        launcher.unlaunch_cancel(what)

def get_launcher(launched, click_quit=False, launching=None, autocenter=True):
    """Prepare and return a launcher object for launching <launched>."""
    launcher = Launcher(launched, launching=launching)
    launcher.autocenter = autocenter
    reac_done = ConstantReaction(constants.THORPY_EVENT,
                         launcher.unlaunch_done,
                         {"id": constants.EVENT_DONE, "el":launched},
                         {"what": DONE},
                         reac_name="reac_done")
    reac_cancel = ConstantReaction(constants.THORPY_EVENT,
                         launcher.unlaunch_cancel,
                         {"id": constants.EVENT_CANCEL, "el":launched},
                         {"what": CANCEL},
                         reac_name="reac_cancel")
    if click_quit:
        reac_clickquit = Reaction(parameters.MOUSEBUTTONUP,
                                func_click_quit,
                                {"button":parameters.LEFT_CLICK_BUTTON},
                                {"launcher":launcher, "what":CLICK_QUIT},
                                reac_name="reac_clickquit")
        launched.add_reaction(reac_clickquit)
    launched.add_reaction(reac_done)
    launched.add_reaction(reac_cancel)
    return launcher

def launch(launched, click_quit=False, launching=None, autocenter=True):
    """Launch <launched> on the current menu."""
    launcher = get_launcher(launched, click_quit, launching, autocenter)
    launcher.launch()
    return launcher



def set_launcher(launching, launched, click_quit=False):
    """Set <launching> as a launcher (on click) for element <launched>.
    Return launcher object."""
    launcher = Launcher(launched, launching=launching)
    reac_enter = ConstantReaction(constants.THORPY_EVENT,
                         launcher.launch,
                         {"id": constants.EVENT_UNPRESS, "el":launching})
    reac_done = ConstantReaction(constants.THORPY_EVENT,
                         launcher.unlaunch,
                         {"id": constants.EVENT_DONE, "el":launched},
                         {"what": DONE})
    reac_cancel = ConstantReaction(constants.THORPY_EVENT,
                         launcher.unlaunch,
                         {"id": constants.EVENT_CANCEL, "el":launched},
                         {"what": CANCEL})
    if click_quit:
        reac_clickquit = Reaction(parameters.MOUSEBUTTONUP,
                                func_click_quit,
                                params={"launcher":launcher, "what":CLICK_QUIT})
        launched.add_reaction(reac_clickquit)
##    launcher.launching = launching
    launching.add_reaction(reac_enter)
    launched.add_reaction(reac_done)
    launched.add_reaction(reac_cancel)
    return launcher

def make_launcher(launched, text, click_quit=False):
    from thorpy.elements._wrappers import make_button
    button = make_button(text)
    set_launcher(button, launched, click_quit)
    return button

def post_done(el):
    el.message = True
    e = event.Event(constants.THORPY_EVENT, id=constants.EVENT_DONE, el=el)
    event.post(e)

def post_cancel(el):
    el.message = True
    e = event.Event(constants.THORPY_EVENT, id=constants.EVENT_CANCEL, el=el)
    event.post(e)

def make_ok_box(elements,ok_text="Ok"):
    ok = make_button(ok_text)
    ok.user_func = post_done
    linesize = max(e.get_fus_rect().w for e in elements+[ok])
    line = Line.make(linesize, "h")
    box = Box(elements=elements+[line,ok])
    box.finish()
    ok.user_params = {"el":box}
    box.e_ok = ok
    return box

def set_as_done_button(button, element_to_unlaunch):
    button.user_func = post_done
    button.user_params = {"el":element_to_unlaunch}

def set_as_cancel_button(button, element_to_unlaunch):
    button.user_func = post_cancel
    button.user_params = {"el":element_to_unlaunch}

def make_ok_cancel_box(elements, ok_text="Ok", cancel_text="Cancel"):
    ok = make_button(ok_text)
    ok.user_func = post_done
    #
    cancel = make_button(cancel_text)
    cancel.user_func = post_cancel
    #
##    ghost = Ghost(elements=[ok, cancel])
##    ghost.finish()
##    thorpy.store(ghost, mode="h")
##    ghost.fit_children()
    ok_cancel = make_stored_ghost([ok,cancel])
    #
    linesize = max(e.get_family_rect().w for e in elements+[ok_cancel])
    line = Line.make(linesize, "h")
    #
    box = Box(elements=elements+[line,ok_cancel])
    ok.user_params = {"el":box}
    cancel.user_params = {"el":box}
    box.e_ok = ok
    box.e_cancel = cancel
    return box

class Launcher(object):

    def __init__(self, launched, focus=True, exceptions=None, launching=None):
        self.launched = launched
        self.focus, self.exceptions = None, None
        self.set_focus(focus, exceptions)
        self.func_before = None
        self.func_after = None
        self.active_record = {}
        self.launching = launching
        self.autocenter = True
        self.how_exited = None

    def set_focus(self,value, exceptions=None):
        self.focus = value
        self.exceptions=[] if not exceptions else exceptions

    def add_to_current_menu(self):
        menu = functions.get_current_menu()
        menu.add_to_population(self.launched)

    def remove_from_current_menu(self):
        menu = functions.get_current_menu()
        if self.launched in menu.get_population():
            menu.remove_from_population(self.launched)
        else:
            functions.debug_msg("The launched element of the launcher has been\
            removed from the current menu by another element!")

    def save_active_records(self):
        self.active_record = {}
        menu = functions.get_current_menu()
        for e in menu.get_population():
            self.active_record[e] = e.active

    def restore_actives(self):
        for e in self.active_record:
            e.active = self.active_record[e]

    def activate_focus(self):
        self.save_active_records()
        if self.focus:
            menu = functions.get_current_menu()
            for e in menu.get_population():
                e.active = False
            for e in self.exceptions:
                e.active = True
        else:
            for e in self.exceptions:
                e.active = False

    def unfocus(self):
        self.restore_actives()
##        if self.focus:
##            menu = functions.get_current_menu()
##            #! could activate elements that were not active before launcher.. this will occur when
##            # launchers are imbricated !!!!! must be changed
##            for e in menu.get_population():
##                e.active = True
##        else:
##            for e in self.exceptions:
##                e.active = True

    def default_func_before(self):
        if self.autocenter:
            self.launched.center()
        self.launched.blit()
        self.launched.update()

    def prelaunch(self): #handles func_before (unblittings, blittings, reactions deactivations)
        if parameters.FILL_SCREEN_AT_SUBMENUS:
            functions.get_screen().fill(parameters.SCREEN_FILL)
            pygame.display.flip()
        if self.func_before is None:
            self.default_func_before()
        else:
            self.func_before()
        self.activate_focus()

##    def default_func_after(self):
##        self.launched.unblit()
##        a = functions.get_current_menu()._elements[0].get_oldest_ancester()
##        a.partial_blit(exception=None, rect=self.launched.get_fus_rect())
##        self.launched.update()
##        if self.launching:
##            aa = self.launching.get_oldest_ancester()
##            if aa:
##                aa.blit()
##                aa.update()

    def default_func_after(self):
        r = self.launched.get_family_rect()
##        self.launched.unblit()
        a = functions.get_current_menu()._elements[0].get_oldest_ancester()
        a.partial_blit(exception=None, rect=r)
##        self.launched.update()
        import pygame
        pygame.display.update(r)
        if self.launching:
            aa = self.launching.get_oldest_ancester()
            if aa:
                aa.blit()
                aa.update()

    def postlaunch(self):
        self.unfocus()
        if self.func_after is None:
            self.default_func_after()
        else:
            self.func_after()

    def launch(self):
        ev = event.Event(constants.THORPY_EVENT, id=constants.EVENT_LAUNCH,
                        launcher=self)
        event.post(ev)
        self.prelaunch()
        self.add_to_current_menu()

    def unlaunch(self, what=None):
        if what is None:
            what = self.launched
        ev = event.Event(constants.THORPY_EVENT, id=constants.EVENT_UNLAUNCH,
                        launcher=self, what=what)
        event.post(ev)
##        print(ev, "posted")
        self.remove_from_current_menu()
        self.postlaunch()

    def unlaunch_cancel(self, what=None):
        self.how_exited = "cancel"
        self.unlaunch(what)

    def unlaunch_done(self, what=None):
        self.how_exited = "done"
        self.unlaunch(what)


class _FakeLauncher:
    def __init__(self, how_exited):
        self.how_exited = how_exited

def launch_blocking(element, after=None, func=None, set_auto_ok=True,
                    add_ok_enter=None, set_auto_cancel=True, click_quit=False):
    if set_auto_ok:
        auto_ok(element)
    if set_auto_cancel:
        auto_cancel(element)
    if click_quit:
##        auto_click_quit(element)
        def click(e):
            if element.get_fus_rect().collidepoint(e.pos):
                if hasattr(element,"e_ok"):
                    emulate_ok_press(element.e_ok)
                elif hasattr(element, "e_cancel"):
                    post_cancel(element)
                    functions.quit_menu_func()
        element.add_reaction(Reaction(pygame.MOUSEBUTTONDOWN, click))
    from thorpy.elements.inserter import Inserter
    inserters = []
    if add_ok_enter is None: #auto detect
        add_ok_enter = True
        for e in [element]+list(element.get_descendants()):
            if isinstance(e, Inserter):
                inserters.append(e)
    if add_ok_enter:
        reac = ConstantReaction(pygame.KEYDOWN, emulate_ok_press,
                        {"key":pygame.K_RETURN}, {"element":element,
                                                    "inserters":inserters})
        element.add_reaction(reac)
    m = TickedMenu(element)
    m.play()
    if add_ok_enter:
        element.remove_reaction(reac)
    if after:
        after.unblit_and_reblit()
    if func:
        func()
    done = None
    cancel = None
    if hasattr(element, "e_ok"):
        done = element.e_ok.message
    if hasattr(element, "e_cancel"):
        cancel = element.e_cancel.message
    if done and not(cancel):
        return _FakeLauncher("done")
    elif cancel and not(done):
        return _FakeLauncher("cancel")
    elif done and cancel:
        raise Exception()
    else:
        return _FakeLauncher(None)


def emulate_ok_press(element, inserters=None):
    if inserters:
        for i in inserters:
            i.K_RETURN_pressed()
    post_done(element)
    functions.quit_menu_func()

def auto_ok(element):
    if hasattr(element,"e_ok"):
        element.e_ok.user_func = emulate_ok_press
        element.e_ok.user_params = {"element":element.e_ok}

def emulate_cancel_press(element, inserters=None):
    if inserters:
        for i in inserters:
            i.K_RETURN_pressed()
    post_cancel(element)
    functions.quit_menu_func()



def auto_cancel(element):
    if hasattr(element,"e_cancel"):
        element.e_cancel.user_func = emulate_cancel_press
        element.e_cancel.user_params = {"element":element.e_cancel}

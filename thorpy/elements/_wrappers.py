import pygame

from thorpy.painting.writer import Writer
from thorpy.elements.element import Element
from thorpy.elements.clickable import Clickable
from thorpy.elements.ghost import Ghost
from thorpy.elements.box import Box
from thorpy.elements.inserter import Inserter
from thorpy.miscgui.storage import store
from thorpy.miscgui import constants, style, functions
from thorpy.painting.painters.imageframe import ImageButton
import thorpy.painting.graphics as graphics

def make_textbox(text, font_size=None, font_color=None, ok_text="Ok"):
    if font_size is None: font_size = style.FONT_SIZE
    if font_color is None: font_color = style.FONT_COLOR
    from thorpy.miscgui.launchers.launcher import make_ok_box
    e_text = make_text(text, font_size, font_color)
    box = make_ok_box([e_text], ok_text=ok_text)
    return box

##def launch_blocking_alert(text, parent=None, font_size=None, font_color=None,
##                            ok_text="Ok"):
##    if font_size is None: font_size = style.FONT_SIZE
##    if font_color is None: font_color = style.FONT_COLOR
##    box_alert = make_textbox(text, font_size, font_color, ok_text)
##    box_alert.center()
##    from thorpy.menus.tickedmenu import TickedMenu
##    m = TickedMenu(box_alert)
##    box_alert.get_elements_by_text(ok_text)[0].user_func = functions.quit_menu_func
##    box_alert.get_elements_by_text(ok_text)[0].user_params = {}
##    m.play()
##    box_alert.unblit()
##    if parent:
##        parent.partial_blit(None, box_alert.get_fus_rect())
##        box_alert.update()

def launch_alert(text, font_size=None, font_color=None, ok_text="Ok"):
    if font_size is None: font_size = style.FONT_SIZE
    if font_color is None: font_color = style.FONT_COLOR
    from thorpy.miscgui.launchers.launcher import launch
    box_alert = make_textbox(text, font_size, font_color, ok_text)
    box_alert.center()
    launch(box_alert)

def launch_choices(text, choices, title_fontsize=None, title_fontcolor=None,
                    click_quit=False):
    """choices are tuple (text,func)"""
    if title_fontsize is None: title_fontsize = style.FONT_SIZE
    if title_fontcolor is None: title_fontcolor = style.FONT_COLOR
##    elements = [make_button(t,f) for t,f in choices]
    elements = []
    for choice in choices:
        if isinstance(choice, tuple):
            elements.append(make_button(choice[0],choice[1]))
        else:
            elements.append(choice)
    ghost = make_stored_ghost(elements)
    e_text = make_text(text, title_fontsize, title_fontcolor)
    box = Box.make([e_text, ghost])
    box.center()
    from thorpy.miscgui.launchers.launcher import launch
    from thorpy.miscgui.reaction import ConstantReaction, Reaction
    from thorpy import functions
    launcher = launch(box)
    for e in elements:
        reac = ConstantReaction(constants.THORPY_EVENT,
                                launcher.unlaunch,
                                {"id":constants.EVENT_UNPRESS, "el":e},
                                {"what":None})
        box.add_reaction(reac)
    def click_outside(e):
        if not box.get_fus_rect().collidepoint(e.pos):
            functions.quit_menu_func()
    box.add_reaction(Reaction(pygame.MOUSEBUTTONDOWN, click_outside))
    return launcher

def launch_blocking_choices(text, choices, parent=None, title_fontsize=None,
                    title_fontcolor=None, main_color=None, click_quit=False):
    """choices is a list of either tuple(text,func) or elements"""
    if title_fontsize is None: title_fontsize = style.FONT_SIZE
    if title_fontcolor is None: title_fontcolor = style.FONT_COLOR
##    elements = [make_button(t,f) for t,f in choices] #old form
    elements = []
    for choice in choices:
        if isinstance(choice, tuple):
            elements.append(make_button(choice[0],choice[1]))
        else:
            elements.append(choice)
    ghost = make_stored_ghost(elements)
    e_text = make_text(text, title_fontsize, title_fontcolor)
    box = Box.make([e_text, ghost])
    if main_color:
        box.set_main_color(main_color)
    box.center()
    from thorpy.miscgui.reaction import ConstantReaction, Reaction
    from thorpy import functions
    for e in elements:
        reac = ConstantReaction(constants.THORPY_EVENT,
                                functions.quit_menu_func,
                                {"id":constants.EVENT_UNPRESS,
                                 "el":e})
        box.add_reaction(reac)
    def click_outside(e):
        if not box.get_fus_rect().collidepoint(e.pos):
            functions.quit_menu_func()
    box.add_reaction(Reaction(pygame.MOUSEBUTTONDOWN, click_outside))
    from thorpy.menus.tickedmenu import TickedMenu
    m = TickedMenu(box)
    m.play()
    box.unblit()
    if parent:
        parent.partial_blit(None, box.get_fus_rect())
        box.update()

def launch_binary_choice(title_text, parent=None, title_fontsize=None,
                    title_fontcolor=None, main_color=None, yes_text="Yes",
                    no_text="No", blocking=True, click_quit=False):
    """Use <blocking> argument to decide wether or not the launch is blocking"""
    class Choice:
        value = False
    def yes():
        Choice.value = True
    choices = [(yes_text,yes), (no_text,None)]
    if blocking:
        launch_blocking_choices(title_text, choices, parent, title_fontsize,
                                title_fontcolor, main_color, click_quit)
    else:
        launch_choices(title_text, choices, parent, title_fontsize,
                        title_fontcolor, main_color, click_quit)
    return Choice.value

def launch_inserter(title_text, initial_value="", parent=None, title_fontsize=None,
                    title_fontcolor=None, main_color=None, blocking=True):
    from thorpy.miscgui.launchers.launcher import make_ok_box, auto_ok, launch_blocking
    ins = Inserter.make(title_text, value=initial_value)
    ins.center()
    ins.enter()
    launch_blocking(ins)
    parent.unblit_and_reblit()
    return ins.get_value()

def make_stored_ghost(elements, mode="h"):
    ghost = Ghost(elements)
    store(ghost, mode=mode)
    ghost.fit_children()
    return ghost


def make_button(text, func=None, params=None):
    button = Clickable(text)
    button.scale_to_title()
    if func:
        button.user_func = func
    if params:
        button.user_params = params
    return button

def make_image_button(img_normal, img_pressed=None, img_hover=None,
                        alpha=255, colorkey=None, text="",
                        force_convert_alpha=False):
    e = Clickable(text,finish=False)
    painter = ImageButton(img_normal, img_pressed, img_hover, alpha, colorkey,
                            force_convert_alpha=force_convert_alpha)
    e.set_painter(painter)
    e.finish()
    return e


def make_text(text, font_size=None, font_color=None):
    if font_size is None: font_size = style.FONT_SIZE
    if font_color is None: font_color = style.FONT_COLOR
    params = {"font_color":font_color, "font_size":font_size}
    button = Element(text, normal_params=params, finish=False)
    if not "\n" in text:
        button.set_style("text")
    button.finish()
    if "\n" in text:
        button.scale_to_title()
        button.set_main_color((0,0,0,0))
    return button

def make_font_setter(fn, const_text="", var_text="", ddl_size="auto"):
    from thorpy.elements.launchers.dropdownlistlauncher import DropDownListLauncher
    from thorpy.miscgui.reaction import Reaction
    from thorpy.miscgui.metadata import MetaDataManager
    import os, sys
    titles = list(constants.AVAILABLE_FONTS)
    titles.sort()
    button = DropDownListLauncher.make(const_text, var_text,
                                        titles,
                                        show_select=False,
                                        ddlf_size=ddl_size)
    def reac_func(event):
        font = event.value
        mdm = MetaDataManager()
        mdm.read_data(fn)
        mdm.data["font"] = font
        mdm.write_data(fn)
        #restart script
        python = sys.executable
        os.execl(python, python, * sys.argv)
    reac = Reaction(constants.THORPY_EVENT, reac_func, {"id":constants.EVENT_DDL,
                                                        "el":button})
    button.add_reaction(reac)
    return button

def make_fontsize_setter(fn, const_text="", slider_length=100, limvals=(6,36)):
    from thorpy.miscgui.reaction import Reaction
    from thorpy.miscgui.metadata import MetaDataManager
    from thorpy.elements.launchers.paramsetterlauncher import ParamSetterLauncher
    from thorpy.miscgui.varset import VarSet
    import os, sys
    varset = VarSet()
    varset.add("fontsize", value=style.FONT_SIZE, text="Font size:",
                limits=limvals, more={"length":slider_length})
    button = ParamSetterLauncher.make([varset], const_text, const_text,
                                        text_ok="Apply")
    def reac_func(event):
        if event.what == constants.LAUNCH_DONE:
            font_size = varset.get_value("fontsize")
            mdm = MetaDataManager()
            mdm.read_data(fn)
            mdm.data["font_size"] = font_size
##            print("writing", mdm.data, fn)
            mdm.write_data(fn)
            #restart script
            python = sys.executable
            os.execl(python, python, * sys.argv)
    reac = Reaction(constants.THORPY_EVENT, reac_func, {"id":constants.EVENT_UNLAUNCH,
                                                        "launcher":button.launcher})
    button.add_reaction(reac)
    return button

def make_font_options_setter(fn, const_text="", var_text="", ddl_size="auto",
                             slider_length=100, limvals=(6,36)):
    from thorpy.miscgui.reaction import Reaction
    from thorpy.miscgui.metadata import MetaDataManager
    from thorpy.elements.launchers.paramsetterlauncher import ParamSetterLauncher
    from thorpy.miscgui.varset import VarSet
    import os, sys
    varset = VarSet()
    titles = list(constants.AVAILABLE_FONTS)
    titles.sort()
    current_font = functions.get_default_font_infos()["name"]
    varset.add("fontname", titles, text="Font: ", more={"ddlf_size":ddl_size,
                                                        "var_text":current_font})
    varset.add("fontsize", value=style.FONT_SIZE, text="Font size:",
                limits=limvals, more={"length":slider_length})
    button = ParamSetterLauncher.make([varset], const_text, const_text,
                                        text_ok="Apply")
    def reac_func(event):
        if event.what == constants.LAUNCH_DONE:
            font_size = varset.get_value("fontsize")
            font_name = varset.get_value("fontname")
##            print("font_name=", font_name)
            mdm = MetaDataManager()
            mdm.read_data(fn)
            mdm.data["font_size"] = font_size
            mdm.data["font"] = font_name
##            print("writing", mdm.data, fn)
            mdm.write_data(fn)
            #restart script
            python = sys.executable
            os.execl(python, python, * sys.argv)
    reac = Reaction(constants.THORPY_EVENT, reac_func, {"id":constants.EVENT_UNLAUNCH,
                                                        "launcher":button.launcher})
    button.add_reaction(reac)
    return button

def make_display_options_setter(fn, const_text="",
                                sliders_length=100,
                                limvalsw=(400,None),
                                limvalsh=(400,None),
                                restart_app=True):
    from thorpy.miscgui.reaction import Reaction
    from thorpy.miscgui.metadata import MetaDataManager
    from thorpy.elements.launchers.paramsetterlauncher import ParamSetterLauncher
    from thorpy.miscgui.varset import VarSet
    import os, sys
    varset = VarSet()
    w,h = functions.get_screen_size()
    maxsize = functions.get_max_screen_size()
    if limvalsw[1] is None: limvalsw = (limvalsw[0], maxsize[0])
    if limvalsh[1] is None: limvalsh = (limvalsh[0], maxsize[1])
    fullscreen = bool(functions.get_screen().get_flags()&pygame.FULLSCREEN)
    varset.add("screen_w", value=int(w), text="Screen width: ", limits=limvalsw)
    varset.add("screen_h", value=int(h), text="Screen height: ", limits=limvalsh)
    varset.add("fullscreen", value=fullscreen, text="Fullscreen")
    button = ParamSetterLauncher.make([varset], const_text, const_text,
                                      text_ok="Apply")
    def reac_func_norestart(event):
        if event.what == constants.LAUNCH_DONE:
            w,h = varset.get_value("screen_w"), varset.get_value("screen_h")
            mdm = MetaDataManager()
            mdm.read_data(fn)
            mdm.data["screen_w"] = w
            mdm.data["screen_h"] = h
            mdm.data["fullscreen"] = varset.get_value("fullscreen")
##            print("writing", mdm.data, fn)
            mdm.write_data(fn)
            #restart script
            flags = functions.get_screen().get_flags()
            if varset.get_value("fullscreen"):
                flags |= pygame.FULLSCREEN
            else:
                flags = 0
            pygame.display.set_mode((w,h), flags)
            functions.get_current_menu()._elements[0].get_oldest_ancester().unblit_and_reblit()
            button.launched.blit()
            button.launched.update()

    def reac_func_restart(event):
        if event.what == constants.LAUNCH_DONE:
            w,h = varset.get_value("screen_w"), varset.get_value("screen_h")
            mdm = MetaDataManager()
            mdm.read_data(fn)
            mdm.data["screen_w"] = w
            mdm.data["screen_h"] = h
            mdm.data["fullscreen"] = varset.get_value("fullscreen")
##            print("writing", mdm.data, fn)
            mdm.write_data(fn)
            #restart script
            python = sys.executable
            os.execl(python, python, * sys.argv)

    reac_func=reac_func_restart if restart_app else reac_func_norestart
    reac = Reaction(constants.THORPY_EVENT, reac_func, {"id":constants.EVENT_UNLAUNCH,
                                                        "launcher":button.launcher})
    button.add_reaction(reac)
    return button

def make_global_display_options(fn, text):
    """Returns a button to launch font and display options"""
    from thorpy.miscgui.launchers.launcher import make_ok_box, make_launcher
    font_options = make_font_options_setter(fn, "Font options")
    disp_options = make_display_options_setter(fn, "Display options")
    box = make_ok_box([disp_options, font_options], "Return")
    return make_launcher(box, text)
##    return box

def make_menu_button(frame_size=(40,40), lines_size=(25,2), lines_radius=1,
                     lines_color=(0,0,0),
                     lines_color_hover=(0,0,200),
                     n=3, force_convert_alpha=False):
    e = make_button("")
    e.set_size(frame_size)
    imgs = {}
    for state in e.get_states():
        img = e.get_image(state).copy()
        frame = img.get_rect()
        line = graphics.get_aa_round_rect(lines_size, lines_radius, lines_color)
        rect = line.get_rect()
        rect.centerx = frame.centerx
        margin = frame.h//3
        gap = (frame.h - 2*margin - n*rect.h) // (n-1)
        for y in range(n):
            rect.y = margin + y*(gap+rect.h)
            img.blit(line, rect.topleft)
        imgs[state] = img
    #
    img_hover = e.get_image(constants.STATE_NORMAL).copy()
    frame = img.get_rect()
    line = graphics.get_aa_round_rect(lines_size, lines_radius, lines_color_hover)
    rect = line.get_rect()
    rect.centerx = frame.centerx
    margin = frame.h//3
    gap = (frame.h - 2*margin - n*rect.h) // (n-1)
    for y in range(n):
        rect.y = margin + y*(gap+rect.h)
        img_hover.blit(line, rect.topleft)
    e = make_image_button(imgs[constants.STATE_NORMAL],
                            imgs[constants.STATE_PRESSED],
                            img_hover,
                            force_convert_alpha=force_convert_alpha)
    return e


class SliderInserter:

    def __init__(self, text, length, limvals, initial_value,
                    reblit=None, type_=float, order="ins"):
        import thorpy
        self.text = thorpy.make_button(text, self.focus)
        self.slider = thorpy.SliderX.make(length, limvals, "", type_, initial_value)
        self.ins = thorpy.Inserter.make("", value=str(initial_value))
        if order == "ins":
            els = [self.text, self.ins, self.slider]
        else:
            els = [self.text, self.slider, self.ins]
        self.e = thorpy.make_group(els)
        reac_slide = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=self.at_slide,
                                event_args={"id":thorpy.constants.EVENT_SLIDE})
        reac_ins = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                        reac_func=self.at_insert,
                                        event_args={"id":thorpy.constants.EVENT_INSERT})
        self.e.add_reactions([reac_slide, reac_ins])
        self.e._manager = self
        self.ins._manager = self
        self.slider._manager = self
        self.e.get_value = self.slider.get_value
        self.reblit = reblit
        if not self.reblit:
            self.reblit = self.e.unblit_and_reblit

    def ins2slide(self):
        val = self.slider._value_type(self.ins.get_value())
        if val > self.slider.limvals[1]:
            val = self.slider.limvals[1]
            self.ins.set_value(str(val))
        elif val < self.slider.limvals[0]:
            val = self.slider.limvals[1]
            self.ins.set_value(str(val))
        self.slider.set_value(val)

    def slide2ins(self):
        self.ins.set_value(str(self.slider.get_value()))

    def at_slide(self, event):
        if event.el._manager is self:
            self.slide2ins()
            self.reblit()

    def at_insert(self, event):
        if event.el._manager is self:
            self.ins2slide()
            self.reblit()

    def focus(self):
        self.ins.enter()


def make_slider_inserter(text, length, limvals, initial_value, reblit=None, type_=float,
                            order="ins"):
    return SliderInserter(text, length, limvals, initial_value, reblit, type_, order).e



def get_user_text(title, value, size=(None,None)):
    from thorpy.miscgui.launchers.launcher import make_ok_box, auto_ok, launch_blocking
    ins = Inserter.make(title,value=value,size=size)
    box = make_ok_box([ins])
    auto_ok(box)
    box.center()
    ins.enter()
    launch_blocking(box)
    return ins.get_value()


def bicolor_text(text, font_size, color1, color2, space=0):
    import thorpy
    get_shadow = thorpy.graphics.get_shadow
    writer = Writer(size=font_size)
    width = writer.get_width(text) + (len(text)-1)*space
    height = writer.get_height()
    surface = pygame.Surface((width, height))
    alpha_color = (50,100,150)
    surface.fill(alpha_color)
    surface.set_colorkey(alpha_color)
    x = 0
    for letter in text:
        img = make_text(letter, font_size-20, color1).get_image()
        shad = get_shadow(img, shadow_radius=0, black=255,
                            color_format="RGBA", alpha_factor=1.,
                            decay_mode="exponential", color=color2,
                            sun_angle=45., vertical=True, angle_mode="flip",
                            mode_value=(False, False))
        size = shad.get_rect().inflate(6,6).size
        shad = pygame.transform.smoothscale(shad, size)
        img1 = shad
        img2 = img
        r1 = img1.get_rect()
        r1.left = x
        r2 = img2.get_rect()
        r2.center = r1.center
        surface.blit(img1, r1)
        surface.blit(img2, r2)
        x += img1.get_width() + space
    return surface

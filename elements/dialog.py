"""This module provides (non)blocking alert and choices similar to the default
ones in ThorPy, but the launched element is richer (title, hline...)"""

import thorpy, pygame

def make_textbox(title, text, font_size=None, font_color=None, ok_text="Ok",
                    hline=0, elements=None):
    from thorpy.miscgui.launchers.launcher import make_ok_box
    els = []
    if title:
        els += [thorpy.make_text(title, thorpy.style.TITLE_FONT_SIZE, (255,0,0))]
    if hline < 0:
        els += [thorpy.Line.make(e_title.get_size()[0],"h")]
    elif hline > 0:
        els += [thorpy.Line.make(hline,"h")]
    if text:
        els += [thorpy.make_text(text, font_size, font_color)]
    if elements is None: elements = []
    els += elements
    box = make_ok_box(els, ok_text=ok_text)
    return box

##def make_choice(title, text, font_size=None, font_color=None, ok_text="Ok",
##                cancel_text="Cancel"):
##    from thorpy.miscgui.launchers.launcher import make_ok_cancel_box
##    e_title = thorpy.make_text(title, thorpy.style.TITLE_FONT_SIZE, (255,0,0))
##    e_text = thorpy.make_text(text, font_size, font_color)
##    box = make_ok_cancel_box([e_title,e_text], ok_text=ok_text,
##                                cancel_text=cancel_text)
##    return box

def launch_blocking_alert(title, text, parent=None, font_size=None, font_color=None,
                            ok_text="Ok", transp=False, alpha_dialog=200, func=None,
                            outside_click_quit=False):
    if font_size is None: font_size = thorpy.style.FONT_SIZE
    if font_color is None: font_color = thorpy.style.FONT_COLOR
    box_alert = make_textbox(title, text, font_size, font_color, ok_text)
    box_alert.center()
    if transp:
        color_transp = tuple(list(thorpy.style.DEF_COLOR)[:3]+[alpha_dialog])
        box_alert.set_main_color(color_transp)
    def click_quit(e):
        if not box_alert.get_fus_rect().collidepoint(e.pos):
            thorpy.functions.quit_menu_func()
    if outside_click_quit:
        box_alert.add_reaction(thorpy.Reaction(pygame.MOUSEBUTTONDOWN, click_quit))
    from thorpy.menus.tickedmenu import TickedMenu
    m = TickedMenu(box_alert)
    box_alert.get_elements_by_text(ok_text)[0].user_func = thorpy.functions.quit_menu_func
    box_alert.get_elements_by_text(ok_text)[0].user_params = {}
    m.play()
    box_alert.unblit()
    if parent:
        parent.partial_blit(None, box_alert.get_fus_rect())
        box_alert.update()
    if func:
        func()


def launch_blocking_choices(text, choices, parent=None, title_fontsize=None,
                            title_fontcolor=None, func=None):
    """choices are tuple (text,func)"""
    if title_fontsize is None: title_fontsize = thorpy.style.FONT_SIZE
    if title_fontcolor is None: title_fontcolor = thorpy.style.FONT_COLOR
    elements = [thorpy.make_button(t,f) for t,f in choices]
    ghost = thorpy.make_group(elements)
    e_text = thorpy.make_text(text, title_fontsize, title_fontcolor)
    box = thorpy.Box.make([e_text, ghost])
    box.center()
    from thorpy.miscgui.reaction import ConstantReaction
    for e in elements:
        reac = ConstantReaction(thorpy.constants.THORPY_EVENT,
                                thorpy.functions.quit_menu_func,
                                {"id":thorpy.constants.EVENT_UNPRESS,
                                 "el":e})
        box.add_reaction(reac)
    from thorpy.menus.tickedmenu import TickedMenu
    m = TickedMenu(box)
    m.play()
    box.unblit()
    if parent:
        parent.partial_blit(None, box.get_fus_rect())
        box.update()
    if func:
        func()

def launch_blocking_choices_str(text, choices, parent=None, title_fontsize=None,
                            title_fontcolor=None, func=None, store="v"):
    """choices are tuple (text,func)"""
    if title_fontsize is None: title_fontsize = thorpy.style.FONT_SIZE
    if title_fontcolor is None: title_fontcolor = thorpy.style.FONT_COLOR
    class Choice:
        value = None
    def choice_func(value):
        Choice.value = value
    elements = []
    for name in choices:
        e = thorpy.make_button(name, choice_func, {"value":name})
        elements.append(e)
    ghost = thorpy.make_group(elements, mode=store)
    e_text = thorpy.make_text(text, title_fontsize, title_fontcolor)
    box = thorpy.Box.make([e_text, thorpy.Line(100,"h"), ghost])
    box.center()
    from thorpy.miscgui.reaction import ConstantReaction
    for e in elements:
        reac = ConstantReaction(thorpy.constants.THORPY_EVENT,
                                thorpy.functions.quit_menu_func,
                                {"id":thorpy.constants.EVENT_UNPRESS,
                                 "el":e})
        box.add_reaction(reac)
    def click_outside(e):
        if not box.get_fus_rect().collidepoint(e.pos):
            thorpy.functions.quit_menu_func()
    reac = thorpy.Reaction(pygame.MOUSEBUTTONDOWN, click_outside)
    box.add_reaction(reac)
    from thorpy.menus.tickedmenu import TickedMenu
    m = TickedMenu(box)
    m.play()
    box.unblit()
    if parent:
        parent.partial_blit(None, box.get_fus_rect())
        box.update()
    if func:
        func()
    return Choice.value

def launch_nonblocking_alert(title, text, parent=None, font_size=None,
                             font_color=None, ok_text="Ok", transp=False,
                             alpha_dialog=200, func=None):
    if font_size is None: font_size = thorpy.style.FONT_SIZE
    if font_color is None: font_color = thorpy.style.FONT_COLOR
    box_alert = make_textbox(title, text, font_size, font_color, ok_text)
    box_alert.center()
    if transp:
        color_transp = tuple(list(thorpy.style.DEF_COLOR)[:3]+[alpha_dialog])
        box_alert.set_main_color(color_transp)
    thorpy.launch_nonblocking(box_alert)


def launch_nonblocking_choices(text, choices, parent=None, title_fontsize=None,
                            title_fontcolor=None, func=None):
    """choices are tuple (text,func)"""
    from thorpy.miscgui.launchers.launcher import post_done
    if title_fontsize is None: title_fontsize = thorpy.style.FONT_SIZE
    if title_fontcolor is None: title_fontcolor = thorpy.style.FONT_COLOR
    elements = [thorpy.make_button(t,f) for t,f in choices]
    ghost = thorpy.make_group(elements)
    e_text = thorpy.make_text(text, title_fontsize, title_fontcolor)
    box = thorpy.Box.make([e_text, ghost])
    box.center()
    from thorpy.miscgui.reaction import ConstantReaction
    for e in elements:
        reac = ConstantReaction(thorpy.constants.THORPY_EVENT,
                                post_done,
                                {"id":thorpy.constants.EVENT_UNPRESS, "el":e},
                                {"el":box})
        box.add_reaction(reac)
    thorpy.launch_nonblocking(box)

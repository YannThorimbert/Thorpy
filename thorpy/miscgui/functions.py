import pygame.event as pygame_event
import pygame


from thorpy.miscgui import constants, application, parameters

def get_max_screen_size():
    infoObject = pygame.display.Info()
    w,h = (infoObject.current_w, infoObject.current_h)

def obtain_valid_painter(painter_class, **kwargs):
    """Returns a valid painter whose class is <painter_class>. You can try any
    argument you want ; only arguments existing in painter's __init__ method
    will be used.
    """
    try:
        painter = painter_class(**kwargs)
    except TypeError:
        painter = painter_class()
        args_okay = {}
        for arg in kwargs:
            if hasattr(painter, arg):
                args_okay[arg] = kwargs[arg]
        painter = painter_class(**args_okay)
    return painter

def keypress(element, newstate):
    """Make <element> goes in state <newstate>, refreshing the display."""
    element.change_state(newstate)
    element.unblit()
    element.blit()
    element.update()

def quit_func():
    """Post quit event."""
    pygame_event.post(constants.EVENT_QUIT)

def set_current_menu(menu):
    debug_msg("Set current menu: ", menu)
    application._OLD_MENUS.append(application._CURRENT_MENU)
    application._CURRENT_MENU = menu

def quit_menu_func():
    """Leaves the current menu and set the new one as the previous one."""
    debug_msg("Quit menu func", application._CURRENT_MENU)
    application._CURRENT_MENU.set_leave()
    application._CURRENT_MENU = application._OLD_MENUS.pop()

def add_element_to_current_menu(element):
    debug_msg("add element to current menu: " + element.get_text())
    application._CURRENT_MENU.add_to_population(element)

def get_current_menu():
    return application._CURRENT_MENU

def get_current_application():
    return application._CURRENT_APPLICATION

def get_screen():
    return pygame.display.get_surface()
##    return application._SCREEN

def get_screen_size():
    return get_screen().get_rect().size

def refresh_current_menu():
    """Refreshes the current menu events. Use it to include newly added
    elements. Returns True if a menu has been refreshed, else returns False.
    """
    debug_msg("Refreshing current menu.")
    current_menu = get_current_menu()
    if current_menu:
        current_menu.refresh()
        return True
    else:
        return False

def debug_msg(*content):
    if application.DEBUG_MODE:
        str_content = list()
        for e in content:
            str_content.append(str(e) + " ")
        print("Thorpy debug : " + ''.join(str_content))

def info_msg(*content):
    if application.DEBUG_MODE:
        str_content = list()
        for e in content:
            str_content.append(str(e) + " ")
        print("Thorpy info : " + ''.join(str_content))

def get_fps():
    return application._CURRENT_MENU.clock.get_fps()

def remove_element(element):
    removed = False
    current_menu = get_current_menu()
    if current_menu:
        for e in current_menu.get_population():
            if element in e.get_elements():
                e.remove_elements([element])
                removed = True
        if element in current_menu.get_population():
            population = get_current_menu.get_population()
            population.remove(element)
            removed = True
    else:
        debug_msg("Could not remove element", element, " since there is no\
                    current menu.")
    if removed:
        refresh_current_menu()

def get_default_font_infos():
    from thorpy.painting.writer import get_font_name
    from thorpy.miscgui import style
    return {"name":get_font_name(None), "size":style.FONT_SIZE}

def writing(delay=30,interval=100,interval_pygame=500):
    parameters.KEY_DELAY = delay
    parameters.KEY_INTERVAL = interval
    pygame.key.set_repeat(delay,interval_pygame)

def playing(delay,interval):
    parameters.KEY_DELAY = delay
    parameters.KEY_INTERVAL = interval
    pygame.key.set_repeat(delay,interval)
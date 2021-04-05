#ThorPy real life tutorial : full final code
import thorpy

def refresh_sliders(event, drag, sx, sy):
    if event.el == drag:
        pos_drag = drag.get_rect().topleft
        sx.unblit_and_reblit_func(sx.set_value, value=pos_drag[0])
        sy.unblit_and_reblit_func(sy.set_value, value=pos_drag[1])

def refresh_drag(event, drag, sx, sy):
    if event.el == sx or event.el == sy:
        drag.unblit_and_reblit_func(drag.set_topleft,
                                    pos=(sx.get_value(), sy.get_value()))

def run_application():
    W, H = 300, 300
    application = thorpy.Application(size=(W,H), caption="Real life example")

    draggable = thorpy.Draggable("Drag me")
    sx = thorpy.SliderX(length=100, limvals=(0, W), text="X:", type_=int)
    sy = thorpy.SliderX(length=100, limvals=(0, H), text="Y:", type_=int)

    background = thorpy.Background(color=(200,255,255),
                                        elements=[draggable, sx, sy])
    thorpy.store(background, [sx, sy])

    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=refresh_drag,
                                event_args={"id":thorpy.constants.EVENT_SLIDE},
                                params={"drag":draggable, "sx":sx, "sy":sy},
                                reac_name="my reaction to slide event")

    reaction2 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=refresh_sliders,
                                event_args={"id":thorpy.constants.EVENT_DRAG},
                                params={"drag":draggable, "sx":sx, "sy":sy},
                                reac_name="my reaction to drag event")

    background.add_reaction(reaction1)
    background.add_reaction(reaction2)

    menu = thorpy.Menu(background) #create a menu for auto events handling
    menu.play() #launch the menu
    application.quit()

run_application()
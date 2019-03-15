"""Example from www.thorpy.org/examples.html"""
import thorpy,pygame

application = thorpy.Application((800, 600), "ThorPy Overview")

bar = thorpy.LifeBar("Remaining time",
                        color=(255,165,0),
                        text_color=(0,0,0),
                        size=(200,30),
                        font_size=None, #keep default one
                        type_="h") #h or v
bar.center()

counter = 0
def event_time():
    global counter
    if counter%4 == 0:
        life = min(1.,counter/500.)
        bar.set_life(life)
        bar.set_text(str(counter))
        bar.unblit_and_reblit()
    if counter < 500:
        counter += 1

bar.add_reaction(thorpy.ConstantReaction(thorpy.THORPY_EVENT,
                                        event_time,
                                        {"id":thorpy.constants.EVENT_TIME}))

menu = thorpy.Menu(bar)
menu.play()

application.quit()

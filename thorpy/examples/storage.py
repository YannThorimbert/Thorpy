#ThorPy storage tutorial : manual placing
import thorpy, random

application = thorpy.Application(size=(400, 400), caption="Storage")

elements = [thorpy.make_button("button" + str(i)) for i in range(13)]
for e in elements:
    w, h = e.get_rect().size
    w, h = w*(1+random.random()/2.), h*(1+random.random()/2.)
    e.set_size((w,h))
elements[6] = thorpy.Element(text="")
elements[6].set_size((100,100))

elements[0].set_topleft((10, 300))
elements[1].set_topleft(elements[0].get_rect().bottomright)
elements[2].set_center((100, 200))
elements[3].stick_to(elements[2], target_side="bottom", self_side="top")
elements[4].stick_to(elements[2], target_side="right", self_side="left")

background = thorpy.Background(color=(200, 200, 255), elements=elements)
thorpy.store(background, elements[6:12], x=380, align="right")
elements[5].center(element=elements[6])
elements[5].rank = elements[6].rank + 0.1 #be sure number 5 is blitted after 6
background.sort_children_by_rank() #tell background to sort its children
elements[12].set_location((0.1, 0.2)) #relative placing of number 12

menu = thorpy.Menu(background)
menu.play()

application.quit()
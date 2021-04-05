import thorpy

ap = thorpy.Application((300,300))

#format of a Pool : thorpy.Pool(elements, first_value, always_value)
#   <first_value> can be None, and is the element that is 'on' at the beginning
#   <always_value>=True means that there must always be an element which is 'on'

#make radios
radios = [thorpy.Checker("radio"+str(i), type_="radio") for i in range(4)]
radio_pool = thorpy.RadioPool(radios, first_value=radios[2], always_value=True)

#make togglable buttons
buttons = [thorpy.Togglable("togglable"+str(i)) for i in range(4)]
togglable_pool = thorpy.TogglablePool(buttons, first_value=buttons[1],
                                                        always_value=False)

#cosmetic separation line
line = thorpy.Line(200, "h")

bck = thorpy.Background.make((220,220,255), elements=radios+[line]+buttons)
thorpy.store(bck)
menu = thorpy.Menu(bck)
menu.play()
ap.quit()
import thorpy

application = thorpy.Application(size=(500, 500))

thorpy.set_theme("round")

def launch_menu(choices):
    title = thorpy.make_text("Choose something", 14, (255,0,0))
    #now define the behaviour of clicked elements
    def at_press(what):
        some_text.set_text(what) #change the element content (see below)
        thorpy.functions.quit_menu_func() #exit the menu
        thorpy.store(background) #align the elements (size has changed)
        background.unblit_and_reblit()
    #dynamically create elements
    elements = []
    for text in choices:
        element = thorpy.make_button(text, func=at_press)
        element.user_params = {"what":text}
        elements.append(element)
    #box to store everything
    box = thorpy.Box([title] + elements)
    box.set_main_color((200,200,200,150))
    box.center()
    m = thorpy.Menu(box)
    m.play()

some_text = thorpy.make_text("Click on the button below to change the text.", 18)
choices = ["My new text", "Another proposition", "Blah", "blah"]
button = thorpy.make_button("Change text", launch_menu, {"choices":choices})
background = thorpy.Background(elements=[some_text,button])
thorpy.store(background)


menu = thorpy.Menu(background)
menu.play()

application.quit()
import thorpy
"""
In this example, a box opens in which the user can choose between turning the
background blue or red (or do nothing).
"""

def set_blue():
    background.set_main_color((0,0,255))
    background.unblit_and_reblit()

def set_red():
    background.set_main_color((255,0,0))
    background.unblit_and_reblit()

def my_choices_1():
    choices = [("I like blue",set_blue), ("No! red",set_red), ("cancel",None)]
    thorpy.launch_nonblocking_choices("This is a non-blocking choices box!\n",
                                        choices)
    print("Proof that it is non-blocking : this sentence is printing!")

def my_choices_2():
    choices = [("I like blue",set_blue), ("No! red",set_red), ("cancel",None)]
    thorpy.launch_blocking_choices("Blocking choices box!\n", choices,
                                    parent=background) #for auto unblit
    print("This sentence will print only after you clicked ok")

application = thorpy.Application((500,500), "Launching alerts")

button1 = thorpy.make_button("Non-blocking version", func=my_choices_1)
button2 = thorpy.make_button("Blocking version", func=my_choices_2)

background = thorpy.Background(elements=[button1,button2])
thorpy.store(background)

menu = thorpy.Menu(background)
menu.play()

application.quit()
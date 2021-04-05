"""Show how to launch alerts. 2 types of alerts are available: blocking and
non-blocking. Both are presented below.
"""
import thorpy

def my_alert_1():
    thorpy.launch_nonblocking_alert(title="This is a non-blocking alert!",
                                text="This is the text..",
                                ok_text="Ok, I've read",
                                font_size=12,
                                font_color=(255,0,0))
    print("Proof that it is non-blocking : this sentence is printing at exit!")

def my_alert_2():
    thorpy.launch_blocking_alert(title="This is a blocking alert!",
                                 text="This is the text of the alert...",
                                 parent=background) #for auto-unblitting
    print("This sentence will print only after you clicked ok")

def my_launch():
    some_element = thorpy.make_text("My text...", font_size=18)
    another_element = thorpy.make_button("Quit")
    box = thorpy.Box.make([some_element, another_element])
    thorpy.set_as_done_button(another_element,box)#could be set_as_cancel_button
    thorpy.launch_nonblocking(box) #could also use thorpy.launch_blocking...

application = thorpy.Application((500,500), "Launching alerts")

button1 = thorpy.make_button("Non-blocking alert", func=my_alert_1)
button2 = thorpy.make_button("Blocking alert", func=my_alert_2)
button3 = thorpy.make_button("Launch element", func=my_launch)

background = thorpy.Background(elements=[button1,button2,button3])
thorpy.store(background, x=10, align="left") # put the menu on the left

menu = thorpy.Menu(background)
menu.play()

application.quit()
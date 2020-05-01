"""Script showing several ways to launch things.

Note: never call set_launcher(launching, launched) if <launched> can be launched
by another element and <launching> is NOT in the same menu.
"""
import thorpy, pygame

application = thorpy.Application((500,500), "Advanced menus")

# ****************** First launcher : button 1 ******************
#This launcher launches a simple button
my_element = thorpy.make_button("I am a useless button\nClick outside to quit.")
button1 = thorpy.make_button("Launcher 1")
#we set click_quit=True below, because we did not provide a "ok" and/or "cancel"
#button to the user. Element disappears When user clicks outside it.
thorpy.set_launcher(button1, my_element, click_quit=True)

# ****************** Second launcher : button 2 ******************
#here the element to be launched is a box with ok and cancel buttons + custom
#elements. We can also use make_ok_box, with only 1 text.
#Note that DONE_EVENT and CANCEL_EVENT are posted accordingly at unlaunch.
box = thorpy.make_ok_cancel_box([thorpy.make_button(str(i)) for i in range(8)],
                                 ok_text="Ok", cancel_text="Cancel")
button2 = thorpy.make_button("Launcher 2")
thorpy.set_launcher(button2, box)

# ****************** Third launcher : button 3 ******************
#This launcher launches a box, set it green, and changes screen color when
#unlaunched.
button3 = thorpy.make_button("Launcher 3")
other_box = thorpy.make_ok_box([thorpy.make_text("Color is gonna change...")])
my_launcher = thorpy.set_launcher(button3, other_box)#this time get the launcher
#we specify some custom operations that have to be done before/after launching:
def my_func_before():
    my_launcher.launched.set_main_color((0,255,0)) #change launched box color
    my_launcher.default_func_before() #default stuff
def my_func_after():
    background.set_main_color((0,100,100)) #change background color
    my_launcher.default_func_after() #default stuff

my_launcher.func_before = my_func_before
my_launcher.func_after = my_func_after

# ****************** Fourth launcher : event ******************
#This launcher is not linked to a ThorPy element, but instead user can activate
#it by pressing SPACE
unlaunch_button = thorpy.make_ok_box([thorpy.make_text("Ready to unlaunch?")])
unlaunch_button.stick_to("screen", "top", "top")
invisible_launcher = thorpy.get_launcher(unlaunch_button, autocenter=False)
# set focus to False for non-blocking behaviour:
##invisible_launcher.focus = False
#this reaction will be added to the background:
reac = thorpy.ConstantReaction(pygame.KEYDOWN, invisible_launcher.launch,
                                {"key":pygame.K_SPACE})
#add a text so user knows what to do
text4 = thorpy.make_text("Press space to launch invisible_launcher", 15)


background = thorpy.Background(elements=[text4, button1, button2, button3])
background.add_reaction(reac)
thorpy.store(background)

menu = thorpy.Menu(background)
menu.play()

application.quit()
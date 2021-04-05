import thorpy

application = thorpy.Application((800, 600), "ThorPy Overview")

text = thorpy.make_text("Some text", 12, (0,0,255))
line = thorpy.Line(200, "h") #horizontal line of width = 200px

element = thorpy.Element("Element")
thorpy.makeup.add_basic_help(element,"Element:\nMost simple graphical element.")

clickable = thorpy.Clickable("Clickable")
thorpy.makeup.add_basic_help(clickable,"Clickable:\nCan be hovered and pressed.")

draggable = thorpy.Draggable("Draggable")
thorpy.makeup.add_basic_help(draggable,"Draggable:\nYou can drag it.")

checker_check = thorpy.Checker("Checker")

checker_radio = thorpy.Checker("Radio", type_="radio")

browser = thorpy.Browser("../../", text="Browser")

browserlauncher = thorpy.BrowserLauncher(browser, const_text="Choose file:",
                                                var_text="")
browserlauncher.max_chars = 15 #limit size of browser launcher

dropdownlist = thorpy.DropDownListLauncher(const_text="Choose:",
                                                var_text="",
                                         titles=[str(i)*i for i in range(1, 9)])
dropdownlist.scale_to_title()
dropdownlist.max_chars = 12 #limit size of drop down list

slider = thorpy.SliderX(80, (5, 12), "Slider: ", type_=float,
                                initial_value=8.4)

inserter = thorpy.Inserter(name="Inserter: ", value="Write here.")

title_element = thorpy.make_text("Overview example", 22, (255,0,0))

elements = [text, line, element, clickable, draggable, checker_check,
            checker_radio, dropdownlist, browserlauncher, slider, inserter]
central_box = thorpy.Box(elements=elements)
central_box.fit_children(margins=(30,30)) #we want big margins
central_box.center() #center on screen
central_box.add_lift() #add a lift (useless since box fits children)
central_box.set_main_color((220,220,220,180)) #set box color and opacity

background = thorpy.Background(image=thorpy.style.EXAMPLE_IMG,
                                    elements=[title_element, central_box])
thorpy.store(background)

menu = thorpy.Menu(background)
menu.play()

application.quit()
"""Show how to use image to make buttons. Here 2 buttons are created."""

import thorpy, pygame

application = thorpy.Application((500,500), "Image buttons")

root = "../documentation/examples/"
normal, pressed, hover = "normal.png", "pressed.png", "hover.png"

button1 = thorpy.make_image_button(root+normal, root+pressed, root+hover,
                                    alpha=255, #opaque
                                    colorkey=(255,255,255)) #white=transparent

#this time a very simple button, with a text (only 1 image)
button2 = thorpy.make_image_button(root+hover, colorkey=False, text="Hello")


background = thorpy.Background(image=thorpy.style.EXAMPLE_IMG,
                                    elements=[button1, button2])
thorpy.store(background)

menu = thorpy.Menu(background)
menu.play()

application.quit()
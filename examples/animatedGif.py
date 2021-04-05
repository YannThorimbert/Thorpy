"""Example from www.thorpy.org/examples.html"""
import thorpy

application = thorpy.Application((800, 600), "Example of animated gif")

gif_element = thorpy.AnimatedGif("../documentation/examples/myGif.gif")
gif_element.center()

menu = thorpy.Menu(gif_element)
menu.play()

application.quit()

"""
Other parameters to pass to the constructor of AnimatedGif:
        <path>: the path to the image.
        <color>: if path is None, use this color instead of image.
        <low>: increase this parameter to lower the gif speed.
        <nread>: number of times the gif is played
"""

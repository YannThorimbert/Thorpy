from thorpy.elements.element import Element
from thorpy.painting.painters.imageframe import ImageFrame
from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui import style


class Image(Element):
    """Image element."""

    @staticmethod
    def make(path=None, color=None, colorkey=None):
        """Image element.
        <path>: the path to the image.
        <color>: if path is None, use this color instead of image.
        """
        img = Image(path, color, colorkey=colorkey, finish=False)
        img.finish()
        return img

    def __init__(self, path=None, color=None, elements=None, normal_params=None,
                    colorkey=None, finish=True):
        """Image element.
        <path>: the path to the image.
        <color>: if path is None, use this color instead of image.
        """
        super(Image, self).__init__("", elements, normal_params, finish=False)
        if path:
            painter = ImageFrame(path, mode=None, colorkey=colorkey)
        else:
            if color:
                painter = BasicFrame(style.SIZE, color)
            else:
                raise Exception("You must specify either a path or a color")
        self.set_painter(painter)
        if finish:
            self.finish()

    def set_alpha(self, alpha):
        img = self.get_image()
        img.set_alpha(alpha)
        self.set_image(img)

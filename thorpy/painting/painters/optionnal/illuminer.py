from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui import constants, functions, style
from thorpy.painting.graphics import illuminate_alphacolor_except


class IlluminerAlphaExcept(BasicFrame):
    """Illuminer that also set alpha values, in addition to colors.
    All pixels with RGB value <colorkey> will be taken into account for fading,
    while all other pixels will be considered as light source.
    """

    def __init__(self, size=None, colorkey=constants.WHITE, clip=None,
                 color_target=None, color_bulk=None, subrect=None,
                 pressed=False, hovered=False, factor=1., fadout=10., bulk_alpha=255):
        if size is None: size=style.SIZE
        if color_target is None: color_target=style.DEF_COLOR
        BasicFrame.__init__(self,
                            size=size,
                            color=colorkey,
                            clip=clip,
                            pressed=pressed,
                            hovered=hovered)
        self.color_target = color_target
        self.color_bulk = color_bulk
        self.subrect = subrect
        self.factor = factor
        self.fadout = fadout
        self.bulk_alpha = bulk_alpha


    def get_fusion(self, title, center_title):
        """Fusion the painter.img and the title.img and returns this fusion"""
        if center_title is True:  # center the title on the element rect
            title.center_on(self.size)
        elif center_title is not False:  # center_title is the topleft argument
            title._pos = center_title
        else:
            title._pos = (0, 0)
        painter_img = self.get_surface()
        title.blit_on(painter_img)
        functions.debug_msg("Building illuminer of size " + str(self.size))
        return illuminate_alphacolor_except(painter_img, self.color,
                                            self.color_target, self.color_bulk,
                                            self.subrect, self.factor,
                                            self.fadout, self.bulk_alpha)

class IlluminerAlphaText(IlluminerAlphaExcept):
    """Text-specialized Illuminer that also set alpha values, in addition to
    colors.
    All pixels with RGB value <colorkey> will be taken into account for fading,
    while all other pixels will be considered as light source.
    """

    def get_fusion(self, title, center_title):
        """Fusion the painter.img and the title.img and returns this fusion"""
        if title._writer.color == self.color:
            functions.debug_msg("Colorkey is the same as writer's color while\
                                 generating " + title._text)
        if center_title is True:  # center the title on the element rect
            title.center_on(self.size)
        elif center_title is not False:  # center_title is the topleft argument
            title._pos = center_title
        else:
            title._pos = (0, 0)
        painter_img = self.get_surface()
        old_aa = title._writer.aa
        old_imgs = title._imgs
        if old_aa:
            title._writer.aa = False
            title.refresh_imgs()
        title.blit_on(painter_img)
        if old_aa:
            title._writer.aa = True
            title._imgs = old_imgs
        functions.debug_msg("Building illuminer of size " + str(self.size))
        return illuminate_alphacolor_except(painter_img, self.color,
                                            self.color_target, self.color_bulk,
                                            self.subrect, self.factor,
                                            self.fadout, self.bulk_alpha)

from pygame import SRCALPHA, BLEND_RGBA_MAX, BLEND_RGBA_MIN, Rect, Color
from pygame import Surface, draw, transform

from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui import style


class RoundRect(BasicFrame):

    def __init__(self, size=None, color=None, clip=None,
                 radius=0.):
        """If radius is in the range [0, 1], self.radius_value is the fraction
        of radius * min(size), else it is interpreted as a raw pixel value.
        """
        BasicFrame.__init__(self, size, color, clip)
        self.radius_value = style.DEF_RADIUS if radius is None else radius
        if 0. <= radius <= 1.:
            self.radius_value = min(self.size) * radius

##    def draw(self):
##        from pygame import gfxdraw as gfx
##        surface = Surface(self.size, flags=SRCALPHA).convert_alpha()
##        surface.fill((0,0,0,0))
##        rect = surface.get_rect()
##        radius = int(self.radius * min(self.size))
##        intern_rect = rect.inflate((-2*radius, -2*radius))
##        gfx.filled_circle(surface, intern_rect.left, intern_rect.top, radius, self.color)
##        gfx.filled_circle(surface, intern_rect.right, intern_rect.top, radius, self.color)
##        gfx.filled_circle(surface, intern_rect.left, intern_rect.bottom, radius, self.color)
##        gfx.filled_circle(surface, intern_rect.right, intern_rect.bottom, radius, self.color)
####        draw.rect(surface, self.color, intern_rect)
##        draw.rect(surface, self.color, Rect(0, radius, radius, rect.h - 2*radius))
####        draw.rect(surface, self.color, intern_rect.inflate(2*radius, 0))
##        return surface

    def draw(self):
        surface = Surface(self.size, flags=SRCALPHA).convert_alpha()
        rect = Rect((0, 0), self.size)
        color = Color(*self.color)
        alpha = color.a
        color.a = 0
        rectangle = Surface(rect.size, SRCALPHA)
        #ex: [h*3, h*3]
        circle = Surface([min(rect.size) * 5] * 2, SRCALPHA)
        draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        #ex: [h*0.5, h*.05]
        circle = transform.smoothscale(circle,
                                       [int(self.radius_value)] * 2)
        #now circle is just a small circle of radius self.radius*h (for example)
        #blit topleft circle:
        radius = rectangle.blit(circle, (0, 0))
        #now radius = Rect((0, 0), circle.size), rect=Rect((0, 0), self.size)
        #blit bottomright circle:
        radius.bottomright = rect.bottomright #radius is growing
        rectangle.blit(circle, radius)
        #blit topright circle:
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        #blit bottomleft circle:
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)
        #black-fill of the internal rect
        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
        #fill with color using blend_rgba_max
        rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
        #fill with alpha-withe using blend_rgba_min in order to make transparent
        #the
        rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)
        surface.blit(rectangle, rect.topleft)
        return surface

"""Module for producing graphics using Python Imaging Library.
By convention, all the functions return PIL images, unless the name of the
function indicates that this is not the case.
"""

try:
    from PIL import Image, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import numpy
    import pygame.surfarray as surfarray
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from pygame.image import tostring, fromstring
from pygame import Surface, SRCALPHA

from thorpy._utils.colorscomputing import square_color_norm

MAX_NORM = 3*(255**2)

def pygame_surf_to_pil_img(surf, color_format="RGBA"):
    if not HAS_PIL:
        raise Exception("PIL was not found on this machine.")
    size = surf.get_size()
    pil_string_image = tostring(surf, color_format, False)
    return Image.frombytes(color_format, size, pil_string_image)

def pil_img_to_pygame_surf(img, color_format="RGBA"):
    if not HAS_PIL:
        raise Exception("PIL was not found on this machine.")
    size = img.size
    data = img.convert(color_format).tobytes("raw", color_format)
    return fromstring(data, size, color_format)

def get_black_white(surf, black=128, color_format="RGBA", convert=True):
    if not HAS_PIL:
        raise Exception("PIL was not found on this machine.")
    img = pygame_surf_to_pil_img(surf)
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x<black else 255, '1')
    if convert:
        bw = bw.convert(color_format)
    return bw

def get_blurred(surf, radius=2, color_format="RGBA"):
    if not HAS_PIL:
        raise Exception("PIL was not found on this machine.")
    img = pygame_surf_to_pil_img(surf, color_format)
    img = img.filter(ImageFilter.GaussianBlur(radius))
    return img

def get_shadow(surf, radius=2, black=255, color_format="RGBA", alpha_factor=255,
               decay_mode="exponential", color=(0,0,0)):
    if not HAS_PIL:
        raise Exception("PIL was not found on this machine. Cannot build shadow")
    img = get_black_white(surf, black, color_format)
    img = img.filter(ImageFilter.GaussianBlur(radius))
    img = pil_img_to_pygame_surf(img, color_format)
    img = set_alpha_from_intensity(img, alpha_factor, decay_mode, color)
    return img

def set_alpha_from_intensity(surface, alpha_factor, decay_mode, color):
    if not HAS_PIL:
        raise Exception("PIL was not found on this machine.")
    if not HAS_NUMPY:
        raise Exception("NumPy was not found on this machine.")
    rect = surface.get_rect()
    newsurf = Surface(rect.size, SRCALPHA, depth=surface.get_bitsize())
    newsurf = newsurf.convert_alpha()
    newsurf.blit(surface, (0, 0))
    arrayrgb = surfarray.pixels3d(newsurf)
    arraya = surfarray.pixels_alpha(newsurf)
    bulk_color = tuple(color)
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            color = tuple(arrayrgb[x][y])
            light = square_color_norm(color)
            alpha = float(light)/MAX_NORM * 255
            arrayrgb[x][y][0] = bulk_color[0]
            arrayrgb[x][y][1] = bulk_color[1]
            arrayrgb[x][y][2] = bulk_color[2]
            if decay_mode == "linear":
                actual_alpha = int(255 - alpha)
            elif decay_mode == "exponential":
                tuning_factor = 1.03
                actual_alpha = int(255*tuning_factor**-alpha)
##            elif decay_mode == "quadratic":
##                pass
            else:
                raise Exception("decay_mode not recognized: " + decay_mode)
            actual_alpha *= alpha_factor
            arraya[x][y] = actual_alpha
    return newsurf
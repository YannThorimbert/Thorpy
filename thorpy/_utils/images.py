# -*- coding: utf-8 -*-
"""Provides functions for handling images."""

import pygame

try:
    import numpy
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from thorpy import miscgui


def detect_frame(surf, vacuum=(255, 255, 255)):
    """Returns a Rect of the minimum size to contain all that is not <vacuum>"""
    if not HAS_NUMPY:
        miscgui.functions.debug_msg("Numpy was not found on this machine.\
            Cannot call detect_frame. Returns surface's size instead.")
        return surf.get_size()
    print("detecting frame...")
    vacuum = numpy.array(vacuum)
    array = pygame.surfarray.array3d(surf)
    x_found = False
    last_x = 0
    miny = float("inf") #previously : 1000000000
    maxy = 0
    len_x = len(array)
    len_y = len(array[0])
    for x in range(len_x):
        if x % 100 == 0:
            print("scanning pixel line " + str(x))
        for y in range(len_y):
            if (array[x][y] != vacuum).any():
                if not x_found:
                    x_found = True
                    first_x = x
                last_x = x
                if y < miny:
                    miny = y
                if y > maxy:
                    maxy = y
    return pygame.Rect(first_x, miny, last_x - first_x, maxy - miny)

def extract_frames(inGif, outFolder):
    """Needs PIL. No more than 100 frames"""
    from PIL import Image
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        snframe = str(nframes).zfill(6)
        if nframes < 10:
            snframe = "0" + str(nframes)
        frame.save(outFolder + snframe, 'GIF')
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break
    return True

def get_resized_image(image, dims, type_=min):
    """Fits whitout deformation <image> to <dims>. Return the scaled image.
    Note that if dims ratio is not the same as image ratio, the max/min side
    fits the specified dimensions, depending on the <type_> argument."""
    size = image.get_size()
    (fx, fy) = (float(dims[0]) / size[0], float(dims[1]) / size[1])
    f = type_(fx, fy)
    size_x = int(size[0] * f)
    size_y = int(size[1] * f)
    return pygame.transform.scale(image, (size_x, size_y))

def get_centered_image(img, dims, bckgr):
    s = pygame.Surface(dims)
    s.fill(bckgr)
    img_size = img.get_size()
    dx = (dims[0] - img_size[0])/2
    dy = (dims[1] - img_size[1])/2
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    s.blit(img, (dx, dy))
    return s

def get_colorkey(colorkey, surf):
    if colorkey is not None:
        if colorkey is "auto":
            colorkey = surf.get_at((0,0))
    return colorkey

##def load_image(filename, colorkey=None):
##    miscgui.functions.debug_msg("Loading " + filename)
##    image = pygame.image.load(filename).convert()
##    if colorkey:
##        image.set_colorkey(colorkey, pygame.RLEACCEL)
####    image.convert_alpha()
####    image.convert()
##    return image

def load_image(filename, colorkey=None, use_img_dict=None):
    use_img_dict=miscgui.application.USE_IMG_DICT if use_img_dict is None else use_img_dict
    loaded = miscgui.application._loaded.get(filename)
    if loaded and use_img_dict:
        miscgui.functions.debug_msg(filename + " found in loaded files.")
        return loaded
    else:
        miscgui.functions.debug_msg("Loading " + filename)
        image = pygame.image.load(filename).convert()
        if colorkey:
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        if miscgui.application.USE_IMG_DICT:
            miscgui.application._loaded[filename] = image
        return image

##def load_image(name, path="./", colorkey=None):
##    fullname = os.path.join(path, name)
##    loaded = miscgui.constants.loaded.get(fullname)
##    if loaded:
##        miscgui.functions.debug_msg(fullname + " found in loaded files.")
##        return loaded
##    else:
##        miscgui.functions.debug_msg("Loading " + fullname)
##        try:
##            image = pygame.image.load(fullname)
##        except:
##            dirpath = os.path.dirname(os.path.dirname(__file__))
##            path = dirpath + "/" + fullname
##            path=os.path.normpath(path)
##            return load_image(name=path, colorkey=colorkey)
##        image.convert()
##        miscgui.constants.loaded[fullname] = image
##        return image

def fusion_images(surf1, surf2, rel_pos=(0,0), colorkey=(255, 255, 255)):
    """Blit surf1 at <rel_pos> from surf1's topleft corner"""
    surface = pygame.Surface(surf1.get_rect().size)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surf1.get_at((0,0))
        surface.fill(colorkey)
        surface.set_colorkey(colorkey, pygame.RLEACCEL)
    surface.blit(surf1,(0,0))
    surface.blit(surf2,rel_pos)
    return surface.convert()

def fusion_images_fine(size, surf1, pos1, surf2, pos2, colorkey=(255, 255, 255)):
    surface = pygame.Surface(size)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surf1.get_at((0,0))
        surface.fill(colorkey)
        surface.set_colorkey(colorkey, pygame.RLEACCEL)
    surface.blit(surf1, pos1)
    surface.blit(surf2, pos2)
    return surface.convert()


def capture_screen(surface, rect=None):
    """Returns a copy of the surface <surface>, with restriction <rect>
        (None means the whole surface)"""
    if not rect:
        rect = surface.get_rect()
    return surface.copy().subsurface(rect).convert()

def change_color_on_img(img, color_source, color_target, colorkey=None):
    px = pygame.PixelArray(img.copy())
    px.replace(color_source, color_target)
    img2 = px.make_surface()
    if colorkey is not None:
        img2.set_colorkey(colorkey, pygame.RLEACCEL)
    return img2.convert()

def change_color_on_img_ip(img, color_source, color_target, colorkey=None):
    px = pygame.PixelArray(img)
    px.replace(color_source, color_target)
    img2 = px.make_surface()
    if colorkey is not None:
        img2.set_colorkey(colorkey, pygame.RLEACCEL)
    return img2.convert()
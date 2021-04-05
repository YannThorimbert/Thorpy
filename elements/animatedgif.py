#NB : the gif extractor was obtained from BigglesZX on https://gist.github.com/BigglesZX/4016539
import os
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

import pygame
from thorpy.elements.image import Image as ThorpyImage
from thorpy.painting.pilgraphics import pil_img_to_pygame_surf
import thorpy

'''
I searched high and low for solutions to the "extract animated GIF frames in Python"
problem, and after much trial and error came up with the following solution based
on several partial examples around the web (mostly Stack Overflow).
There are two pitfalls that aren't often mentioned when dealing with animated GIFs -
firstly that some files feature per-frame local palettes while some have one global
palette for all frames, and secondly that some GIFs replace the entire image with
each new frame ('full' mode in the code below), and some only update a specific
region ('partial').
This code deals with both those cases by examining the palette and redraw
instructions of each frame. In the latter case this requires a preliminary (usually
partial) iteration of the frames before processing, since the redraw mode needs to
be consistently applied across all frames. I found a couple of examples of
partial-mode GIFs containing the occasional full-frame redraw, which would result
in bad renders of those frames if the mode assessment was only done on a
single-frame basis.
Nov 2012
'''


def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def processImage(path):
    '''
    Iterate the GIF, extracting each frame.
    '''
    if not path.endswith(".gif") or path.endswith(".GIF"):
        return [thorpy.load_image(path)]
    mode = analyseImage(path)['mode']
    im = Image.open(path)
    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    images = []
    try:
        while True:
##            print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():

                im.putpalette(p)
            new_frame = Image.new('RGBA', im.size)
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(im, (0,0), im.convert('RGBA'))
##            new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')
            images.append(pil_img_to_pygame_surf(new_frame))
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return images



class AnimatedGif(ThorpyImage):
    @staticmethod
    def make(path=None, colorkey=None, low=2, nread=float("inf")):
        """Image element.
        <path>: the path to the image.
        <color>: if path is None, use this color instead of image.
        <low>: increase this parameter to lower the gif speed.
        <nread>: number of times the gif is played
        """
        img = AnimatedGif(path, colorkey=colorkey, low=low, nread=nread,
                            finish=False)
        img.finish()
        return img

    def __init__(self, path, elements=None, normal_params=None, colorkey=None,
                 start_frame=0, low=2, nread=float("inf"),finish=True):
        low = 1 if low < 1 else low
        if not HAS_PIL:
            print("You need to have PIL installed in order to use animated gifs")
        ThorpyImage.__init__(self, path=path, elements=elements,
                            normal_params=normal_params, colorkey=colorkey,
                            finish=False)
        self.colorkey = colorkey
        if isinstance(path,list):
            self.frames = frames
        else:
            self.frames = processImage(path)
        self.current_frame = start_frame
        self.low = low
        self.nread = nread
        self.i = 0
        thorpy.add_time_reaction(self, self.next_frame)
        for img in self.frames:
            img.set_colorkey(self.colorkey)
        if finish:
            self.finish()
        self.time_func = None

    def next_frame(self):
        if self.i%self.low == 0 and self.nread>0:
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.current_frame = 0
                self.nread -= 1
            self.set_image(self.frames[self.current_frame])
            self.unblit_and_reblit()
            if self.time_func:
                self.time_func()
        if self.nread <= 0:
            self.set_visible(False)
        self.i += 1

    def resize_frames(self, size):
        self.set_size(size)
        new_frames = []
        for img in self.frames:
            newone = pygame.transform.smoothscale(img, size)
            newone.set_colorkey(self.colorkey)
            new_frames.append(newone)
        self.frames = new_frames


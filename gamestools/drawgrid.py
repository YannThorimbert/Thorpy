import pygame

from thorpy.gamestools.grid import Grid
from thorpy.elements.element import Element
from thorpy.miscgui import style
from thorpy.painting.painters.basicframe import BasicFrame
from thorpy.miscgui.reaction import Reaction


class BasicGridPainter(BasicFrame):

    def __init__(self, size, color1, color2, nx, ny):
        BasicFrame.__init__(self, size=size, color=color1)
        self.color2 = color2
        self.color1 = color1
        self.nx = nx
        self.ny = ny
        self.frame = True
        self.xinternal = True
        self.yinternal = True

    def draw(self):
        surface = pygame.Surface(self.size).convert()
        surface.fill(self.color)
        w,h = self.size
        dx, dy = w/self.nx, h/self.ny
        if self.xinternal:
            for x in range(1,self.nx):
                xpix = x*dx-1
                pygame.draw.line(surface, self.color2, (xpix, 0), (xpix, h))
        if self.yinternal:
            for y in range(1,self.ny):
                ypix = y*dy
                pygame.draw.line(surface, self.color2, (0, ypix), (w, ypix))
        if self.frame:
            pygame.draw.rect(surface, self.color2, pygame.Rect(0,0,w,h), 1)
        return surface

class RealGridPainter(BasicFrame):

    def __init__(self, grid, color1, color2, frame=True, rects=True):
        if frame:
            grid.move((1,1))
            size = grid.frame.inflate((2,2)).size
        else:
            size = grid.frame.size
        BasicFrame.__init__(self, size=size, color=color1)
        self.color2 = color2
        self.color1 = color1
        self.grid = grid
        self.frame = frame
        self.rects = rects

    def draw(self):
        surface = pygame.Surface(self.size).convert()
        surface.fill(self.color)
        if self.rects:
            for rect in self.grid.iterrects():
                pygame.draw.rect(surface, self.color2, rect, 1)
        if self.frame:
            pygame.draw.rect(surface, self.color2, self.grid.frame.inflate((2,2)), 1)
        return surface


class DrawGrid(Element):

    @staticmethod
    def make(nx, ny, cell_size):
        dg = DrawGrid(nx, ny, cell_size)
        dg.finish()
        return dg

    def __init__(self, nx, ny, cell_size):
        Element.__init__(self)
        self.grid = Grid(nx, ny, cell_size)
        self.margins = style.MARGINS
        self.current_coord = None
        self.current_rect = None
        reac_mousemotion = Reaction(pygame.MOUSEMOTION, self.func_mousemotion)
        self.add_reaction(reac_mousemotion)

    def finish(self):
##        painter = BasicGridPainter(size, style.DEF_COLOR, style.DEF_DARK,
##                                    self.grid.nx, self.grid.ny)
        painter = RealGridPainter(self.grid, style.DEF_COLOR, style.DEF_DARK)
        self.set_painter(painter)
        Element.finish(self)

    def draw_values(self, value):
        for x in range(self.grid.nx):
            for y in range(self.grid.ny):
                if self.grid[x,y] == value:
                    print((x,y))

    def get_rect_at_coord(self, coord):
        rect = self.grid.get_rect_at_coord(coord).inflate((-2,-2))
        return rect

    def func_mousemotion(self, event):
        coord = self.grid.get_coord_at_pix(event.pos)
        if coord != self.current_coord:
            if self.grid.is_inside(coord):
##                print(coord)
                if self.current_coord:
                    self.partial_blit(None, self.current_rect)
                pygame.display.update(self.current_rect)
                self.current_coord = coord
                self.current_rect = self.get_rect_at_coord(self.current_coord)
                pygame.draw.rect(self.surface, style.DEF_DARK, self.current_rect)
                pygame.display.update(self.current_rect)

    def move(self, shift):
        Element.move(self, shift)
        self.grid.move(shift)


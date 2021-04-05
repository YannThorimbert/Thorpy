import pygame

from thorpy.gamestools.basegrid import BaseGrid

NA = [(1, 0), (-1, 0), (0, 1), (0, -1)]
NB = [(1, 1), (1, -1), (-1, 1), (-1, -1)] + NA


class Grid(BaseGrid):

    def __init__(self, nx, ny, cell_size, topleft=(0,0), value=None,
                 periodicity=(False, False)):
        BaseGrid.__init__(self, nx, ny, value, periodicity)
        self.cell_w = cell_size[0]
        self.cell_h = cell_size[1]
        self.frame = pygame.Rect(topleft,
                                 (self.nx*self.cell_w, self.ny*self.cell_h))
        self.cell_rect = self.build_cell_rect()

    def __len__(self):
        return self.nx*self.ny

    def copy(self):
        copied = BaseGrid.copy(self)
        copied.cell_w = self.cell_w
        copied.cell_h = self.cell_h
        copied.frame = self.frame.copy()
        copied.cell_rect = self.cell_rect.copy()
        return copied

    def build_cell_rect(self):
        topleft = (self.frame.left, self.frame.bottom - self.cell_h)
        return pygame.Rect(topleft, (self.cell_w, self.cell_h))

    def move(self, shift):
        self.frame.move_ip(shift)
        self.cell_rect = self.build_cell_rect()

    def set_topleft(self, pos):
        self.frame.topleft = pos
        self.cell_rect = self.build_cell_rect()

    def set_bottomleft(self, pos):
        self.frame.bottomleft = pos
        self.cell_rect = self.build_cell_rect()

    def set_center(self, pos):
        self.frame.center = pos
        self.cell_rect = self.build_cell_rect()

    def center_on(self, pos):
        if isinstance(pos, pygame.Rect):
            pos = pos.center
        self.set_center(pos)

    def iterrects(self):
        for coord in self:
            yield self.get_rect_at_coord(coord)

    def get_rect_at_coord(self, coord):
        shift_x = coord[0] * self.cell_w
        shift_y = coord[1] * self.cell_h
        return self.cell_rect.move((shift_x, -shift_y))

    def get_coord_at_pix(self, pix):
        x = pix[0] - self.frame.left
        y = self.frame.bottom - pix[1]
        cx = int(x * self.nx / self.frame.width)
        cy = int(y * self.ny / self.frame.height)
        return (cx, cy)

    def get_rect_at_pix(self, pix):
        return self.get_rect_at_coord(self.get_coord_at_pix(pix))

##    def blit_cell_on(self, surface, color, coord, thick=1):
##        r = self.get_rect_at_coord(coord)
##        pygame.draw.rect(surface, color, r, thick)
##
##    def blit_on(self, surface, cell_color=(0, 0, 0), frame_color=(0,0,0)):
##        for coord in self:
##            self.blit_cell_on(surface, color, coord)
##        pygame.draw.rect(surface, frame_color, self.frame, 1)

class PygameGrid(Grid):

    def build_cell_rect(self):
        return pygame.Rect(self.frame.topleft, (self.cell_w, self.cell_h))

    def get_rect_at_coord(self, coord):
        shift_x = coord[0] * self.cell_w
        shift_y = coord[1] * self.cell_h
        return self.cell_rect.move((shift_x, shift_y))

    def get_coord_at_pix(self, pix):
        x = pix[0] - self.frame.left
        y = pix[1] - self.frame.bottom
        cx = int(x * self.nx / self.frame.width)
        cy = int(y * self.ny / self.frame.height)
        return (cx, cy)

    def get_rect_at_pix(self, pix):
        return self.get_rect_at_coord(self.get_coord_at_pix(pix))
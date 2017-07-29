import math
from thorpy import load_image
from thorpy.miscgui import style


class HeartLife:

    def __init__(self, full=style.HEART_FULL, empty=style.HEART_EMPTY, n=5,
                    spacing=5, x0=5, y0=5):
        self.full = load_image(full,(255,255,255))
        self.empty = load_image(empty,(255,255,255))
        self.n = n
        self.heart_size = self.full.get_size()
        self.heart_spacing = self.heart_size[0] + spacing
        self.xlife = - self.heart_spacing + x0
        self.ylife = y0

    def blit(self, surf, life):
        x = 0
        nfull = math.ceil(life*self.n)
        for i in range(nfull):
            x += self.heart_spacing
            surf.blit(self.full,(self.xlife+x,self.ylife))
        for i in range(self.n-nfull):
            x += self.heart_spacing
            surf.blit(self.empty,(self.xlife+x,self.ylife))

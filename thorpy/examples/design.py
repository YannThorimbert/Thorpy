import thorpy, pygame

application = thorpy.Application((300, 300))

class MyPainter(thorpy.painters.painter.Painter):

    def __init__(self,c1, c2, c3, size=None, clip=None, pressed=False,
                    hovered=False,):
        super(MyPainter, self).__init__(size, clip, pressed, hovered)
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

    def get_surface(self):
        #transparent surface so that all that is not drawn is invisible
        surface = pygame.Surface(self.size, flags=pygame.SRCALPHA).convert_alpha()
        rect_corner = pygame.Rect(0, 0, self.size[0]//6, self.size[1]//6)
        rect_body = surface.get_rect().inflate((-5,-5))
        color_corner = self.c1 #this color will change accordin to the state
        if self.pressed:
            color_corner = self.c3
        #draw the four corners:
        if not self.hovered:
            for pos in [rect_body.topleft, rect_body.bottomleft,
                        rect_body.topright, rect_body.bottomright]:
                rect_corner.center = pos
                pygame.draw.rect(surface, color_corner, rect_corner)
        pygame.draw.rect(surface, self.c2, rect_body) #draw body
        #draw body border:
        pygame.draw.rect(surface, self.c3, rect_body.inflate((-5,-5)))
        #redraw corner rects if hovered
        if self.hovered:
            for pos in [rect_body.topleft, rect_body.bottomleft,
                    rect_body.topright, rect_body.bottomright]:
                rect_corner.center = pos
                pygame.draw.rect(surface, color_corner, rect_corner)
        surface.set_clip(self.clip) #don't forget to set clip
        return surface

my_painter = MyPainter((255,0,0), (0,255,0), (200,200,255))
my_button = thorpy.Clickable("My Button") #don't use 'make' !
my_button.set_painter(my_painter)
my_button.finish() #don't forget to call 'finish()
my_button.center()

background = thorpy.Background.make((255,255,255), elements=[my_button])
background.finish()

menu = thorpy.Menu(background)
menu.play()

application.quit()
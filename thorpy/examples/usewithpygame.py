#Tutorial : how to use ThorPy with a pre-existing code - step 1
import pygame, thorpy
pygame.init()
pygame.key.set_repeat(300, 30)
screen = pygame.display.set_mode((400,400))
screen.fill((255,255,255))
rect = pygame.Rect((0, 0, 50, 50))
rect.center = screen.get_rect().center
rect.y += 100
clock = pygame.time.Clock()

pygame.draw.rect(screen, (255,0,0), rect)
pygame.display.flip()

#declaration of some ThorPy elements ...
slider = thorpy.SliderX(100, (12, 35), "My Slider")
button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
text = thorpy.make_text("Left arrow to move the red square")
box = thorpy.Box(elements=[slider,button, text])
#we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu(box)
#important : set the screen as surface for all elements
for element in menu.get_population():
    element.surface = screen
#use the elements normally...
box.set_topleft((100,100))
box.blit()
box.update()

playing_game = True
while playing_game:
    clock.tick(45)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pygame.draw.rect(screen, (255,255,255), rect) #delete old
                pygame.display.update(rect)
                rect.move_ip((-5,0))
                pygame.draw.rect(screen, (255,0,0), rect) #drat new
                pygame.display.update(rect)
        menu.react(event) #the menu automatically integrate your elements

pygame.quit()
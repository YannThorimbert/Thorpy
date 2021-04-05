import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

def refresh():
    pos = pygame.mouse.get_pos()
    e_ship.set_center(pos) #ship follows mouse
    # process smoke
    smokegen1.kill_old_elements()
    smokegen2.kill_old_elements()
    pressed = pygame.mouse.get_pressed()
    if pressed[0]: #left mouse button
        smokegen1.generate(V2(pos))
    elif pressed[2]: #left mouse button
        smokegen2.generate(V2(pos))
    smokegen1.update_physics(V2(0))
    smokegen2.update_physics(V2(0))
    # process debris
    debrisgen.kill_old_elements(screen.get_rect())
    debrisgen.update_physics(dt=0.1)
    # refresh screen
    e_background.blit()
    debrisgen.draw(thorpy.get_screen())
    smokegen1.draw(screen)
    smokegen2.draw(screen)
    pygame.display.flip()


def make_debris():
    angle = random.randint(0,360) #pick random angle
    spread = 15 #spread of debris directions
    debrisgen.generate( V2(pygame.mouse.get_pos()), #position
                        n=20, #number of debris
                        v_range=(10,50), #translational velocity range
                        omega_range=(5,25), #rotational velocity range
                        angle_range=(angle-spread,angle+spread))

# ##############################################################################

app = thorpy.Application((400,400), "Effects")

smokegen1 = thorpy.fx.get_smokegen(n=50, color=(200,200,255), grow=0.6)
smokegen2 = thorpy.fx.get_fire_smokegen(n=50, color=(200,255,155), grow=0.4)
debrisgen = thorpy.fx.get_debris_generator(duration=200, #nb. frames before die
                                    color=(100,100,100),
                                    max_size=10)

e_ship = thorpy.Image("../documentation/examples/boat_example.png",
                        colorkey=(255,255,255))
if thorpy.constants.CAN_SHADOWS: #set shadow
    thorpy.makeup.add_static_shadow(e_ship, {"target_altitude":5,
                                            "shadow_radius":3,
                                            "sun_angle":40,
                                            "alpha_factor":0.6})

e_background = thorpy.Background(image=thorpy.style.EXAMPLE_IMG,
                                        elements=[e_ship])

reac_time = thorpy.ConstantReaction(thorpy.constants.THORPY_EVENT, refresh,
                                    {"id":thorpy.constants.EVENT_TIME})
reac_space = thorpy.ConstantReaction(pygame.KEYDOWN, make_debris,
                                    {"key":pygame.K_SPACE})
e_background.add_reactions([reac_time, reac_space])

screen = thorpy.get_screen()
infotext = "Press SPACE to spawn debris\n"+\
            "LMB and RMB to spawn smokes\n"+\
            "and move the mouse to move the boat."
thorpy.launch_blocking_alert("Commands", infotext)
menu = thorpy.Menu(e_background)
pygame.key.set_repeat(30,30)
menu.play()
app.quit()
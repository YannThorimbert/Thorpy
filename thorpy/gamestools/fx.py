import pygame, random, thorpy
from pygame.math import Vector2 as V2


class SmokeGenerator(object):
    current_id = 0

    def __init__(self, samples, n, opac=None, mov=1, grow=0.5, prob=0.2, i=2,
                    color=None, alpha0=255, size0=None, smoothscale=False,
                    copy=False):
        if not copy:
            samples = [s.copy() for s in samples]
        self.samples = samples
        self.n = n
        opac = alpha0/n if opac is None else opac
        self.opac = opac
        self.mov = mov
        self.grow = grow
        self.prob = prob
        self.alpha0 = alpha0
        if not copy:
            if smoothscale:
                self.scale_func = pygame.transform.smoothscale
            else:
                self.scale_func = pygame.transform.scale
            if isinstance(size0, tuple):
                self.size0 = {s:size0 for s in self.samples}
            elif size0 is None:
                self.size0 = {s:s.get_size() for s in self.samples}
            else:
                self.size0 = size0
            if color is not None:#for the moment colorkey is hardcoded to white, and color source to black
                color=(254,254,254) if color == (255,255,255) else color
                for s in self.samples:
                    thorpy.change_color_on_img_ip(  img=s,
                                                    color_source=(0,0,0),
                                                    color_target=color,
                                                    colorkey=(255,255,255))
            self.imgs = self.build_imgs() #on the form img[sample][time]
        self.i = i
        self.smokes = []
        self.body = None
        self.id = SmokeGenerator.current_id
        SmokeGenerator.current_id += 1

    def get_copy(self):
        gen = SmokeGenerator(samples=self.samples, n=self.n, mov=self.mov,
                                prob=self.prob, i=self.i, copy=True)
        gen.imgs = self.imgs
        return gen

    def build_imgs(self):
        imgs = {}
        for s in self.samples:
            imgs[s] = []
            w,h = self.size0[s]
            alpha = self.alpha0
            for i in range(self.n):
                w += self.grow
                h += self.grow
                alpha -= self.opac
                img = self.scale_func(s, (int(w), int(h)))
                img.set_colorkey((255,255,255))
                img.set_alpha(int(alpha))
                imgs[s].append(img)
        return imgs

    def generate(self, q):
        self.smokes.append(Smoke(V2(q), self))

    def kill_old_elements(self):
##        for s in self.smokes:
##            parent.partial_blit(None, s.rect)
        if len(self.smokes) > self.n:
            self.smokes = self.smokes[1::]

    def translate_old_elements(self, delta):
        for s in self.smokes:
            s.update_pos_only(delta)

##    def draw(self, surface):
##        for s in self.smokes:
##            if not s.dead:
##                surface.blit(s.img, s.rect.topleft)

    def draw(self, surface):
        blits = [(s.img, s.rect.topleft) for s in self.smokes if not s.dead]
        surface.blits(blits)

##        for s in self.smokes:
##            if not s.dead:
##                surface.blit(s.img, s.rect.topleft)

##    def draw(self, surface, parent):
##        if len(self.smokes) > self.n:
##            self.smokes = self.smokes[1::]
##        for s in self.smokes:
##            parent.partial_blit(None, s.rect)
##        for s in self.smokes:
##            if not s.dead:
##                surface.blit(s.img, s.rect.topleft)

    def update_physics(self, dq):
        for s in self.smokes:
            s.update_physics(dq)

    def add_to(self, body, position):
##        body.fight.smokes.append((self, body, position))
##        print("adding", self, body)
        self.body = body
        body.fight.smokes.insert(0, (self, body, position))


class Smoke(object):

    def __init__(self, q, generator):
        self.q = q
        self.t = 0
        self.s = random.choice(generator.samples)
        self.generator = generator
        self.img = self.generator.imgs[self.s][0]
        self.rect = self.img.get_rect()
        self.rect.center = self.q
        self.dead = False

    def update_pos_only(self, dq):
        self.q += dq
        self.rect = self.img.get_rect()
        self.rect.center = self.q

    def update_physics(self, dq):
        if self.t < self.generator.n:
            self.img = self.generator.imgs[self.s][self.t]
            if random.random() < self.generator.prob:
                dx = random.randint(-self.generator.mov,self.generator.mov)
                dy = random.randint(-self.generator.mov,self.generator.mov)
                self.q += (dx, dy)
            self.q += dq
            self.rect = self.img.get_rect()
            self.rect.center = self.q
            self.t += 1
        else:
            self.dead = True


class FireSmokeGenerator(SmokeGenerator):

    def __init__(self, samples, n, opac=None, mov=1, grow=0.5, prob=0.2, i=2,
                    color=None, alpha0=255, size0=None, smoothscale=False,
                    copy=False, black_increase_factor=1.):
        self.black_increase = black_increase_factor / n
        if not copy:
            samples = [s.copy() for s in samples]
        self.samples = samples
        self.n = n
        opac = alpha0/n if opac is None else opac
        self.opac = opac
        self.mov = mov
        self.grow = grow
        self.prob = prob
        self.alpha0 = alpha0
        if not copy:
            if smoothscale:
                self.scale_func = pygame.transform.smoothscale
            else:
                self.scale_func = pygame.transform.scale
            if isinstance(size0, tuple):
                self.size0 = {s:size0 for s in self.samples}
            elif size0 is None:
                self.size0 = {s:s.get_size() for s in self.samples}
            else:
                self.size0 = size0
            self.imgs = self.build_imgs() #on the form img[sample][time]
        self.i = i
        self.smokes = []
        self.body = None


    def build_imgs(self):
        from thorpy._utils.colorscomputing import linear_combination
        color1 = (255,255,0)
        color2 = (255,150,0)
        imgs = {}
        for s in self.samples:
            imgs[s]=[]
            for ic, c in enumerate([color1, color2]):
                imgs[s].append([])
                w,h = self.size0[s]
                alpha = self.alpha0
                k = 0.
                for i in range(self.n):
##                    k += 0.01
##                    k = (i-10)*1.1/self.n
                    k += self.black_increase
                    if k > 1.: k=1.
                    elif k < 0: k=0.
                    color_i = linear_combination((0,0,0), c, k)
                    local_s = s.copy()
                    thorpy.change_color_on_img_ip(  img=local_s,
                                                    color_source=(0,0,0),
                                                    color_target=color_i,
                                                    colorkey=(255,255,255))
                    w += self.grow
                    h += self.grow
                    alpha -= self.opac
                    img = self.scale_func(local_s, (int(w), int(h)))
                    img.set_colorkey((255,255,255))
                    img.set_alpha(int(alpha))
                    imgs[s][ic].append(img)
        return imgs

    def get_copy(self):
        gen = FireSmokeGenerator(samples=self.samples, n=self.n, mov=self.mov,
                                prob=self.prob, i=self.i, copy=True)
        gen.imgs = self.imgs
        return gen

    def generate(self, q):
        self.smokes.append(FireSmoke(V2(q), self))

class FireSmoke(Smoke):

    def __init__(self, q, generator):
        self.q = q
        self.t = 0
        self.s = random.choice(generator.samples)
        self.c = random.randint(0,1)
        self.generator = generator
        self.img = self.generator.imgs[self.s][self.c][0]
        self.rect = self.img.get_rect()
        self.rect.center = self.q
        self.dead = False

    def update_physics(self, dq):
        if self.t < self.generator.n:
            self.img = self.generator.imgs[self.s][self.c][self.t]
            if random.random() < self.generator.prob:
                dx = random.randint(-self.generator.mov,self.generator.mov)
                dy = random.randint(-self.generator.mov,self.generator.mov)
                self.q += (dx, dy)
            self.q += dq
            self.rect = self.img.get_rect()
            self.rect.center = self.q
            self.t += 1
        else:
            self.dead = True


class DebrisGenerator(object):
    def __init__(self, samples, color=None, size0=None, max_i=300, copy=False,
                    imgmanagers=None):
        self.max_i = max_i
        self.color = color
        if copy:
            self.samples = samples
            self.imgmanagers = imgmanagers
        else:
            samples = [s.copy() for s in samples]
            self.samples = samples
            if isinstance(size0, tuple):
                self.size0 = {s:size0 for s in self.samples}
            elif size0 is None:
                self.size0 = {s:s.get_size() for s in self.samples}
            else:
                self.size0 = size0
##            if color is not None:#for the moment colorkey is hardcoded to white, and color source to black
##                color=(254,254,254) if color == (255,255,255) else color
##                for s in self.samples:
##                    thorpy.change_color_on_img_ip(  img=s,
##                                                    color_source=(0,0,0),
##                                                    color_target=color,
##                                                    colorkey=(255,255,255))
            self.imgmanagers = {s:ImgManager(s) for s in self.samples}
        self.debris = []

    def generate(self, q, n, v_range, omega_range, angle_range):
        angle_range = (angle_range[0]*100, angle_range[1]*100)
        v_range = (v_range[0]*100, v_range[1]*100)
        for i in range(n):
            angle = random.randint(angle_range[0],angle_range[1])/100.
            velocity = random.randint(v_range[0],v_range[1])/100.
            omega = random.randint(omega_range[0],omega_range[1])
            v = V2(0,velocity).rotate(angle)
##            print("     ==>", self.color, q)
            self.debris.append(Debris(V2(q), v, omega, self))

    def kill_old_elements(self, domain):
        to_remove = []
        for d in self.debris:
            if d.i > self.max_i or not(d.rect.colliderect(domain)):
                to_remove.append(d)
##            parent.partial_blit(None, d.rect)
        for d in to_remove:
            self.debris.remove(d)

##    def draw(self, surface):
##        for d in self.debris:
##            surface.blit(d.img, d.rect.topleft)

    def draw(self, surface):
        blits = [(d.img, d.rect.topleft) for d in self.debris]
        surface.blits(blits)

    def update_physics(self,dt):
        for d in self.debris:
            d.update_physics(dt)

    def add_to(self, vessel):
        vessel.fight.debris.append((self, vessel))

    def get_copy(self):
        gen = DebrisGenerator(samples=self.samples, imgmanagers=self.imgmanagers,
                                max_i=self.max_i, copy=True)
        gen.color = self.color
        return gen

class Debris(object):

    def __init__(self, q, v, omega, generator):
        self.q = q
        self.v = v #constant
        self.angle = random.randint(-360,359)
        self.omega = omega
        self.s = random.choice(generator.samples)
        self.generator = generator
        self.img = self.generator.imgmanagers[self.s].imgs[int(self.angle)]
        self.rect = self.img.get_rect()
        self.rect.center = self.q
        self.i = 0

    def update_physics(self,dt):
        self.angle = (self.angle+self.omega*dt)%360
        self.q += self.v*dt
        self.img = self.generator.imgmanagers[self.s].imgs[int(self.angle)]
        self.rect = self.img.get_rect()
        self.rect.center = self.q
        self.i += 1

class ImgManager(object):

    def __init__(self, img):
        self.img = img
        self.imgs = self.build_imgs()

    def build_imgs(self):
        imgs = {}
        for angle in range(-360, 360):
            img = pygame.transform.rotate(self.img, angle).convert()
            img.set_colorkey((255,255,255))
            imgs[angle] = img
        return imgs

def get_debris_generator(duration, color, max_size, black_border=True):
    samples = []
    for w in range(1,max_size):
        for h in range(1,max_size):
            s = pygame.Surface(((w+1)*1.5,)*2).convert()
            s.fill((255,255,255))
            r = pygame.Rect(0,0,w,h)
            r.center = s.get_rect().center
            pygame.draw.rect(s, color, r)
            if black_border:
                pygame.draw.rect(s, (0,0,0), r, 1)
            samples.append(s)
    return DebrisGenerator(samples, color, max_i=duration)


def get_smokegen(n=15, color=(99,99,99), grow=0.4, i=2, prob=0.3, alpha0=255,
                    size0=None, images=None):
    if images is None:
        images = [thorpy.load_image(thorpy.style.SMOKE_IMG, (255,255,255))]
    return SmokeGenerator(images,
                                 n=n,
                                 prob=prob,
                                 grow=grow,
                                 i=i,
                                 color=color,
                                 alpha0=alpha0,
                                 size0=size0)


def get_fire_smokegen(n=50, color=(255,200,0), grow=0.4, i=2, prob=0.3, alpha0=255,
                    size0=None, images=None, black_increase_factor=1.):
    if images is None:
        images = [thorpy.load_image(thorpy.style.SMOKE_IMG, (255,255,255))]
    return FireSmokeGenerator(images,
                                 n=n,
                                 prob=prob,
                                 grow=grow,
                                 i=i,
                                 color=color,
                                 alpha0=alpha0,
                                 size0=size0,
                                 black_increase_factor=black_increase_factor)
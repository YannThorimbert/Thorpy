import pygame
#Usage example:
##c = SoundCollection()
##c.add("ok.wav", "ok")
##c.ok.play() #or wathever the pygame Sound class allows

class FakeSound(object):

    def play(self):
        pass


class SoundCollection:

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

    def add(self,filename,name):
        pygame.mixer.init()
        try:
            sound = pygame.mixer.Sound(filename)
            sound.play()
            pygame.mixer.stop()
            print("Loaded", filename, name)
        except:
            sound = FakeSound()
            print("Couldn't load", filename, name)
        setattr(self, name, sound)


def play_music(name, n=0):
    try:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(n)
    except:
        pass

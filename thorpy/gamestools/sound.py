import pygame
#Usage example:
##c = SoundCollection()
##c.add("ok.wav", "ok")
##c.ok.play() #or wathever the pygame Sound class allows

class FakeSound(object):

    def play(self, loop=0):
        pass

    def play_next_channel(self):
        pass

    def stop(self):
        pass

class Sound(pygame.mixer.Sound):

    def __init__(self, filename, manager):
        filename = filename.replace("\\","/")
        pygame.mixer.Sound.__init__(self, filename)
        self.manager = manager

    def play_next_channel(self):
        self.play()
##        self.manager.current_channel_number += 1
##        self.manager.current_channel_number %= pygame.mixer.get_num_channels()
##        c = self.manager.current_channel_number
##        if not c in self.manager.reserved_channels:
##            self.manager.current_channel = pygame.mixer.Channel(c)
##            self.manager.current_channel.play(self)

class SoundCollection:

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
##        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init(frequency=22050, size=-16, buffer=512)
        self.current_channel_number = 0
        self.current_channel = pygame.mixer.Channel(self.current_channel_number)
        self.reserved_channels = set()

    def reserve_current_channel(self):
        self.reserved_channels.add(self.current_channel_number)

    def add(self, filename, name=None):
        pygame.mixer.init()
        fake = False
        try:
            sound = Sound(filename, manager=self)
            sound.play()
            pygame.mixer.stop()
            print("Loaded", filename, name)
        except FileNotFoundError:
            sound = FakeSound()
            fake = True
            print("Couldn't load", filename, name)
        if name:
            setattr(self, name, sound)
        return sound, fake


def play_music(name, n=0):
    try:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(n)
    except:
        pass

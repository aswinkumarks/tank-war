import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.mute = False

    def mute_toggle(self):
        self.mute = not self.mute
        if self.mute:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def vol_mute_max(self, x):
        if self.mute:
            x.set_volume(0.0)
        else:
            x.set_volume(1.0)

    def fire_sound(self):
        x = pygame.mixer.Sound("sounds/boom1.wav")
        self.vol_mute_max(x)
        x.play()

    def crash_sound(self):
        x = pygame.mixer.Sound("sounds/explosion.wav")
        self.vol_mute_max(x)
        x.play()
            
    def damage_sound(self):
        # pygame.mixer.Sound("sounds/damage.mp3").play()
        pygame.mixer.music.load("sounds/damage.mp3")
        pygame.mixer.music.play()
    
    def menu_music(self):
        # pygame.mixer.Sound("sounds/menu.mp3").play()
        pygame.mixer.music.load("sounds/menu.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

game_sound = Sound()
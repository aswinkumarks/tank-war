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
            
    def fire_sound(self):
        pygame.mixer.Sound("sounds/boom1.wav").play()

    def crash_sound(self):
        pygame.mixer.Sound("sounds/explosion.wav").play()
            
    def damage_sound(self):
        # pygame.mixer.Sound("sounds/damage.mp3").play()
        pygame.mixer.music.load("sounds/damage.mp3")
        pygame.mixer.music.play()
    
    def menu_music(self):
        # pygame.mixer.Sound("sounds/menu.mp3").play()
        pygame.mixer.music.load("sounds/menu.mp3")
        pygame.mixer.music.play()
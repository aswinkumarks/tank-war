import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
    
    def fire_sound(self):
        pygame.mixer.Sound("sounds/fire.wav").play()
    
    def crash_sound(self):
        pygame.mixer.Sound("sounds/crash.ogg").play()
    
    def damage_sound(self):
        # pygame.mixer.Sound("sounds/damage.mp3").play()
        pygame.mixer.music.load("sounds/damage.mp3")
        pygame.mixer.music.play()
    
    def menu_music(self):
        # pygame.mixer.Sound("sounds/menu.mp3").play()
        pygame.mixer.music.load("sounds/menu.mp3")
        pygame.mixer.music.play()
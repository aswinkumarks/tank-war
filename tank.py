import pygame
class Tank:
    def __init__(self):
        sprites = pygame.image.load("Sprites/tank-sprite.png")
        self.tank_image = sprites.subsurface(11,7,40,54)
        self.tank_rect = self.tank_image.get_rect()
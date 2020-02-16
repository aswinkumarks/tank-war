import pygame
class Tank:
    def __init__(self):
        self.sprites = pygame.image.load("Sprites/tank-blue.png")
        self.tank_image = self.sprites.subsurface(11,7,40,54)
        self.tank_rect = self.tank_image.get_rect()
        self.direction = 'DOWN'

    def change_direction(self,new_direction):
        if new_direction == 'UP':
            self.tank_image = self.sprites.subsurface(140,192,40,62)
        elif new_direction == 'DOWN':
            self.tank_image = self.sprites.subsurface(11,7,40,54)
        elif new_direction == 'RIGHT':
            self.tank_image = self.sprites.subsurface(131,141,61,45)
        elif new_direction == 'LEFT':
            self.tank_image = self.sprites.subsurface(128,77,63,45)

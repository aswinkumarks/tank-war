import pygame
from game import Sound 

class Tank:
    def __init__(self):
        self.bullet = Bullet()
        self.sprites = pygame.image.load("Sprites/tank-blue.png")
        self.image = self.sprites.subsurface(11,7,40,54)
        self.rect = self.image.get_rect()
        self.direction = 'DOWN'

    def change_direction(self,new_direction):
        if new_direction == 'UP':
            self.image = self.sprites.subsurface(140,192,40,62)
        elif new_direction == 'DOWN':
            self.image = self.sprites.subsurface(11,7,40,54)
        elif new_direction == 'RIGHT':
            self.image = self.sprites.subsurface(131,141,61,45)
        elif new_direction == 'LEFT':
            self.image = self.sprites.subsurface(128,77,63,45)


class Bullet:
    def __init__(self):
        self.sprites = pygame.image.load("Sprites/bullets.png")
        self.image = self.sprites.subsurface(14,92,10,17)
        self.rect = self.image.get_rect()
        self.direction = 'DOWN'
        self.travel = False
        self.fire = False
    
    def fire_bullet(self, tank_direction):
        self.fire = False
        self.direction = tank_direction
        if self.travel:
            self.rect = self.rect.move([0,5])
        else:
            Sound.fire_sound(self)
            self.travel = True

        # print(self.tank.rect)
        if self.rect[0] > 640 or self.rect[1] > 480:
            self.travel = False

    # def change_bullet_powerlevel(self,plevel):
    #     if plevel == 0:
    #         self.image = self.sprites.subsurface(14,92,10,17)
    #     elif plevel == 1:
    #         self.image = self.sprites.subsurface(35,92,10,17)
    #     elif plevel == 2:
    #         self.image = self.sprites.subsurface(56,91,10,17)

    # def change_direction(self, new_direction):
    #     if new_direction == 'UP':
    #         self.image = pygame.transform.rotate(self.bullet_img, 180)
    #     elif new_direction == 'DOWN':
    #         self.image = pygame.transform.rotate(self.bullet_img, 0)
    #     elif new_direction == 'RIGHT':
    #         self.image = pygame.transform.rotate(self.bullet_img, 270)
    #     elif new_direction == 'LEFT':
    #         self.image = pygame.transform.rotate(self.bullet_img, 90)
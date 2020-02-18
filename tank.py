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


class Bullet:
    def __init__(self):
        self.sprites = pygame.image.load("Sprites/bullet.png")
        self.bullet_img = self.sprites.subsurface(14,92,10,17)
        self.bullet_rect = self.bullet_img.get_rect()
        # self.direction = 'DOWN'

    # def change_bullet_powerlevel(self,plevel):
    #     if plevel == 0:
    #         self.tank_image = self.sprites.subsurface(14,92,10,17)
    #     elif plevel == 1:
    #         self.tank_image = self.sprites.subsurface(35,92,10,17)
    #     elif plevel == 2:
    #         self.tank_image = self.sprites.subsurface(56,91,10,17)

    # def change_direction(self, new_direction):
    #     if new_direction == 'UP':
    #         self.tank_image = pygame.transform.rotate(self.bullet_img, 180)
    #     elif new_direction == 'DOWN':
    #         self.tank_image = pygame.transform.rotate(self.bullet_img, 0)
    #     elif new_direction == 'RIGHT':
    #         self.tank_image = pygame.transform.rotate(self.bullet_img, 270)
    #     elif new_direction == 'LEFT':
    #         self.tank_image = pygame.transform.rotate(self.bullet_img, 90)
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
        self.org_image = self.sprites.subsurface(14,92,10,17)
        self.rect = self.image.get_rect()
        self.direction = 'DOWN'
        self.speed = 10
        self.travel = False
        self.fire = False
        self.move_vec = {'UP':[0,-self.speed],'DOWN':[0,self.speed],'RIGHT':[self.speed,0],'LEFT':[-self.speed,0]}
    
    def fire_bullet(self):
        self.fire = False
        # print(self.direction,self.rect)
        if self.travel:
            self.rect = self.rect.move(self.move_vec[self.direction])

        else:           
            if self.direction == 'DOWN' or self.direction == 'UP':
                self.rect = self.rect.move([15,40])
                
            elif self.direction == 'LEFT' or self.direction == 'RIGHT':
                self.rect = self.rect.move([15,10])
                
            Sound.fire_sound(self)
            self.travel = True

        # print(self.tank.rect)
        if self.rect[0] > 645 or self.rect[1] > 485 or self.rect[1] < -10 or self.rect[0] < -10:
            self.travel = False

    def rotate_bullet(self, new_direction):
        if new_direction == 'UP':
            self.image = pygame.transform.rotate(self.org_image, 180)
        elif new_direction == 'DOWN':
            self.image = pygame.transform.rotate(self.org_image, 0)
        elif new_direction == 'RIGHT':
            self.image = pygame.transform.rotate(self.org_image, 90)
        elif new_direction == 'LEFT':
            self.image = pygame.transform.rotate(self.org_image, 270)

        # def change_bullet_powerlevel(self,plevel):
    #     if plevel == 0:
    #         self.image = self.sprites.subsurface(14,92,10,17)
    #     elif plevel == 1:
    #         self.image = self.sprites.subsurface(35,92,10,17)
    #     elif plevel == 2:
    #         self.image = self.sprites.subsurface(56,91,10,17)
import pygame
from game import Sound 

class Tank:
    def __init__(self):
        # self.bullet = Bullet()
        self.sprites = pygame.image.load("Sprites/tank-blue.png")
        self.image = self.sprites.subsurface(11,7,40,54)
        self.rect = self.image.get_rect()
        # self.fire = False
        self.direction = 'DOWN'
        self.bullets = pygame.sprite.Group()
        self.bullet_speed = 10
        self.bullet_move_vec = {'UP':[0,-self.bullet_speed],'DOWN':[0,self.bullet_speed],
                                'RIGHT':[self.bullet_speed,0],'LEFT':[-self.bullet_speed,0]}

    def change_direction(self,new_direction):
        if new_direction == 'UP':
            self.image = self.sprites.subsurface(140,192,40,62)
        elif new_direction == 'DOWN':
            self.image = self.sprites.subsurface(11,7,40,54)
        elif new_direction == 'RIGHT':
            self.image = self.sprites.subsurface(131,141,61,45)
        elif new_direction == 'LEFT':
            self.image = self.sprites.subsurface(128,77,63,45)

    def fire(self):

        bullet = Bullet(self.bullets,self.direction)
        bullet.rect = self.rect
        bullet.update_position_vec = self.bullet_move_vec[self.direction]

        if self.direction == 'DOWN' or self.direction == 'UP':
            bullet.rect = bullet.rect.move([15,40])
                
        elif self.direction == 'LEFT' or self.direction == 'RIGHT':
            bullet.rect = bullet.rect.move([15,10])

        Sound.fire_sound(self)



class Bullet(pygame.sprite.Sprite):
    image = None
    def __init__(self,bullets,direction):
        pygame.sprite.Sprite.__init__(self, bullets)
        if Bullet.image is None:
            sprites = pygame.image.load("Sprites/bullets.png")
            Bullet.image = sprites.subsurface(14,92,10,17)

        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.update_position_vec = [0,5]
        self.rotate_bullet(direction)
    
    def update(self):
        self.rect = self.rect.move(self.update_position_vec)


        # print(self.tank.rect)
        if self.rect[0] > 645 or self.rect[1] > 485 or self.rect[1] < -10 or self.rect[0] < -10:
            # print('Destroyed')
            self.kill()

    def rotate_bullet(self, new_direction):
        if new_direction == 'UP':
            self.image = pygame.transform.rotate(self.image, 180)
        elif new_direction == 'RIGHT':
            self.image = pygame.transform.rotate(self.image, 90)
        elif new_direction == 'LEFT':
            self.image = pygame.transform.rotate(self.image, 270)

        # def change_bullet_powerlevel(self,plevel):
    #     if plevel == 0:
    #         self.image = self.sprites.subsurface(14,92,10,17)
    #     elif plevel == 1:
    #         self.image = self.sprites.subsurface(35,92,10,17)
    #     elif plevel == 2:
    #         self.image = self.sprites.subsurface(56,91,10,17)
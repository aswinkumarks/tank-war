from tank import Tank, Bullet
from game import Sound
import uuid
import pygame


class Player:
    def __init__(self, name, hp, ptype = 'local',network=None):
        # super().__init__()
        self.tank = Tank()
        self.pid = str(uuid.uuid4())
        self.ptype = ptype
        self.name = name
        self.hp = hp
        self.movement_speed = 5
        self.action = 'IDLE'
        self.game_mode = 'Single Player'
        self.ip = ''
        self.EXIT_GAME = False

        if ptype == 'remote':
            self.network = network


    def get_action(self):
        
        if self.ptype == 'local':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.EXIT_GAME = True
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP :
                        self.action = "UP"
                    elif event.key == pygame.K_DOWN :
                        self.action = "DOWN"
                    elif event.key == pygame.K_LEFT :
                        self.action = "LEFT"
                    elif event.key == pygame.K_RIGHT :
                        self.action = "RIGHT"

                    elif event.key == pygame.K_SPACE :
                        # Sound.fire_sound(self)
                        # self.tank.fire()
                        self.action = 'FIRE'

                elif event.type == pygame.KEYUP:
                    self.action = 'IDLE'
        
        else:
            if self.EXIT_GAME:
                self.network.stop()
                print('stop')
                exit(0)

            self.network.get_action(self.ip)


    def move(self):
        speed = self.movement_speed
        if self.action == 'LEFT':
            self.tank.rect = self.tank.rect.move([-speed,0])
        elif self.action == 'RIGHT':
            self.tank.rect = self.tank.rect.move([speed,0])
        elif self.action == 'DOWN':
            self.tank.rect = self.tank.rect.move([0,speed])
        elif self.action == 'UP':
            self.tank.rect = self.tank.rect.move([0,-speed])
        elif self.action == 'FIRE':
            self.tank.fire()
        # print(self.action)
        self.tank.change_direction(self.action)
        if self.action != 'IDLE' and self.action != 'FIRE':
            self.tank.direction = self.action
        

    


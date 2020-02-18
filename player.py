from tank import Tank, Bullet
from game import Sound
import pygame


class Player(Tank, Bullet):
    def __init__(self, name, hp, ptype = 'local',network=None):
        super().__init__()
        self.ptype = ptype
        self.name = name
        self.hp = hp
        self.movement_speed = 5
        self.action = 'IDLE'
        self.game_mode = 'Single Player'
        self.fire = False

        if ptype == 'remote':
            self.ip = ''
            self.network = network


    def get_action(self):
        if self.ptype == 'local':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True
                    exit(0)
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
                        self.fire = True

                elif event.type == pygame.KEYUP:
                    self.action = 'IDLE'
        
        else:
            self.network.get_action(this.ip)

    def move(self):
        speed = self.movement_speed
        if self.action == 'LEFT':
            self.tank_rect = self.tank_rect.move([-speed,0])
        elif self.action == 'RIGHT':
            self.tank_rect = self.tank_rect.move([speed,0])
        elif self.action == 'DOWN':
            self.tank_rect = self.tank_rect.move([0,speed])
        elif self.action == 'UP':
            self.tank_rect = self.tank_rect.move([0,-speed])
        
        self.change_direction(self.action)
        self.direction = self.action
        
        if self.fire:
            self.fire = False
            Sound.fire_sound(self)
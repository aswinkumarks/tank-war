from .tank import Tank, Bullet
from .game import Sound
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
        self.action = 'IDLE'
        self.game_mode = 'Single Player'
        self.ip = ''
        self.prev_fire_tick = pygame.time.get_ticks()
        self.EXIT_GAME = False

        if ptype == 'remote':
            self.network = network


    def get_action(self):
        
        if self.ptype == 'local':
            self.action = 'IDLE'
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
                        current_tick = pygame.time.get_ticks()
                        if current_tick - self.prev_fire_tick > 400:
                            self.prev_fire_tick = current_tick
                            self.action = 'FIRE'
        
                # elif event.type == pygame.KEYUP:
                #     self.action = 'IDLE'
        
        else:
            self.network.get_action(self.ip)
        
        if self.EXIT_GAME:
            # self.network.stop()
            print('stop')
            pygame.quit()
            # exit(0)

        self.tank.move(self.action)
        

    


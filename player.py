from tank import Tank
import pygame

class Player(Tank):
    def __init__(self, name, hp, ptype = 'local'):
        super().__init__()
        self.ptype = ptype
        self.name = name
        self.hp = hp

    def get_action(self):
        self.action = 'IDLE'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP :
                    self.action = "UP"
                elif event.key == pygame.K_DOWN :
                    self.action = "DOWN"
                    print("DOWN")
                elif event.key == pygame.K_LEFT :
                    self.action = "LEFT"
                elif event.key == pygame.K_RIGHT :
                    self.action = "RIGHT"

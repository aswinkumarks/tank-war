import pygame

FPS = 30
BLACK = (0,0,0)
fps_obj = pygame.time.Clock()

class Gameplay:
    def __init__(self,players,full_screen=False, mode = 'Single Player'):
        pygame.init()
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Tank War")
        pygame.key.set_repeat(5)
        self.mode = mode
        self.players = players

        if full_screen == True:
            self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        else:
            self.screen = pygame.display.set_mode((640, 480))

        # if mode == 'Multi Player':
        #     self.network = Network()
        # screen.fill(black)

    def update_screen(self):
        self.screen.fill(BLACK)
        for player in self.players:
            self.screen.blit(player.tank.image, player.tank.rect)
            self.screen.blit(player.tank.bullet.image, player.tank.bullet.rect)
        pygame.display.flip()

    def show_menu(self):
        pass

    def add_player(self,player):
        self.players.append(player)
        if self.mode=='Multi Player':
            for player in self.players:
                if player.ptype == 'remote':
                    pass


    def start(self):
        while True:
            for player in self.players:
                player.get_action()
                player.move()
            self.update_screen()
            fps_obj.tick(FPS)


class Sound:
    def __init__(self):
        pygame.mixer.init()
    
    def fire_sound(self):
        pygame.mixer.Sound("sounds/fire.wav").play()
    
    def crash_sound(self):
        pygame.mixer.Sound("sounds/crash.ogg").play()
    
    def damage_sound(self):
        pygame.mixer.Sound("sounds/damage.mp3").play()
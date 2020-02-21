import pygame


FPS = 30
BLACK = (0,0,0)

class Gameplay:
    def __init__(self,players,full_screen=False, mode = 'Single Player'):
        pygame.init()
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Tank War")
        pygame.key.set_repeat(10)
        self.mode = mode
        self.players = players
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 32) 

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
            player.tank.draw(self.screen)
            
        pygame.display.flip()

    def show_menu(self):
        # self.screen.draw.text("hello world", (20, 100))
        text = self.font.render('Tank War', True, (255,255,0), (0,0,0)) 
        textRect = text.get_rect()  
        self.screen.blit(text,textRect)
        pygame.display.flip()
        while True:
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
                # player.tank.move()

            self.update_screen()
            self.timer.tick(FPS)


class Sound:
    def __init__(self):
        pygame.mixer.init()
    
    def fire_sound(self):
        pygame.mixer.Sound("sounds/fire.wav").play()
    
    def crash_sound(self):
        pygame.mixer.Sound("sounds/crash.ogg").play()
    
    def damage_sound(self):
        pygame.mixer.Sound("sounds/damage.mp3").play()
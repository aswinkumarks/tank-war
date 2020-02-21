import pygame

FPS = 30
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,200)
RED = (255,0,0)
WHITE = (255,255,255)

HEIGHT = 480
WIDTH = 640

class Gameplay:
    def __init__(self,players,full_screen=False, mode = 'Single Player'):
        pygame.init()
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Tank War")
        pygame.key.set_repeat(10)
        self.mode = mode
        self.players = players
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.small_font =  pygame.font.Font('freesansbold.ttf', 24)

        if full_screen == True:
            self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # if mode == 'Multi Player':
        #     self.network = Network()
        # screen.fill(black)

    def update_screen(self):
        self.screen.fill(BLACK)
        for player in self.players:
            player.tank.draw(self.screen)
            
        pygame.display.flip()

    def text_format_draw(self, text, color, x, y, font, menu_id, selected):
        if selected == menu_id:
            color = WHITE
        text = font.render(text, True, color, (0,0,0)) 
        textRect = text.get_rect()  
        # print(self.font.size('Tank War'))
        textRect[0], textRect[1] = x - textRect[2]/2, y
        # print(textRect)
        self.screen.blit(text,textRect)


    def draw_menu(self, selected):
        self.text_format_draw('Tank War', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
        self.text_format_draw('Singleplayer',BLUE , WIDTH/2, HEIGHT/8 + 100, self.small_font, 0, selected)
        self.text_format_draw('Multiplayer', BLUE, WIDTH/2, HEIGHT/8 + 130, self.small_font, 1, selected)
        self.text_format_draw('Settings', BLUE, WIDTH/2, HEIGHT/8 + 160, self.small_font, 2, selected)
        self.text_format_draw('Quit', RED, WIDTH/2, HEIGHT/8 + 200, self.small_font, 3, selected)

    def show_menu(self):
        # self.screen.draw.text("hello world", (20, 100))
        
        # set-repeat 10 is causing menu selction issue and is also causing multiple bullets to fire when pressing spacebar once
        pygame.key.set_repeat(0)

        selected = 0
        self.draw_menu(selected)
        pygame.display.flip()
        s = Sound()
        s.menu_music()

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP and selected >= 1:
                        selected -= 1
                    elif event.key==pygame.K_DOWN and selected < 3:
                        selected += 1
    
                    self.draw_menu(selected)
                    pygame.display.flip()

                    if event.key==pygame.K_RETURN:
                        if selected == 0:
                            # reverting back to set-repeat 10
                            pygame.key.set_repeat(20)
                            pygame.mixer.music.fadeout(3000)
                            self.start()
                        elif selected == 3:
                            pygame.quit()
                                   

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
        # pygame.mixer.Sound("sounds/damage.mp3").play()
        pygame.mixer.music.load("sounds/damage.mp3")
        pygame.mixer.music.play()
    
    def menu_music(self):
        # pygame.mixer.Sound("sounds/menu.mp3").play()
        pygame.mixer.music.load("sounds/menu.mp3")
        pygame.mixer.music.play()
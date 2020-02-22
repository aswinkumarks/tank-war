import pygame
from player import Enemy,Player
from sound import Sound

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
        
        self.enemies = pygame.sprite.Group()
        self.no_enemies = 2
        # self.e1 = Enemy()

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
        
        # if self.e1.hp > 0:
        #     self.e1.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
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
        self.no_enemies = 2

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
                            p1 = Player('Aswin',100)
                            self.add_player(p1)
                            Enemy(self.enemies)
                            Enemy(self.enemies)
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
        s = Sound()
        while True:
            for player in self.players:
                player.get_action()
                for enemy in self.enemies:
                    bullect_collided = pygame.sprite.spritecollideany(enemy, player.tank.bullets)
                    if bullect_collided is not None:
                        bullect_collided.kill()
                        self.enemies.remove(enemy)
                        s.crash_sound()


            for enemy in self.enemies:
                enemy.get_action(self.players)
                for player in self.players:
                    bullect_collided = pygame.sprite.spritecollideany( player.tank, enemy.bullets)
                    if bullect_collided is not None:
                        player.hp -=10
                        print('HP:',player.hp)
                        s.crash_sound()
                        bullect_collided.kill()
                        if player.hp <= 0:
                            print('You died')
                            self.players.remove(player)
                            self.enemies.empty()
                            self.show_menu()

            if len(self.enemies) == 0:
                self.no_enemies += 1
                for _ in range(self.no_enemies):
                    Enemy(self.enemies)


            self.update_screen()
            self.timer.tick(FPS)

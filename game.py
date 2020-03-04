import pygame
from player import Enemy,Player
from network import Network
from sound import Sound

FPS = 30
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,200)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

HEIGHT = 480
WIDTH = 640
s = Sound()

class Gameplay:
    def __init__(self,full_screen=False, mode = 'Single Player'):
        pygame.init()
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Tank War")
        pygame.key.set_repeat(10)
        self.mode = mode
        self.players = []
        self.available_servers = []
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.small_font =  pygame.font.Font('freesansbold.ttf', 24)
        self.tiny_font = pygame.font.Font('freesansbold.ttf', 18)
        self.active_menu = 'Main menu'
        self.network = Network(self.players)
        
        self.enemies = pygame.sprite.Group()
        self.no_enemies = 2

        if full_screen == True:
            self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # screen.fill(black)

    def update_screen(self):
        self.screen.fill(BLACK)
        for player in self.players:
            player.tank.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        pygame.display.flip()

    def text_format_draw(self, text, color, x, y, font, menu_id, selected):
        if selected == menu_id:
            # color = BLUE
            font = self.small_font
            text = "> " + text + " <"
        text = font.render(text, True, color, (0,0,0)) 
        textRect = text.get_rect()  
        textRect[0], textRect[1] = x - textRect[2]/2, y
        self.screen.blit(text,textRect)


    def draw_menu(self, selction):
        self.screen.fill(BLACK)
        if self.active_menu == 'Main menu':
            self.text_format_draw('TANK WAR', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
            self.text_format_draw('Singleplayer',WHITE , WIDTH/2, HEIGHT/8 + 100, self.tiny_font, 1, selction)
            self.text_format_draw('Multiplayer', WHITE, WIDTH/2, HEIGHT/8 + 130, self.tiny_font, 2, selction)
            self.text_format_draw('Settings', WHITE, WIDTH/2, HEIGHT/8 + 160, self.tiny_font, 3, selction)
            self.text_format_draw('Quit', RED, WIDTH/2, HEIGHT/8 + 200, self.tiny_font, 4, selction)

        elif self.active_menu == 'Multi-player menu':
            self.text_format_draw('Join Server',WHITE , WIDTH/2, HEIGHT/8 + 100, self.tiny_font, 1, selction)
            self.text_format_draw('Host Server', WHITE, WIDTH/2, HEIGHT/8 + 130, self.tiny_font, 2, selction)

        elif self.active_menu == 'List available servers':
            self.text_format_draw('Available Servers', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
            for i in range(len(self.available_servers)):
                self.text_format_draw(self.available_servers[i][0],WHITE , WIDTH/2, HEIGHT/8 + 100 + i * 20, self.tiny_font, i+1, selction)
        
        elif self.active_menu == 'Show connected clients':
            self.text_format_draw('Connected Players', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
            for i in range(len(self.players)):
                self.text_format_draw(self.playesrs[i].name,WHITE , WIDTH/2, HEIGHT/8 + 100 + i * 20, self.tiny_font, -1, 2)

        pygame.display.flip()
                                    

    def show_menu(self):
        pygame.key.set_repeat(0)
        self.no_enemies = 2
        selected = 1
        self.draw_menu(selected)
        s.menu_music()

        while True:
            no_entries = {'Main menu':4, 'Multi-player menu':2,
                          'Show connected clients':3,'List available servers':len(self.available_servers)}
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.active_menu = 'Main menu'
                        self.network.allowconnection = False
                        self.network.server_flag = False
                        self.network.listen = False

                    if event.key==pygame.K_UP and selected >= 1:
                        selected -= 1
                    elif event.key==pygame.K_DOWN and selected < no_entries[self.active_menu]:
                        selected += 1

                    if event.key==pygame.K_RETURN:
                        if self.active_menu == 'Main menu':
                            if selected == 1:
                                # reverting back to set-repeat 10
                                pygame.key.set_repeat(20)
                                pygame.mixer.music.fadeout(2000)
                                p1 = Player('Warrior',100)
                                self.add_player(p1)
                                Enemy(self.enemies)
                                Enemy(self.enemies)
                                self.start()

                            elif selected == 2:
                                self.active_menu = 'Multi-player menu'
                                selected = 1

                            elif selected == 4:
                                pygame.quit()

                        elif self.active_menu =='Multi-player menu':
                            if selected == 1:
                                self.network.broadcast()
                                self.active_menu = 'Show connected clients'                            
                            elif selected == 2:
                                self.network.start_listen_server(self.available_servers) 
                                self.active_menu = 'List available servers'

            self.timer.tick(FPS)
            self.draw_menu(selected)
                                   

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
                if player.tank.state == player.tank.STATE_DESTROYED:
                    self.players.remove(player)
                    self.enemies.empty()
                    self.text_format_draw('Game OVER', YELLOW, WIDTH/2, HEIGHT/8 + 250, self.font, -1, -2)
                    self.show_menu()
                    
                for enemy in self.enemies:
                    bullect_collided = pygame.sprite.spritecollideany(enemy, player.tank.bullets)
                    if bullect_collided is not None:
                        bullect_collided.kill()
                        # enemy.explode(self.screen, [enemy.rect[0], enemy.rect[1]])
                        enemy.state = enemy.STATE_EXPLODING
                        s.crash_sound()
                        
                    if enemy.state == enemy.STATE_DESTROYED:
                        self.enemies.remove(enemy)



            for enemy in self.enemies:
                enemy.get_action(self.players)
                for player in self.players:
                    bullect_collided = pygame.sprite.spritecollideany( player.tank, enemy.bullets)
                    if bullect_collided is not None:
                        player.hp -= 20
                        print('HP:',player.hp)
                        s.damage_sound()
                        bullect_collided.kill()
                        if player.hp <= 0:
                            player.tank.state = player.tank.STATE_EXPLODING           
                            s.crash_sound()


            if len(self.enemies) == 0:
                self.no_enemies += 1
                for _ in range(self.no_enemies):
                    Enemy(self.enemies)


            self.update_screen()
            self.timer.tick(FPS)

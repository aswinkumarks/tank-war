import pygame

BLACK = (0,0,0)

class Gameplay:
    players = []

    def __init__(self,full_screen=False):
        pygame.init()
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Tank War")

        if full_screen == True:
            self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        else:
            self.screen = pygame.display.set_mode((640, 480))
        # screen.fill(black)

    def update_screen(self):
        self.screen.fill(BLACK)
        for player in self.players:
            self.screen.blit(player.tank_image, player.tank_rect)
        pygame.display.flip()

    def show_menu(self):
        pass

    def add_player(self,player):
        self.players.append(player)

    def start(self):
        while True:
            for player in self.players:
                player.get_action()
                if player.action == 'DOWN':
                    print(player.tank_rect)
                    player.tank_rect = player.tank_rect.move([2,2])
                    print(player.tank_rect)
            self.update_screen()

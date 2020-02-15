import pygame

class Gameplay:
    def __init__(self,full_screen=False):
        pygame.init()
        infoObject = pygame.display.Info()
        if full_screen == True:
            pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        else:
            pygame.display.set_mode((640, 480))
        # screen.fill(black)

    def update_screen(self):
        pygame.display.flip()

    def show_menu(self):
        pass
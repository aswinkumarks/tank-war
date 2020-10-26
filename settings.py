import pygame

def sprite_obstacles_init():
	global allObstacles
	allObstacles = pygame.sprite.Group()



FPS = 30

BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,200)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

TILE_SIZE = 50
MAP_DIM = 13
HEIGHT = MAP_DIM * TILE_SIZE
WIDTH = MAP_DIM * TILE_SIZE

TANK_H, TANK_W = 48, 48

# mute icon
mute_icon = pygame.image.load("Sprites/mute.png")
mute_icon = pygame.transform.scale(mute_icon, (20, 20))
mute_rect = mute_icon.get_rect()
mute_rect = mute_rect.move((10,10))

# hp icon
hp_icon = pygame.image.load("Sprites/hp.png")
hp_icon = pygame.transform.scale(hp_icon, (20, 20))
hp_rect = hp_icon.get_rect()
hp_rect = hp_rect.move((580,10))

# kill icon
kills_icon = pygame.image.load("Sprites/kills.png")
kills_icon = pygame.transform.scale(kills_icon, (20, 20))
kills_rect = kills_icon.get_rect()
kills_rect = kills_rect.move((510,10))
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
HEIGHT = 13*TILE_SIZE
WIDTH = 13*TILE_SIZE
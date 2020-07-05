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

TILE_SIZE = 25
HEIGHT = 26*TILE_SIZE
WIDTH = 26*TILE_SIZE
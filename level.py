import pygame
import os
import settings
from settings import TILE_SIZE
from map_gen import Map

class Tile(pygame.sprite.Sprite):
	(TILE_EMPTY, TILE_BRICK, TILE_STEEL) = '.','#','@'
	def __init__(self,tiles,ttype,pos):
		pygame.sprite.Sprite.__init__(self, tiles)
		settings.allObstacles.add(self)
		self.ttype = ttype
		if ttype == self.TILE_BRICK:
			brick = pygame.image.load("Sprites/brick.png")
			self.image = pygame.transform.scale(brick, (TILE_SIZE, TILE_SIZE))

		self.rect = self.image.get_rect()
		self.rect = self.rect.move(pos)
		self.visible = False
	
	def draw(self, screen):
		screen.blit(self.image, self.rect)


class Level:

	(TILE_EMPTY, TILE_BRICK, TILE_STEEL) = '.','#','@'

	def __init__(self):
		self.tiles = pygame.sprite.Group()
		self.lno = 1

	def load_level(self, random=False):
		if random:
			map_generator = Map(7,7)
			map_matrix = map_generator.generate()
			for row_index in range(settings.MAP_DIM):
				y = row_index * TILE_SIZE
				for col_index in range(settings.MAP_DIM):
					x = col_index * TILE_SIZE
					if map_matrix[row_index][col_index] == 1:
						Tile(self.tiles,"#",(x, y))
			
			# print(self.tiles)
			return True

		filename = "Levels/"+str(self.lno)
		if (not os.path.isfile(filename)):
			return False

		with open(filename, "r") as f:
			data = f.read().split("\n")

		x, y = 0, 0
		for row in data:
			for ch in row:
				if ch == self.TILE_BRICK:
					Tile(self.tiles,ch,(x, y))

				x += TILE_SIZE

			x = 0
			y += TILE_SIZE

		return True


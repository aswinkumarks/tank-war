import pygame
import os
import settings
from settings import TILE_SIZE


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


class Level:

	(TILE_EMPTY, TILE_BRICK, TILE_STEEL) = '.','#','@'

	def __init__(self):
		self.tiles = pygame.sprite.Group()
		self.lno = 1

	def load_level(self):
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


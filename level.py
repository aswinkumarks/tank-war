import pygame
import os

class Tile(pygame.sprite.Sprite):
	(TILE_EMPTY, TILE_BRICK, TILE_STEEL) = '.','#','@'
	def __init__(self,tiles,ttype,pos):
		pygame.sprite.Sprite.__init__(self, tiles)
		self.ttype = ttype
		if ttype == self.TILE_BRICK:
			brick = pygame.image.load("Sprites/brick.png")
			self.image = pygame.transform.scale(brick, (25, 25))

		elif ttype == self.TILE_EMPTY:
			self.image = pygame.Surface((25, 25))
		else:
			return True

		self.rect = self.image.get_rect()
		self.rect = self.rect.move(pos)


class Level:
	TILE_SIZE = 25
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
				Tile(self.tiles,ch,(x, y))
				x += self.TILE_SIZE
			x = 0
			y += self.TILE_SIZE

		return True


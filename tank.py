import pygame
from sound import game_sound
import random
import uuid
import settings

allTanks = []
CC = 5

class Tank(pygame.sprite.Sprite):
	(STATE_ALIVE,STATE_EXPLODING,STATE_DESTROYED) = range(3)

	def __init__(self, colour = "Blue"):
		super().__init__()
		allTanks.append(self)
		self.id = str(uuid.uuid4())
		self.hp = 20
		self.no_kills = 0

		if colour == "Blue":
			self.sprites = pygame.image.load("Sprites/tank-blue.png")
		else:
			self.sprites = pygame.image.load("Sprites/tank-green.png")

		tank_image = self.sprites.subsurface(11,7,40,54)
		self.image = pygame.transform.scale(tank_image,(settings.TANK_H,settings.TANK_W))
		# self.rect = self.image.get_rect()

		while True:
			# print("Finding co-ordinate")
			x = random.randint(0, settings.WIDTH//settings.TILE_SIZE - 1)
			y = random.randint(0, settings.HEIGHT//settings.TILE_SIZE - 1)
			x , y = x * settings.TILE_SIZE , y * settings.TILE_SIZE
			self.rect = pygame.Rect(x,y,settings.TANK_H - CC,settings.TANK_W - CC)
			collided_brick = pygame.sprite.spritecollideany(self,settings.allObstacles)
			collided_tanks = pygame.sprite.spritecollide(self,allTanks,dokill=False)
			flag = False

			for coll_tank in collided_tanks:
				if coll_tank != self:
					flag = True
					break

			if collided_brick == None and flag == False:
				break

		self.movement_speed = 5
		self.state = self.STATE_ALIVE

		sprites = pygame.image.load("Sprites/explosion.png")
		self.explosion_images = [sprites.subsurface(74, 11, 45, 40), sprites.subsurface(131, 5, 58, 53), 
					sprites.subsurface(191, 0, 65, 62), sprites.subsurface(262, 0, 58, 60), 
					sprites.subsurface(2, 68, 61, 57), sprites.subsurface(70, 70, 55, 55)]

		self.direction = 'DOWN'
		self.bullets = pygame.sprite.Group()
		self.bullet_speed = 10
		self.bullet_move_vec = {'UP':[0,-self.bullet_speed],'DOWN':[0,self.bullet_speed],
								'RIGHT':[self.bullet_speed,0],'LEFT':[-self.bullet_speed,0]}
		

	def change_direction(self,new_direction):
		if new_direction == 'UP':
			tank_image = self.sprites.subsurface(140,192,40,62)
		elif new_direction == 'DOWN':
			tank_image = self.sprites.subsurface(11,7,40,54)
		elif new_direction == 'RIGHT':
			tank_image = self.sprites.subsurface(131,141,61,45)
		elif new_direction == 'LEFT':
			tank_image = self.sprites.subsurface(128,77,63,45)

		self.image = pygame.transform.scale(tank_image,(48,48))

	def fire(self):

		bullet = Bullet(self.bullets,self.direction)
		bullet.rect.top = self.rect.top
		bullet.rect.left = self.rect.left
		bullet.update_position_vec = self.bullet_move_vec[self.direction]

		if self.direction == 'DOWN' or self.direction == 'UP':
			bullet.rect = bullet.rect.move([20,40])
				
		elif self.direction == 'LEFT' or self.direction == 'RIGHT':
			bullet.rect = bullet.rect.move([15,10])

		game_sound.fire_sound()

	def move(self,action):
		if self.state == self.STATE_DESTROYED or self.state == self.STATE_EXPLODING:
			return False

		prev_rect =  self.rect
	
		speed = self.movement_speed
		if action == 'LEFT':
			self.rect = self.rect.move([-speed,0])
		elif action == 'RIGHT':
			self.rect = self.rect.move([speed,0])
		elif action == 'DOWN':
			self.rect = self.rect.move([0,speed])
		elif action == 'UP':
			self.rect = self.rect.move([0,-speed])
		elif action == 'FIRE':
			self.fire()

		if self.rect[0] > (settings.HEIGHT - settings.TILE_SIZE) or \
					self.rect[1] > (settings.WIDTH - settings.TILE_SIZE) \
				or self.rect[1] < 0 or self.rect[0] < 0:
			self.rect = prev_rect
		else:
			collided_bricks = pygame.sprite.spritecollideany(self,settings.allObstacles)
			
			if collided_bricks is not None:
				# print("Collided",self)
				self.rect = prev_rect
			else:
				collided_tanks = pygame.sprite.spritecollide(self,allTanks,dokill=False)
				for coll_tank in collided_tanks:
					if coll_tank != self:
						print("Collition with ",coll_tank.id)
						self.rect = prev_rect
						break
				# pass

		if action != 'IDLE' and action != 'FIRE':
			self.change_direction(action)
			self.direction = action

	def draw(self,screen):
		if self.hp <= 0 and self.state != self.STATE_EXPLODING:
			self.state = self.STATE_EXPLODING
			game_sound.crash_sound()

		if self.state == self.STATE_ALIVE:
			self.bullets.update(self)
			self.bullets.draw(screen)
			screen.blit(self.image,self.rect)

		elif self.state == self.STATE_EXPLODING:
			if len(self.explosion_images) == 0:
				self.state = self.STATE_DESTROYED
				if len(self.bullets) > 0:
					self.bullets.update(self)
					self.bullets.draw(screen)
					return
				else:
					print(len(allTanks)," Killed ",self.id)
					# allTanks.remove(self)
					self.kill()
					# del self
					return

			screen.blit(self.explosion_images[0],self.rect)
			self.explosion_images.pop(0)

	def kill(self):
		pygame.sprite.Sprite.kill(self)
		allTanks.remove(self)


class Bullet(pygame.sprite.Sprite):
	image = None
	def __init__(self,bullets,direction):
		pygame.sprite.Sprite.__init__(self, bullets)
		if Bullet.image is None:
			sprites = pygame.image.load("Sprites/bullets.png")
			Bullet.image = sprites.subsurface(14,92,10,17)

		self.image = Bullet.image
		# self.rect = self.image.get_rect()
		self.damage = 10
		self.rect = pygame.Rect(0,0,5,5)
		self.update_position_vec = [0,5]
		self.rotate_bullet(direction)
	
	def update(self,mytank):
		self.rect = self.rect.move(self.update_position_vec)

		if self.rect[0] > settings.HEIGHT or self.rect[1] > settings.WIDTH \
				or self.rect[1] < -10 or self.rect[0] < -10:
			# print('Destroyed')
			self.kill()
		
		else:
			collided_bricks = pygame.sprite.spritecollideany(self,settings.allObstacles)
			if collided_bricks is not None:
				game_sound.bullet_hit_wall_sound()
				self.kill()

				# change bullet hitting wall sound
				game_sound.damage_sound()
			else:
				collided_tanks = pygame.sprite.spritecollide(self,allTanks,dokill=False)

				for coll_tank in collided_tanks:
					if coll_tank != mytank:
						coll_tank.hp -= self.damage
						game_sound.damage_sound()
						self.kill()

						if coll_tank.hp == 0:
							mytank.no_kills+=1


	def rotate_bullet(self, new_direction):
		if new_direction == 'UP':
			self.image = pygame.transform.rotate(self.image, 180)
		elif new_direction == 'RIGHT':
			self.image = pygame.transform.rotate(self.image, 90)
		elif new_direction == 'LEFT':
			self.image = pygame.transform.rotate(self.image, 270)


	# def change_bullet_powerlevel(self,plevel):
	#     if plevel == 0:
	#         self.image = self.sprites.subsurface(14,92,10,17)
	#     elif plevel == 1:
	#         self.image = self.sprites.subsurface(35,92,10,17)
	#     elif plevel == 2:
	#         self.image = self.sprites.subsurface(56,91,10,17)
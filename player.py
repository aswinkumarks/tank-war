from tank import Tank, Bullet
# from .game import HEIGHT, WIDTH   #### cyclic import need to fix
import uuid, random
import pygame
import settings
from sound import game_sound


class Player:
	def __init__(self, name, hp, ptype = 'local'):
	   
		self.tank = Tank()
		self.pid = str(uuid.uuid4())
		self.ptype = ptype
		self.name = name
		self.action = 'IDLE'
		self.addr = ()
		self.prev_fire_tick = pygame.time.get_ticks()
		self.EXIT_GAME = False

	def get_action(self):
		
		if self.ptype == 'local':
			self.action = 'IDLE'
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.EXIT_GAME = True
					
				elif event.type == pygame.KEYDOWN:

					if event.key==pygame.K_m:
						game_sound.mute_toggle()

					if event.type == pygame.K_q:
						self.EXIT_GAME = True

					if event.key == pygame.K_UP :
						self.action = "UP"
					elif event.key == pygame.K_DOWN :
						self.action = "DOWN"
					elif event.key == pygame.K_LEFT :
						self.action = "LEFT"
					elif event.key == pygame.K_RIGHT :
						self.action = "RIGHT"

					elif event.key == pygame.K_SPACE :
						current_tick = pygame.time.get_ticks()
						if current_tick - self.prev_fire_tick > 400:
							self.prev_fire_tick = current_tick
							self.action = 'FIRE'

				# elif event.type == pygame.KEYUP:
				#     self.action = 'IDLE'

		
		else:
			self.action = 'IDLE'
		
		if self.EXIT_GAME:
			# self.network.stop()
			print('stop')
			pygame.quit()
			# exit(0)

		self.tank.move(self.action)
		

class Enemy(Tank):
	def __init__(self,enemies):
		super().__init__(colour="Green")
		pygame.sprite.Sprite.__init__(self, enemies)
		self.hp = 20
		self.movement_speed = 3
		self.prev_fire_tick = 0

	def get_action(self,players):
		current_tick = pygame.time.get_ticks()
		# if current_tick - self.prev_fire_tick > 1000:
		# 	self.prev_fire_tick = current_tick
		# 	self.move('FIRE')
		# else:
		movement_prob = random.random()
		if movement_prob < 0.05 and \
			(current_tick - self.prev_fire_tick) > 500:
			self.prev_fire_tick = current_tick
			self.move('FIRE')
			return

		player = random.choice(players)
		p_x = player.tank.rect[0]
		p_y = player.tank.rect[1]
		action = 'IDLE'
		if p_x - self.rect[0] > 5:
			action = 'RIGHT'
		elif p_x - self.rect[0] < -5:
			action = 'LEFT'
		elif p_y - self.rect[1] > 5:
			action = 'DOWN'
		elif p_y - self.rect[1] < -5:
			action = 'UP'

		self.move(action)
   

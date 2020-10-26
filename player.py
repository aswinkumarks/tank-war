from tank import Tank, Bullet
import uuid, random
import pygame
import settings
from sound import game_sound
from aStar import AstarSearch
from threading import Thread
from powers import Powers


class Player:
	def __init__(self, name, ptype = 'local'):
	   
		self.tank = Tank()
		self.powers = Powers()
		self.pid = str(uuid.uuid4())
		self.ptype = ptype
		self.name = name
		self.action = 'IDLE'
		self.addr = ()
		self.prev_fire_tick = pygame.time.get_ticks()
		self.EXIT_GAME = False
		self.explored_tiles = []

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

	def check_LOS(self, px, py):
		
		tiles_up = list(filter(lambda x : (x.rect[0] // settings.TILE_SIZE == px or x.rect[0] // settings.TILE_SIZE == px-1 or x.rect[0] // settings.TILE_SIZE == px+1)\
			and x.rect[1]//settings.TILE_SIZE < py, settings.allObstacles))
		tiles_down = list(filter(lambda x : (x.rect[0] // settings.TILE_SIZE == px or x.rect[0] // settings.TILE_SIZE == px-1 or x.rect[0] // settings.TILE_SIZE == px+1)\
			and x.rect[1]//settings.TILE_SIZE > py, settings.allObstacles)) 
		tiles_left = list(filter(lambda x : (x.rect[1] // settings.TILE_SIZE == py or x.rect[0] // settings.TILE_SIZE == py-1 or x.rect[0] // settings.TILE_SIZE == py+1)\
			and x.rect[0]//settings.TILE_SIZE < px, settings.allObstacles))
		tiles_right = list(filter(lambda x : (x.rect[1] // settings.TILE_SIZE == py or x.rect[0] // settings.TILE_SIZE == py-1 or x.rect[0] // settings.TILE_SIZE == py+1)\
			and x.rect[0]//settings.TILE_SIZE > px, settings.allObstacles))

		blocking_tile_up, blocking_tile_right, blocking_tile_left, blocking_tile_down = None, None, None, None	
		# dist to nearest block
		if len(tiles_up) != 0:
			blocking_tile_up = min(tiles_up, key=lambda x: abs(x.rect[1]//settings.TILE_SIZE - py))
		if len(tiles_down) != 0:
			blocking_tile_down = min(tiles_down, key=lambda x: abs(x.rect[1]//settings.TILE_SIZE - py))
		if len(tiles_left) != 0:
			blocking_tile_left = min(tiles_left, key=lambda x: abs(x.rect[0]//settings.TILE_SIZE - px))
		if len(tiles_right) != 0:
			blocking_tile_right = min(tiles_right, key=lambda x: abs(x.rect[0]//settings.TILE_SIZE - px))


		bu = (px, 0)
		bl = (0, py)
		bd = (px, settings.MAP_DIM)
		br = (settings.MAP_DIM, py)

		if blocking_tile_up is not None:
			bu = (blocking_tile_up.rect[0]//settings.TILE_SIZE, blocking_tile_up.rect[1]//settings.TILE_SIZE)
		if blocking_tile_left is not None:
			bl = (blocking_tile_left.rect[0]//settings.TILE_SIZE, blocking_tile_left.rect[1]//settings.TILE_SIZE)
		if blocking_tile_down is not None:
			bd = (blocking_tile_down.rect[0]//settings.TILE_SIZE, blocking_tile_down.rect[1]//settings.TILE_SIZE)
		if blocking_tile_right is not None:
			br = (blocking_tile_right.rect[0]//settings.TILE_SIZE, blocking_tile_right.rect[1]//settings.TILE_SIZE)
		
		return bu, bl, bd, br

	def explore_map(self):
		# add unexplored bricks(tiles)
		px = (self.tank.rect[0] + settings.TANK_W/2) // settings.TILE_SIZE
		py = (self.tank.rect[1] + settings.TANK_H/2) // settings.TILE_SIZE
		bu, bl, bd, br = self.check_LOS(px, py)
		# print(bu, bl, bd, br)
		
		for tile in settings.allObstacles:
			
			tx = tile.rect[0]//settings.TILE_SIZE
			ty = tile.rect[0]//settings.TILE_SIZE

			if tx >= bl[0] and tx <= br[0]:
				if abs(ty-py) < 2:
					tile.visible = True
			
			if ty >= bu[0] and ty <= bd[0]:
				if abs(tx-px) < 2:
					tile.visible = True
					

class Enemy(Tank):
	def __init__(self,enemies):
		super().__init__(colour="Green")
		pygame.sprite.Sprite.__init__(self, enemies)
		self.hp = 10
		self.movement_speed = 3
		self.prev_fire_tick = 0
		self.prev_path_find_tick = 0
		self.actions = []
		self.thread_started = False

	def findPathToPlayer(self,player):
		self.thread_started = True
		# tile_size = settings.TILE_SIZE
		
		# curr_cord = (self.rect[0]//tile_size , self.rect[1]//tile_size)
		# target_cord = (player.tank.rect[0]//tile_size, player.tank.rect[1]//tile_size)

		curr_cord = (self.rect[0] , self.rect[1])
		target_cord = (player.tank.rect[0], player.tank.rect[1])
		self.actions = AstarSearch.findPath(curr_cord,target_cord)
		self.thread_started = False

	def get_action(self,players):
		current_tick = pygame.time.get_ticks()

		movement_prob = random.random()
		if movement_prob < 0.05 and \
			(current_tick - self.prev_fire_tick) > 500:
			self.prev_fire_tick = current_tick
			self.move('FIRE')
			return

		player = random.choice(players)

		if len(self.actions) == 0 and (current_tick - self.prev_path_find_tick) > 2000:
			self.prev_path_find_tick = current_tick
			if not self.thread_started:
				t = Thread(target=self.findPathToPlayer,args=(player,))
				t.start()
				# exit(0)

		if len(self.actions) != 0:
			nextMove = self.actions.pop()
			self.move(nextMove)
		else:
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
		


   

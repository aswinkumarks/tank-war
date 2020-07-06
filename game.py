import pygame
from player import Enemy,Player
from network import Network
from sound import game_sound
from level import Level
from settings import *
import settings
global allObstacles
# s = Sound()

class Gameplay:
	def __init__(self,server_port,full_screen=False):
		pygame.init()
		infoObject = pygame.display.Info()
		pygame.display.set_caption("Tank War")
		pygame.key.set_repeat(10)

		self.level = Level()
		self.mode = 'Single Player'
		self.players = []
		self.available_servers = []
		self.timer = pygame.time.Clock()
		self.font = pygame.font.Font('freesansbold.ttf', 36)
		self.small_font =  pygame.font.Font('freesansbold.ttf', 24)
		self.tiny_font = pygame.font.Font('freesansbold.ttf', 18)
		self.active_menu = 'Main menu'

		self.network = Network(server_port,self)
		self.start_game = False
		
		self.enemies = pygame.sprite.Group()
		self.no_enemies = 2

		# mute icon
		self.mute_icon = pygame.image.load("Sprites/mute.png")
		self.mute_icon = pygame.transform.scale(self.mute_icon, (20, 20))
		self.mute_rect = self.mute_icon.get_rect()
		self.mute_rect = self.mute_rect.move((10,10))

		if full_screen == True:
			self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
		else:
			self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

		# screen.fill(black)

	def update_screen(self):
		self.screen.fill(BLACK)
		self.level.tiles.draw(self.screen)
		if game_sound.mute:
			self.screen.blit(self.mute_icon, self.mute_rect)

		for player in self.players:
			player.tank.draw(self.screen)
		
		for enemy in self.enemies:
			enemy.draw(self.screen)

		pygame.display.flip()

	def text_format_draw(self, text, color, x, y, font, menu_id, selected):
		if selected == menu_id:
			# color = BLUE
			font = self.small_font
			text = "> " + text + " <"
		text = font.render(text, True, color, (0,0,0)) 
		textRect = text.get_rect()  
		textRect[0], textRect[1] = x - textRect[2]/2, y
		self.screen.blit(text,textRect)


	def draw_menu(self, selction):
		self.screen.fill(BLACK)
		# self.level.tiles.draw(self.screen)
		if self.active_menu == 'Main menu':
			self.text_format_draw('TANK WAR', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
			self.text_format_draw('Singleplayer',WHITE , WIDTH/2, HEIGHT/8 + 100, self.tiny_font, 1, selction)
			self.text_format_draw('Multiplayer', WHITE, WIDTH/2, HEIGHT/8 + 130, self.tiny_font, 2, selction)
			self.text_format_draw('Settings', WHITE, WIDTH/2, HEIGHT/8 + 160, self.tiny_font, 3, selction)
			self.text_format_draw('Quit', RED, WIDTH/2, HEIGHT/8 + 200, self.tiny_font, 4, selction)

		elif self.active_menu == 'Multi-player menu':
			self.text_format_draw('Host Server', WHITE, WIDTH/2, HEIGHT/8 + 100, self.tiny_font, 1, selction)
			self.text_format_draw('Join Server',WHITE , WIDTH/2, HEIGHT/8 + 130, self.tiny_font, 2, selction)

		elif self.active_menu == 'List available servers':
			self.text_format_draw('Available Servers', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
			for i in range(len(self.available_servers)):
				self.text_format_draw(self.available_servers[i][0],WHITE , WIDTH/2, HEIGHT/8 + 100 + i * 20, self.tiny_font, i+1, selction)

		
		elif self.active_menu == 'Show connected clients':
			self.text_format_draw('Connected Players', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
			for i in range(len(self.players)):
				self.text_format_draw(self.players[i].name,WHITE , WIDTH/2, HEIGHT/8 + 100 + i * 20, self.tiny_font, -1, 2)

		if game_sound.mute:
			self.screen.blit(self.mute_icon, self.mute_rect)

		pygame.display.flip()
									

	def show_menu(self):
		pygame.key.set_repeat(0)
		self.no_enemies = 2
		selected = 1
		self.draw_menu(selected)
		game_sound.menu_music()
		self.level.load_level()

		while True:
			no_entries = {'Main menu':4, 'Multi-player menu':2,
						  'Show connected clients':3,
						  'List available servers':len(self.available_servers)}

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					self.network.allowconnection = False
					self.network.server_flag = False
					self.network.listen = False
					pygame.quit()

				if event.type==pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.active_menu = 'Main menu'
						self.network.reset()
					
					if event.key==pygame.K_m:
							game_sound.mute_toggle()

					if event.key==pygame.K_UP and selected > 1:
						selected -= 1
					
					elif event.key==pygame.K_DOWN and selected < no_entries[self.active_menu]:
						selected += 1

					if event.key==pygame.K_RETURN:
						# print(selected)
						if self.active_menu == 'Main menu':
							if selected == 1:
								self.mode = 'Single Player'
								self.start_game = True
								# reverting back to set-repeat 10

							elif selected == 2:
								self.mode = 'Multi Player'
								self.active_menu = 'Multi-player menu'
								selected = 1

							elif selected == 4:
								pygame.quit()

						elif self.active_menu == 'Multi-player menu':
							# print(selected)
							if selected == 1:
								self.network.start_broadcast()
								self.active_menu = 'Show connected clients'                            
							
							elif selected == 2:
								selected = 1
								self.network.start_listen_server()
								self.network.start_server()
								self.active_menu = 'List available servers'

						elif self.active_menu == 'List available servers':
							p1 = Player('Player 2',100)
							self.add_player(p1)
							self.network.join_server(p1,selected-1)
							# self.network.start_server()

						elif self.active_menu == 'Show connected clients':
							p1 = Player('Warrior',100)
							self.add_player(p1)
							self.network.send_connected_player_info()

			# print('pass')
			if self.start_game:
				if self.mode == 'Single Player':
					p1 = Player('Warrior',100)
					self.add_player(p1)
					Enemy(self.enemies)
					Enemy(self.enemies)

				pygame.mixer.music.fadeout(2000)
				print('Game started')
				self.start()        


			self.timer.tick(FPS)
			self.draw_menu(selected)
								   

	def add_player(self,player):
		if player.ptype == 'local':  
			player.addr = (self.network.serverIP,self.network.serverPort)
		
		self.players.append(player)
		# if self.mode=='Multi Player':
		#     for player in self.players:
		#         if player.ptype == 'remote':
		#             pass


	def start(self):
		pygame.key.set_repeat(20)
		# self.update_screen()
		# self.level.load_level()
		while True:
			for player in self.players:
				player.get_action()

				if player.tank.state == player.tank.STATE_DESTROYED:
					self.players.remove(player)
					self.enemies.empty()
					self.text_format_draw('Game OVER', YELLOW, WIDTH/2, HEIGHT/8 + 250, self.font, -1, -2)
					self.show_menu()
				
				if self.mode == 'Multi Player' and player.ptype == 'local':
					if player.action != 'IDLE':
						self.network.send_action(player)

				for enemy in self.enemies:
					bullect_collided = pygame.sprite.spritecollideany(enemy, player.tank.bullets)
					if bullect_collided is not None:
						print(len(settings.allObstacles))
						bullect_collided.kill()
						# enemy.explode(self.screen, [enemy.rect[0], enemy.rect[1]])
						enemy.state = enemy.STATE_EXPLODING
						game_sound.crash_sound()


			self.update_screen()
			self.timer.tick(FPS)

			if self.mode == 'Multi Player':
				continue

			for enemy in self.enemies:
				enemy.get_action(self.players)
				for player in self.players:
					bullect_collided = pygame.sprite.spritecollideany( player.tank, enemy.bullets)
					if bullect_collided is not None:
						player.hp -= 20
						print('HP:',player.hp)
						game_sound.damage_sound()
						bullect_collided.kill()
						if player.hp <= 0:
							player.tank.state = player.tank.STATE_EXPLODING           
							game_sound.crash_sound()


			if len(self.enemies) == 0:
				# self.no_enemies += 1
				for _ in range(self.no_enemies):
					Enemy(self.enemies)



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
		self.local_player = None
		
		self.enemies = pygame.sprite.Group()
		self.no_enemies = 2

		if full_screen == True:
			self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
		else:
			self.screen = pygame.display.set_mode((WIDTH, HEIGHT))


	def draw_hud(self):				
		if game_sound.mute:
			self.screen.blit(settings.mute_icon, settings.mute_rect)

		# draw hp, kills on top right
		self.screen.blit(settings.hp_icon, settings.hp_rect)
		text_hp = self.tiny_font.render(str(self.local_player.tank.hp), True, WHITE, (0,0,0)) 
		self.screen.blit(text_hp,[610,12])
		self.screen.blit(settings.kills_icon, settings.kills_rect)
		text_kills = self.tiny_font.render(str(self.local_player.tank.no_kills), True, WHITE, (0,0,0)) 
		self.screen.blit(text_kills,[540,12])

	def update_screen(self):
		self.screen.fill(BLACK)
		self.draw_hud()

		for player in self.players:
			player.tank.draw(self.screen)

			# if player.ptype == "local":
			# 	player.explore_map()

		# single player
		for enemy in self.enemies:
			# player.explore_map()
			enemy.draw(self.screen)

		# render explored part of map
		for tile in self.level.tiles:
			if tile.visible:
				# print(tile)
				tile.draw(self.screen)

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
			self.text_format_draw('Singleplayer',WHITE , WIDTH/2, HEIGHT/8 + 140, self.tiny_font, 1, selction)
			self.text_format_draw('Multiplayer', WHITE, WIDTH/2, HEIGHT/8 + 170, self.tiny_font, 2, selction)
			self.text_format_draw('Settings', WHITE, WIDTH/2, HEIGHT/8 + 200, self.tiny_font, 3, selction)
			self.text_format_draw('Quit', RED, WIDTH/2, HEIGHT/8 + 230, self.tiny_font, 4, selction)

		elif self.active_menu == 'Multi-player menu':
			self.text_format_draw('Host Server', WHITE, WIDTH/2, HEIGHT/8 + 120, self.tiny_font, 1, selction)
			self.text_format_draw('Join Server',WHITE , WIDTH/2, HEIGHT/8 + 150, self.tiny_font, 2, selction)

		elif self.active_menu == 'List available servers':
			self.text_format_draw('Available Servers', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
			for i in range(len(self.available_servers)):
				self.text_format_draw(self.available_servers[i][0],WHITE , WIDTH/2, HEIGHT/8 + 110 + i * 20, self.tiny_font, i+1, selction)

		
		elif self.active_menu == 'Show connected clients':
			self.text_format_draw('Connected Players', YELLOW, WIDTH/2, HEIGHT/10, self.font, -1, -2)
			for i in range(len(self.players)):
				self.text_format_draw(self.players[i].name,WHITE , WIDTH/2, HEIGHT/8 + 100 + i * 20, self.tiny_font, -1, 2)

		if game_sound.mute:
			self.screen.blit(settings.mute_icon, settings.mute_rect)

		pygame.display.flip()
									

	def show_menu(self):
		pygame.key.set_repeat(0)
		self.no_enemies = 2
		selected = 1
		self.draw_menu(selected)
		game_sound.menu_music()
		self.level.load_level(random=True)

		self.active_menu = 'Main menu'
		self.start_game = False

		self.players = []

		while True:
			no_entries = {'Main menu':4, 'Multi-player menu':2,
						  'Show connected clients':3,
						  'List available servers':len(self.available_servers)}

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.network.allowconnection = False
					self.network.server_flag = False
					self.network.listen = False
					pygame.quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.active_menu = 'Main menu'
						self.network.reset()
					
					if event.key == pygame.K_m:
							game_sound.mute_toggle()

					if event.key == pygame.K_UP and selected > 1:
						selected -= 1
					
					elif event.key == pygame.K_DOWN and selected < no_entries[self.active_menu]:
						selected += 1

					if event.key == pygame.K_RETURN:
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
							p1 = Player('Player 2')
							self.add_player(p1)
							self.network.join_server(p1,selected-1)
							# self.network.start_server()

						elif self.active_menu == 'Show connected clients':
							p1 = Player('Warrior')
							self.add_player(p1)
							self.network.send_connected_player_info()

			# print('pass')
			if self.start_game:
				if self.mode == 'Single Player':
					p1 = Player('Warrior')
					self.add_player(p1)
					Enemy(self.enemies)
					# Enemy(self.enemies)

				pygame.mixer.music.fadeout(2000)
				print('Game started')
				self.start()        

			self.timer.tick(FPS)
			self.draw_menu(selected)
								   

	def add_player(self,player):
		if player.ptype == 'local':  
			player.addr = (self.network.serverIP,self.network.serverPort)
			self.local_player = player
		self.players.append(player)


	def start(self):
		pygame.key.set_repeat(20)
		self.update_screen()

		while True:
			self.local_player.explore_map()
			for player in self.players:
				player.get_action()
			
				if self.mode == "Single Player":
					for enemy in self.enemies:
						enemy.get_action(self.players)

						if player.tank.state == player.tank.STATE_DESTROYED:
							self.players.remove(player)
							for enemy in self.enemies:
								enemy.kill()					
							
					if len(self.enemies) == 0:
						for _ in range(self.no_enemies):
							Enemy(self.enemies)

				elif self.mode == 'Multi Player':
					if player.tank.state == player.tank.STATE_DESTROYED:
						self.players.remove(player)	
				
					# if player.ptype == 'local':
					if self.local_player.action != 'IDLE':
						self.network.send_action(self.local_player)			

			self.update_screen()
			self.timer.tick(FPS)

			if self.local_player.tank.state == self.local_player.tank.STATE_DESTROYED:
				self.reset()
				break

		self.show_menu()


	def reset(self):
		self.text_format_draw('Game OVER', YELLOW, WIDTH/2, HEIGHT/8 + 200, self.font, -1, -2)
		score = 'Score : ' + str(self.local_player.tank.no_kills)
		self.text_format_draw(score, YELLOW, WIDTH/2, HEIGHT/8 + 245, self.small_font, -1, -2)
		self.text_format_draw("Hit SPACE to exit to main menu", YELLOW, WIDTH/2, HEIGHT/8 + 280, self.tiny_font, -1, -2)

		# reset map
		for tile in self.level.tiles:
			tile.visible = False

		pygame.display.flip()
		pygame.event.clear()
		while True:
			event = pygame.event.wait()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE :
					break



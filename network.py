import socket
import time
import pickle
from threading import Thread
from player import Player

class Network:
	def __init__(self,port,game):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		# self.connection.settimeout(0.2)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))

		self.serverIP = s.getsockname()[0]
		self.serverPort = port
		self.allowconnection = True
		self.server_flag = True
		self.listen = True
		self.gameplay = game

	def reset(self):
		self.listen = False
		self.server_flag = False
		self.allowconnection = False
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

	def broadcast(self):
		conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		conn.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

		data = {'msg':'Tank War Server',
				'addr':(self.serverIP,self.serverPort)}
		data_string = pickle.dumps(data)

		self.allowconnection = True
		while self.allowconnection:
			conn.sendto(data_string, ('<broadcast>', 37020))
			# print("message sent!")
			time.sleep(2)
		conn.close()

	def start_broadcast(self):
		print('started broad cast')
		t1 = Thread(target=self.broadcast)
		t1.setDaemon(True)
		t1.start()
		self.start_server()

	def start_server(self):
		t = Thread(target=self.server)
		t.start()

	def server(self):
		# self.listen = False
		print('Server started')
		self.connection.bind(('', self.serverPort))
		self.server_flag = True
		while self.server_flag:
			add_player = True
			data_str, addr = self.connection.recvfrom(1024)
			data = pickle.loads(data_str)
			# print(data)

			if data['msg'] == 'Add Player' and self.allowconnection:
				pname = data['p_info']['pname']
				for player in self.gameplay.players:
					if player.name == pname:
						print('Already added player')
						add_player = False
						break

				if add_player:
					player = Player(pname,100,ptype='remote')
					player.pid = data['pid']
					player.addr = data['p_info']['addr']
					self.gameplay.add_player(player)
					print('New Player Added')

			elif data['msg'] == 'Action':
				for player in self.gameplay.players:
					if player.pid == data['pid']:
						# print(player.pid,data['Action'])
						player.action = data['Action']
						player.tank.move(player.action)

			elif data['msg'] == 'Start Game':
				self.gameplay.start_game = True


			# elif data['msg'] == 'Get Action':
			#     for player in self.players:
			#         if player.ptype == 'local':
			#             action = player.action
			#             action = action.encode()
			#             msg = b'Action:-'+action
			#             self.connection.sendto(msg,(addr[0],6000))
				
	def stop(self):
		self.allowconnection = False
		self.server_flag = False


	def listen4server(self):
		conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		conn.bind(('', 37020))
		self.listen = True
		while self.listen:
			data_str, addr = conn.recvfrom(1024)
			data = pickle.loads(data_str)

			print("received message: %s"%data['msg'])
			if data['msg'] != 'Tank War Server':
				continue

			if data['addr'] not in self.gameplay.available_servers:
				self.gameplay.available_servers.append(data['addr'])


	def start_listen_server(self):
		t1 = Thread(target=self.listen4server)
		t1.start()


	def send_data(self,data,addr):
		data_string = pickle.dumps(data)
		self.connection.sendto(data_string,addr)

	def send_action(self,player):
		data = {'pid':player.pid , 'msg':'Action', 'Action':player.action}
		for other_player in self.gameplay.players:
			if other_player.ptype != 'local':
				self.send_data(data, other_player.addr)
		

	def join_server(self,player,selection):
		self.listen = False
		data = {'pid':player.pid , 'msg':'Add Player', 
				'p_info':{'pname':player.name,'addr':player.addr} }

		self.send_data(data,self.gameplay.available_servers[selection])


	def send_connected_player_info(self):
		self.allowconnection = False
		for player in self.gameplay.players:
			if player.ptype == 'local':
				continue

			for player1 in self.gameplay.players:
				data = {'pid':player1.pid , 'msg':'Add Player', 
						'p_info':{'pname':player1.name,'addr':player1.addr}}
				self.send_data(data,player.addr)

		self.gameplay.start_game = True
		data = {'msg':'Start Game'}
		for player in self.gameplay.players:
			if player.ptype == 'remote':
				self.send_data(data,player.addr)

	
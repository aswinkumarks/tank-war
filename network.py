import socket
import time
import pickle
from threading import Thread
from player import Player

class Network:
    def __init__(self,game):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # self.connection.settimeout(0.2)
        self.serverIP = ''
        self.serverPort = 6000
        self.allowconnection = True
        self.server_flag = True
        self.listen = True
        self.gameplay = game

    def broadcast(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        message = b'Tank War Server'

        while self.allowconnection:
            conn.sendto(message, ('<broadcast>', 37020))
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
        self.listen = False
        self.connection.bind(('', self.serverPort))
        self.server_flag = True
        while self.server_flag:
            add_player = True
            data_str, addr = self.connection.recvfrom(1024)
            data = pickle.loads(data_str)
            print(data)

            if data['msg'] == 'Add Player' and self.allowconnection:
                pname = data['p_info']['pname']
                for player in self.gameplay.players:
                    if player.name == pname:
                        print('Already added player')
                        add_player = False

                if add_player:
                    player = Player(pname,100,ptype='remote')
                    player.pid = data['pid']
                    player.ip = addr[0]
                    self.gameplay.add_player(player)
                    print('New Player Added')

            elif data['msg'] == 'Action':
                for player in self.gameplay.players:
                    if player.pid == data['pid']:
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
            data, addr = conn.recvfrom(1024)
            print("received message: %s"%data)
            if data == b'Tank War Server':
                if addr not in self.gameplay.available_servers:
                    self.gameplay.available_servers.append(addr)


    def start_listen_server(self):
        t1 = Thread(target=self.listen4server)
        t1.start()


    def send_data(self,data,ip):
        data_string = pickle.dumps(data)
        self.connection.sendto(data_string,(ip,6000))

    def get_action(self,ip):
        self.connection.sendto(b'Get Action',(ip,6000))
    
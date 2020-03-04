import socket
import time
# from main import game
from threading import Thread
from player import Player

class Network:
    def __init__(self,players):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # self.connection.settimeout(0.2)
        self.serverIP = ''
        self.serverPort = 6000
        self.allowconnection = True
        self.server_flag = True
        self.listen = True
        self.players = players

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
        t1 = Thread(target=self.broadcast)
        t1.setDaemon(True)
        t1.start()
        t = Thread(target=self.server)
        t.start()


    def server(self):
        self.connection.bind(('', self.serverPort))
        self.server_flag = True
        while self.server_flag:
            message, addr = self.connection.recvfrom(1024)
            message = message.decode()
            if message[:10] == 'Add Player' and self.allowconnection:
                pname = message.split(':-')[1]
                player = Player(pname,100,ptype='remote',network=self)
                player.ip = addr[0]
                self.players.append(player)

            elif message[:6] == 'Action':
                for player in self.players:
                    if player.ip == addr[0]:
                        player.action = message.split(':-')[1]
                        player.move()

            elif message[:10] == 'Get Action':
                for player in self.players:
                    if player.ptype == 'local':
                        action = player.action
                        action = action.encode()
                        msg = b'Action:-'+action
                        self.connection.sendto(msg,(addr[0],6000))
                
    def stop(self):
        self.allowconnection = False
        self.server_flag = False


    def listen4server(self,available_servers):
        self.connection.bind(('', 37020))
        self.listen = True
        while self.listen:
            data, addr = self.connection.recvfrom(1024)
            print("received message: %s"%data)
            if data == b'Tank War Server':
                if addr not in available_servers:
                    available_servers.append(addr)


    def start_listen_server(self,available_servers):
        t1 = Thread(target=self.listen4server,args=(available_servers,))
        t1.start()


    def send_msg(self,msg,ip):
        msg = msg.encode()
        self.connection.sendto(msg,(ip,6000))

    def get_action(self,ip):
        self.connection.sendto(b'Get Action',(ip,6000))
    
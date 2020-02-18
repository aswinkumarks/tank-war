import socket
import time
from threading import Thread
from player import Player

class Network:
    def ___init__(self, players):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.connection.settimeout(0.2)
        self.serverIP = ''
        self.serverPort = '6000'
        self.allowconnection = True
        self.players = players

    def broadcast(self):
        message = b'Tank War Server'
        print(self.serverPort)
        while self.allowconnection:
            self.connection.sendto(message, ('<broadcast>', 37020))
            print("message sent!")
            time.sleep(2)

    def start_broadcast(self):
        t1 = Thread(target=self.broadcast)
        t1.setDaemon(True)
        t1.start()
        self.start_server()


    def server(self):
        self.connection.bind(("", 6000))
        while True:
            message, addr = self.connection.recvfrom(1024)
            if message[:10] == b'Add Player' and self.allowconnection:
                pname = message.split(':-')[1]
                player = Player(pname,100,ptype='remote',network=self)
                player.ip = addr[0]
                players.append(player)

            elif message[:6] == b'Action':
                for player in players:
                    if player.ip == addr[0]:
                        player.action = message.split(':-')[1]
                        player.move()

            elif message[:10] == b'Get Action':
                for player in players:
                    if player.ptype == 'local':
                        action = player.action
                        action = action.encode()
                        msg = b'Action:-'+action
                        self.connection.sendto(msg,(addr[0],6000))
                

    def start_server(self):
        t = Thread(target=self.server)
        t.start()

    def listen4server(self):
        self.connection.bind(("", 37020))
        while True:
            data, addr = self.connection.recvfrom(1024)
            print("received message: %s"%data)
            if data == b'Tank War Server':
                self.serverIP = addr[0]
                self.serverPort = addr[1]
                self.connection.sendto('Add Player:-Dvk',(addr[0],6000))
                break

    def get_action(self,ip):
        self.connection.sendto(b'Get Action',(ip,6000))
    
import socket
import time
from threading import Thread

class Network:
    def ___init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.connection.settimeout(0.2)
        self.serverIP = ''

    def broadcast(self):
        message = b'Tank War Server'
        while True:
            self.connection.sendto(message, ('<broadcast>', 37020))
            print("message sent!")
            time.sleep(2)
    
    def start_broadcast(self):
        t = Thread(target=self.broadcast)
        t.start()

    def listen4server(self):
        self.connection.bind(("", 37020))
        while True:
            data, addr = client.recvfrom(1024)
            print("received message: %s"%data)
            if data == b'Tank War Server':
                self.serverIP = addr[0]
                break
    
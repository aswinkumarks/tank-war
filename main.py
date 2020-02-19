import pygame
from game import Gameplay, Sound
from player import Player
from network import Network
import sys

if __name__ == '__main__':

    players = []

    if len(sys.argv) > 1:

        net = Network(players)
        if sys.argv[1] == 'server':
            net.start_broadcast()

        elif sys.argv[1] == 'client':
            net.listen4server()
        
        game = Gameplay(players,mode='Multi Player')
        sound = Sound()
        p1 = Player('Aswin',100)
        game.add_player(p1)
        game.start()

    else:
        game = Gameplay(players)
        sound = Sound()
        p1 = Player('Aswin',100)
        game.add_player(p1)
        game.start()
    # game.update_screen()


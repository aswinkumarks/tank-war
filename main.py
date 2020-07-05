import pygame
from game import Gameplay
import sys
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Tank War')
	parser.add_argument('--port', help = '--port port_no',
						default = 6000, type = int)
	args = parser.parse_args()
	game = Gameplay(args.port)
	game.show_menu()


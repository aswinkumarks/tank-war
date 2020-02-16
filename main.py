from game import Gameplay
from player import Player


if __name__ == '__main__':
    game = Gameplay()
    p1 = Player('Aswin',100)
    game.add_player(p1)
    game.start()
    # game.update_screen()


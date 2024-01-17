# import sys
# from network.server import Server

# server = Server()
# server.run()

from game.table import Table
from game.player import Player

player1 = Player(None, "player_1")
player2 = Player(None, "player_2")
player3 = Player(None, "player_3")

table = Table("Main table", 2)
table.join(player1)
table.join(player2)

table.start()

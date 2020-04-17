import socket
import sys
import os
from random import randint
from network.connection import Connection
from network.request import Request, RequestType

from game.lobby import Lobby
from game.player import Player
from game.table import Table

from uuid import uuid4


class Server:
    def __init__(self, config={}):
        self.config = config
        self.lobby = Lobby()
        self.tables = {}
        self.players = []
        self.connected_clients = []
        self.is_running = False

    def create_listening_socket(self, port=None):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if not port:
            port = randint(4500, 6001)

        connection_address = ('localhost', port)
        server_sock.bind(connection_address)
        server_sock.listen(1)

        self.server_connection = Connection(
            server_sock, connection_address, is_server=True)
        print(f'Listening at port {connection_address[1]}')
        self.is_running = True

    def get_new_player_connection(self):
        new_client_connection = self.server_connection.read_from_socket()
        return new_client_connection

    def is_closing(self, request):
        return request == 'close' and self.config.get('DEBUG') == True

    def main_loop(self):
        should_close = self.is_closing('')
        while not should_close:
            new_player_connection = self.get_new_player_connection()
            if new_player_connection:
                self.lobby.add_player(Player(new_player_connection, str(uuid4())))
                self.connected_clients.append(new_player_connection)

            for player in self.lobby.players:
                msg_from_client = player.connection.read_from_socket()
                if msg_from_client:

                    should_close = self.is_closing(msg_from_client)
                    if should_close:
                        self.close()
                        break

                    client_request = Request(msg_from_client)
                    if not client_request.is_valid:
                        player.connection.send('Invalid request')
                        continue

                    self.lobby.handle_request(
                        client_request, player)

    def close(self):
        self.lobby.close()
        self.server_connection.close()

    def run(self, port):
        self.create_listening_socket(port)
        self.main_loop()

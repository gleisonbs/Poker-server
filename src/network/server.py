import socket
import sys
import os
from random import randint
from network.connection import Connection
from network.request import Request, RequestType

from game.table import Table
from game.main_menu import MainMenu

class Server:
    def __init__(self, options):
        self.tables = {}
        self.players = []
        self.start_server()
        self.clients = []

    def start_server(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        connection_address = ('localhost', randint(4500, 6001))
        server_sock.bind(connection_address)
        server_sock.listen(1)
        
        self.server_connection = Connection(server_sock, connection_address, is_server = True)
        print(f'Listening at port {connection_address[1]}')

    def create_table(self, table_name, max_players):
        if table_name in self.tables:
            return f'table {table_name} already exists'
        self.tables[table_name] = Table(table_name, max_players)
        return f'table {table_name} was created\n: '

    def list_players(self):
        formatted_player_list = '\nPlayers in the server:\n'
        return formatted_player_list + '\n'.join([player_name for player_name in self.players])

    def list_tables(self):
        formatted_table_list = '\nTables in the server:\n'
        for table_name in self.tables:
            formatted_table_list += str(self.tables[table_name]) + '\n'
        return formatted_table_list + '\n: '

    def show_menu_to_client(self, client):
        client.send(f'{MainMenu.get()}')

    def run(self):
        while True:
            new_client = self.server_connection.read_from_socket()
            if new_client:    
                new_client_connection = Connection(new_client[0], new_client[1])
                self.clients.append(new_client_connection)
                self.show_menu_to_client(new_client_connection)
                    
            for client in self.clients:
                msg_from_client = client.read_from_socket()
                if msg_from_client:
                    client_request = Request(msg_from_client)
                    if not client_request.is_valid:
                        new_client_connection.send('Invalid request')
                        continue

                    self.choose_action(client_request, client)
    
    def choose_action(self, request, client):
        result = ''
        if request.type == RequestType.CREATE_TABLE:
            table_name = request.value[0]
            max_players = request.value[1]
            result = self.create_table(table_name, max_players)

        elif request.type == RequestType.JOIN_TABLE:
            self.tables[request.value[0]].join(client)
        
        elif request.type == RequestType.LIST_TABLES:
            result = self.list_tables()

        elif request.type == RequestType.LIST_PLAYERS:
            result = self.list_players()

        client.send(result)


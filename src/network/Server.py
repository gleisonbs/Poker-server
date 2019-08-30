import socket
import sys
import os
from select import select
from random import randint
from Connection import Connection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import MainMenu

class Table:
    pass

class Server:
    def __init__(self, options):
        self.tables = {}
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
        self.tables[table_name] = Table(max_players)

    def list_tables(self):
        return '\n'.join([table_name for table_name in self.tables])
            
    # def parse_options(self, options):
    #     for opt in options:
    #         if opt.startswith('-p'):
    #             table_size = opt.split(':')[1]
    #             self.table.max_players = int(table_size)
    #             print('Table Size:', table_size)

    def show_menu_to_client(self, client):
        client.send(f'{MainMenu.get()}')

    def run(self):
        while True:

            new_client, client_addr = self.server_connection.read_from_socket()
            if new_client:    
                new_client_connection = Connection(new_client, client_addr)
                self.clients.append(new_client_connection)
                self.show_menu_to_client(new_client_connection)
                    
            for client in self.clients:
                msg_from_client = client.read_from_socket()
                if (msg_from_client):
                    print(msg_from_client)
                

            # if self.table.is_full():
            #     if not self.table.is_round_in_progress:
            #         self.table.start_round()
            #         for player_conn, player_info in zip(self.clients, self.table.players):
            #             self.send(player_conn, str(player_info))

            #     if self.table.next_to_act is not None:
            #         self.broadcast_table_info()
            #         self.send_players_info()
            #     else:
            #         self.table.update_players_in_hand()
            #         self.table.current_call = 0
            #         for p in self.table.players:
            #             p.current_bettings = 0

            #         if len(self.table.cards_drawn) == 0:
            #             self.table.cards_drawn += self.table.deck.draw_cards(3)
            #         elif len(self.table.cards_drawn) == 3:
            #             self.table.cards_drawn += self.table.deck.draw_cards(1)
            #         elif len(self.table.cards_drawn) == 4:
            #             self.table.cards_drawn += self.table.deck.draw_cards(1)

            #             self.table.decide_winner()

            #             self.reset_table_state()

            #         print(self.table.cards_drawn)
            #         self.broadcast(f'{self.table.cards_drawn}')

            # if self.table.previous_action:
            #     self.broadcast(self.table.previous_action)

    # def send_players_info(self):
    #     for player_seat, player in enumerate(self.table.players):
    #         if player_seat not in self.table.players_out:
    #             self.send(self.clients[player_seat], f'Hand: {self.table.players[player_seat].hand}')
    #             self.send(self.clients[player_seat], f'Stack: {self.table.players[player_seat].stack}')
    #             if player_seat == self.table.next_to_act:
    #                 self.send(self.clients[player_seat], str(self.table.options))

    # def broadcast_table_info(self):
    #     self.broadcast('\nPot: ' + str(self.table.pot))
    #     self.broadcast('To Call: ' + str(self.table.call_value_for_player()))
    #     self.broadcast('Min Raise: ' + str(self.table.current_call*2))

    # def recv(self):
    #     for client in self.clients:
    #         try:
    #             data = client.recv(128)
    #             if client is self.clients[self.table.next_to_act]:
    #                 action = data.strip().decode()
    #                 if action.split(' ')[0] in self.table.options:
    #                     print(action)
    #                     self.table.player_action(action)
    #         except:
    #             pass

s = Server(sys.argv)
s.run()

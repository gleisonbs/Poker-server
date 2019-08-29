import socket
import select
import sys
from random import randint

class Server:
    def __init__(self, options):
        self.tables = {}
        print(options)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', randint(4000, 6001))
        self.server_sock.bind(server_address)
        self.server_sock.listen(1)
        self.clients = []
        self.table = Table()
        self.parse_options(options)

        print(f'Listening on port {server_address[1]}')

    def create_table(self, table_name, seats):
        if table_name in tables:
            print(f'table {table_name} already exists')
            return
        self.tables[table_name] = Table(max_players)

    def parse_options(self, options):
        for opt in options:
            if opt.startswith('-p'):
                table_size = opt.split(':')[1]
                self.table.max_players = int(table_size)
                print('Table Size:', table_size)

    def run(self):
        while True:
            if self.table.is_full():
                if not self.table.is_round_in_progress:
                    self.table.start_round()
                    for player_conn, player_info in zip(self.clients, self.table.players):
                        self.send(player_conn, str(player_info))

                if self.table.next_to_act is not None:
                    self.broadcast_table_info()
                    self.send_players_info()
                else:
                    self.table.update_players_in_hand()
                    self.table.current_call = 0
                    for p in self.table.players:
                        p.current_bettings = 0

                    if len(self.table.cards_drawn) == 0:
                        self.table.cards_drawn += self.table.deck.draw_cards(3)
                    elif len(self.table.cards_drawn) == 3:
                        self.table.cards_drawn += self.table.deck.draw_cards(1)
                    elif len(self.table.cards_drawn) == 4:
                        self.table.cards_drawn += self.table.deck.draw_cards(1)

                        self.table.decide_winner()

                        self.reset_table_state()

                    print(self.table.cards_drawn)
                    self.broadcast(f'{self.table.cards_drawn}')

            self.read_sockets()

            if self.table.previous_action:
                self.broadcast(self.table.previous_action)

    def reset_table_state(self):
        self.table.cards_drawn = []
        self.table.players_out = []
        self.table.update_positions()
        self.table.start_round()

    def read_sockets(self):
        read_list = self.clients + [self.server_sock]
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is self.server_sock:
                self.accept()
            else:
                self.recv()

    def send_players_info(self):
        for player_seat, player in enumerate(self.table.players):
            if player_seat not in self.table.players_out:
                self.send(self.clients[player_seat], f'Hand: {self.table.players[player_seat].hand}')
                self.send(self.clients[player_seat], f'Stack: {self.table.players[player_seat].stack}')
                if player_seat == self.table.next_to_act:
                    self.send(self.clients[player_seat], str(self.table.options))

    def broadcast_table_info(self):
        self.broadcast('\nPot: ' + str(self.table.pot))
        self.broadcast('To Call: ' + str(self.table.call_value_for_player()))
        self.broadcast('Min Raise: ' + str(self.table.current_call*2))

    def accept(self):
        connection, client_address = self.server_sock.accept()
        if not self.table.add_player(client_address):
            self.send(connection, 'Table is full\n')
            connection.close()
            return False
        else:
            connection.setblocking(0)
            self.clients.append(connection)
            print(f'Connection from {client_address}')
            return True

    def recv(self):
        for client in self.clients:
            try:
                data = client.recv(128)
                if client is self.clients[self.table.next_to_act]:
                    action = data.strip().decode()
                    if action.split(' ')[0] in self.table.options:
                        print(action)
                        self.table.player_action(action)
            except:
                pass

    def broadcast(self, data):
        for c in self.clients:
            self.send(c, data)

    def send(self, dest, data):
        data += '\n'
        dest.sendall(data.encode())

s = Server(sys.argv)
s.run()

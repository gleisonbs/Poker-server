from game.table import Table
from network.request import RequestType

class Lobby:
    def __init__(self):
        self.tables = {}
        self.players = []

    def handle_request(self, request, client):
        if request.type == RequestType.CREATE_TABLE:
            table_name = request.values[0]
            max_players = int(request.values[1])
            return self._create_table(table_name, max_players)
        elif request.type == RequestType.JOIN_TABLE:
            table_name = request.values[0]
            return self._join_table(table_name, client)
        elif request.type == RequestType.LIST_TABLES:
            return self._list_tables()
        elif request.type == RequestType.LIST_PLAYERS:
            return self.list_players()

    def _create_table(self, table_name, max_players):
        if table_name in self.tables:
            return f'table "{table_name}" already exists'
        self.tables[table_name] = Table(table_name, max_players)
        return f'table {table_name} was created\n: '

    def _join_table(table_name, client):
        return self.tables[table_name].join(client)

    def _list_tables(self):
        if not self.tables:
            return 'No tables created'
        formatted_table_list = '\nTables in the server:\n'
        for table_name in self.tables:
            formatted_table_list += str(self.tables[table_name]) + '\n'
        return formatted_table_list + '\n: '
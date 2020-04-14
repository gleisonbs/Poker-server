from unittest import TestCase
from unittest.mock import patch
from game.lobby import Lobby
from network.request import Request

class LobbyTest(TestCase):
    def test_create_table(self):
        request = Request('create_table:me:my table:2')

        lobby = Lobby()

        self.assertEqual(len(lobby.tables), 0)

        client = None
        lobby.handle_request(request, client)

        self.assertEqual(len(lobby.tables), 1)
        self.assertIn('my table', lobby.tables.keys())

    def test_create_same_name_table(self):
        request = Request('list_tables:me')

        lobby = Lobby()

        self.assertEqual(len(lobby.tables), 0)

        client = None
        lobby.handle_request(Request('create_table:me:my table:2'), client)
        result = lobby.handle_request(Request('create_table:me:my table:2'), client)

        self.assertEqual(result, 'table "my table" already exists')
        self.assertEqual(len(lobby.tables), 1)


    def test_list_tables_no_tables(self):

        lobby = Lobby()

        self.assertEqual(len(lobby.tables), 0)

        client = None
        result = lobby.handle_request(Request('list_tables:me'), client)

        self.assertEqual(result, 'No tables created')

    def test_list_tables(self):
        request = Request('list_tables:me')

        lobby = Lobby()
        lobby._create_table('Test table 1', 6)
        lobby._create_table('Test table 2', 9)

        client = None
        result = lobby.handle_request(Request('list_tables:me'), client)

        self.assertEqual(result, '\nTables in the server:\nTest table 1: 0/6\nTest table 2: 0/9\n\n: ')

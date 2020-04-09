from unittest import TestCase
from unittest.mock import patch
from network.server import Server

class ServerTest(TestCase):
    def test_create_table(self):
        server = Server()

        response = server.create_table('test table', 6)

        self.assertEqual(response, 'table test table was created\n: ')
        self.assertEqual(len(server.tables), 1)
        self.assertIn('test table', server.tables.keys())
        self.assertEqual(server.tables['test table'].name, 'test table')
        self.assertEqual(server.tables['test table'].max_players, 6)
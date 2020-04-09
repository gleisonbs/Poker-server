from unittest import TestCase
from unittest.mock import patch
from network.server import Server

class ServerTest(TestCase):
    def test_create_server(self):
        server = Server()

        self.assertEqual(len(server.tables), 0)
        self.assertEqual(len(server.players), 0)
        self.assertEqual(len(server.clients), 0)

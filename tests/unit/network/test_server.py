from unittest import TestCase
from unittest.mock import patch
from network.server import Server

class ServerTest(TestCase):
    def test_create_server(self):
        server = Server()
        self.assertEqual(len(server.connected_clients), 0)

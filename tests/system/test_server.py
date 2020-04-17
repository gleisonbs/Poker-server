from random import randint
from unittest import TestCase
from threading import Thread
import socket
from time import sleep

from network.server import Server

class ServerTest(TestCase):
    def wait_server(self):
        while not self.server.is_running:
            sleep(0.001)

    def setUp(self):
        self.server = Server({'DEBUG': True})
        port = randint(5600, 6600)
        self.server_thread = Thread(target=self.server.run, args=(port,))
        self.server_thread.start()

        self.wait_server()

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.settimeout(2)
        self.client_sock.connect(('127.0.0.1', port))

    def test_create_table(self):
        self.assertNotIn('my table', self.server.lobby.tables.keys())
        self.client_sock.send('create_table:me:my table:2'.encode())

        msg_from_server = self.client_sock.recv(4096)
        msg_from_server = msg_from_server.decode()

        self.assertEqual(msg_from_server, 'Table "my table" was created\n: ')
        self.assertIn('my table', self.server.lobby.tables.keys())

    def test_list_tables(self):
        self.client_sock.send('create_table:me:Test Table 1:2'.encode())
        self.client_sock.recv(1024)

        self.client_sock.send('create_table:me:Test Table 2:6'.encode())
        self.client_sock.recv(1024)

        self.client_sock.send('list_tables:me'.encode())
        msg_from_server = self.client_sock.recv(1024)
        msg_from_server = msg_from_server.decode()

        self.assertEqual(msg_from_server, '\nTables in the server:\nTest Table 1: 0/2\nTest Table 2: 0/6\n\n: ')
        self.assertIn('Test Table 1', self.server.lobby.tables.keys())
        self.assertIn('Test Table 2', self.server.lobby.tables.keys())

    def test_join_table(self):
        self.server.lobby._create_table('Test Table', 2)

        self.assertEqual(len(self.server.lobby.tables['Test Table'].players), 0)

        self.client_sock.send('join_table:me:Test Table'.encode())

        msg_from_server = self.client_sock.recv(1024)
        msg_from_server = msg_from_server.decode()

        self.assertEqual(len(self.server.lobby.tables['Test Table'].players), 1)

    def tearDown(self):
        self.client_sock.send('close'.encode())
        self.client_sock.close()
        self.server_thread.join()


from random import randint
from unittest import TestCase
from threading import Thread
import socket
from time import sleep

from network.server import Server

class ServerTest(TestCase):
    def setUp(self):
        self.server = Server({'DEBUG': True})
        port = randint(5600, 6600)
        self.server_thread = Thread(target=self.server.run, args=(port,))
        self.server_thread.start()

        sleep(1)
        
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(('127.0.0.1', port))

    def test_show_menu(self):
        # self.server = Server({'DEBUG': True})
        # port = 5641
        # t = Thread(target=server.run, args=(port,))
        # t.start()

        msg_from_server = self.client_sock.recv(4096)
        msg_from_server = msg_from_server.decode()

        self.assertEqual(msg_from_server, """
         /$$$$$$$           /$$                          
        | $$__  $$         | $$                          
        | $$  \ $$ /$$$$$$ | $$   /$$  /$$$$$$   /$$$$$$ 
        | $$$$$$$//$$__  $$| $$  /$$/ /$$__  $$ /$$__  $$
        | $$____/| $$  \ $$| $$$$$$/ | $$$$$$$$| $$  \__/
        | $$     | $$  | $$| $$_  $$ | $$_____/| $$      
        | $$     |  $$$$$$/| $$ \  $$|  $$$$$$$| $$      
        |__/      \______/ |__/  \__/ \_______/|__/      
        

        1. Join table
        2. Create table
        3. List tables

        : """)

    def test_create_table(self):
        self.client_sock.recv(4096)

        self.assertNotIn('my table', self.server.lobby.tables.keys())
        self.client_sock.send('create_table:me:my table:2'.encode())

        msg_from_server = self.client_sock.recv(4096)
        msg_from_server = msg_from_server.decode()

        self.assertEqual(msg_from_server, 'Table "my table" was created\n: ')
        self.assertIn('my table', self.server.lobby.tables.keys())

    def tearDown(self):
        self.client_sock.send('close'.encode())
        self.client_sock.close()
        self.server_thread.join()


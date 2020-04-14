from unittest import TestCase
from threading import Thread
import socket
from time import sleep

from network.server import Server

class ServerTest(TestCase):
    def setUp(self):
        server = Server({'DEBUG': True})
        port = 5641
        self.server_thread = Thread(target=server.run, args=(port,))
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

    def tearDown(self):
        self.client_sock.send('close'.encode())
        self.client_sock.close()
        self.server_thread.join()


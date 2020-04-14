import socket
from select import select


class Connection:
    def __init__(self, sock, conn_addr, is_server=False):
        self.socket = sock
        self.connection_address = conn_addr
        self.is_server = is_server

    def read_from_socket(self):
        readable_sockets, *_ = select([self.socket], [], [], 1)
        for _ in readable_sockets:
            if self.is_server:
                return self.accept()
            else:
                return self.recv()
        return None

    def accept(self):
        connection, connection_address = self.socket.accept()
        connection.setblocking(0)
        print(f'Connection from {connection_address}')
        
        return Connection(connection, connection_address)

    def recv(self):
        try:
            data = self.socket.recv(128)
            data = data.strip().decode()
            return data
        except:
            return None

    def send(self, data):
        self.socket.sendall(data.encode())

    def close(self):
        self.socket.close()
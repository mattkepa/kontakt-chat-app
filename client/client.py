import socket
from threading import Thread


class Client:
    """
    Represents client socket
    """
    HOST = '192.168.1.16'
    PORT = 9090
    ADDR = (HOST, PORT)
    BUFFSIZE = 1024

    def __init__(self, name):
        """
        Init client socket object and send user name to server
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.name = name
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)

    def receive_messages(self):
        """
        Receive messages from server
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFSIZE).decode('utf8')
                print(msg)
            except Exception as e:
                print(f'[ERROR] {e}')
                break

    def send_message(self, msg):
        """
        Send message to server
        """
        try:
            self.client_socket.send(bytes(msg, 'utf8'))
            if msg == '{quit}':
                self.client_socket.close()
        except Exception as e:
            print(f'[ERROR] {e}')


    def disconnect(self):
        self.send_message('{quit}')


if __name__ == '__main__':
    print(socket.gethostbyname(socket.gethostname()))
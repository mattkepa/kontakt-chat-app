import socket
from threading import Thread
from user import User


HOST = '192.168.1.16'
PORT = 9090
ADDR = (HOST, PORT)
BUFFSIZE = 1024

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


users = []


def broadcast(msg, name=''):
    """
    Broadcast message to all the clients.
    :param msg: bytes['utf8']
    :param name: str
    """
    for user in users:
        client = user.client
        try:
            client.send(bytes(name, 'utf8') + msg)
        except Exception as e:
            print(f'[ERROR] {e}')



def handle_client_communication(user):
    """
    Handles a single client connection.
    Thread to handle all messages form client
    :param user: User
    """
    client = user.client

    # Get persons name
    # first message recieved is always the persons name
    name = client.recv(BUFFSIZE).decode('utf8')
    user.set_name(name)

    # Broadcast user joined message
    msg = bytes(f'{name} has joined the chat.', 'utf8')
    broadcast(msg)

    while True:
        msg = client.recv(BUFFSIZE)
        if msg == bytes('{quit}', 'utf8'): # if message is command to disconnect
            broadcast(bytes(f'{name} has left the chat.', 'utf8'))
            client.close()
            users.remove(user)
            print(f'[DISCONNECT] {name} disconnected')
            break
        else:

            print(f'{name}: {msg.decode("utf8")}')
            broadcast(msg, name+': ')


def accept_incoming_connections():
    """
    Sets up handling for incoming clients.
    Wait for connection from new clients, starts new thread once connected
    """
    while True:
        try:
            client, client_addr = SERVER.accept()
            user = User(client_addr, client)
            users.append(user)
            print(f'[CONNECTION] {client_addr} connected to the server')
            Thread(target=handle_client_communication, args=(user,)).start()
        except Exception as e:
            print(f'[ERROR] {e}')
            break
    print('SERVER STOPPED')


if __name__ == '__main__':
    SERVER.listen()
    print('Server is running...')
    print('[STARTED] Waiting for connections...')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


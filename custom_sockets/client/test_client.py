from client import Client
import sys

try:
    username = sys.argv[1]
except IndexError as e:
    sys.exit('Error: name argument must be passed')

client_socket = Client(username)

while True:
    msg = input('')
    client_socket.send_message(msg)
    if msg == '{quit}':
        break


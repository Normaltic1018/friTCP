import socket
import os
import threading

def msg_recv(sock):
    while(True):
        print(sock.recv(65535).decode())

#wait client

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12344))
server_socket.listen(0)
client_socket, addr = server_socket.accept()

my_thread = threading.Thread(target=msg_recv, args=(client_socket,))
my_thread.start()

while(True):
    msg = input(": ")
    client_socket.send(msg.encode())


client_socket.close()

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12346))
server_socket.listen(0)
client_socket, addr = server_socket.accept()
while(True):
    data = client_socket.recv(65535)
    print(data.decode())
    msg = "Welcome Client!".encode()
    client_socket.send(msg)
    
    
client_socket.close()

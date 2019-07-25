import socket
import threading
import os

def msg_recv(sock):
	while(True):
		print(os.getpid())
		msg = "Welcome Client!".encode()
		sock.send(msg)
		data = sock.recv(65535).decode()
		print(data)
      
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(server_socket)
server_socket.bind(('127.0.0.1', 12346))
server_socket.listen(10)
while(True):
   client_socket, addr = server_socket.accept()
   print(client_socket)
   my_thread = threading.Thread(target=msg_recv, args=(client_socket,))
   my_thread.start()
    
    
client_socket.close()
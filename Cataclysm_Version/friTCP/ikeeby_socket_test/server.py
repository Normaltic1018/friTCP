import socket
import threading

def msg_recv(sock):
   while(True):

      data = sock.recv(65535).decode()
      print(data)
      #msg = "Welcome Client!".encode()
      #sock.send(msg)
      
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(server_socket)
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(server_socket2)
server_socket.bind(('127.0.0.1', 12346))
server_socket.listen(10)
while(True):
   client_socket, addr = server_socket.accept()
   print(client_socket)
   my_thread = threading.Thread(target=msg_recv, args=(client_socket,))
   my_thread.start()
    
    
client_socket.close()
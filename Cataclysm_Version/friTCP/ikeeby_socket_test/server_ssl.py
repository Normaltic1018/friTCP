import socket
import threading
import ssl

def msg_recv(sock):
   while(True):
      msg = "Welcome Client!".encode()
      sock.send(msg)
      data = sock.recv(65535).decode()
      print(data)

context = ssl.SSLContext()
#context = ssl.create_default_context()
context.load_cert_chain('server.pem', 'server.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:    
	sock.bind(('127.0.0.1', 12346))
	sock.listen(10)
	with context.wrap_socket(sock, server_side=True) as ssock:
		while(True):
		   client_socket, addr = ssock.accept()
		   print(client_socket)
		   my_thread = threading.Thread(target=msg_recv, args=(client_socket,))
		   my_thread.start()
		
    
client_socket.close()
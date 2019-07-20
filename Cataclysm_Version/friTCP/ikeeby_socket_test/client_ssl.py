import socket
import os
import time
import ssl

print(os.getpid())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wrappedSocket = ssl.wrap_socket(sock)
wrappedSocket.connect(('127.0.0.1', 12346))

while(True):
	msg = "Hello Server!1234567890123456789012345678901234567890".encode()
	wrappedSocket.send(msg)
	data = wrappedSocket.recv(65535)
	
	print(os.getpid())
	print(data.decode())
	time.sleep(1)

wrappedSocket.close()

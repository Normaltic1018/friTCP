import socket
import os
import time

print(os.getpid())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12346))

while(True):
    msg = "Hello Server!1234567890123456789012345678901234567890".encode()
    sock.send(msg)
    data = sock.recv(65535)
    print(data.decode())
    time.sleep(1)

sock.close()

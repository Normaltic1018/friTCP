import socket
import os
import time

#print os.getpid() 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12345))


# get gui.print_info()

print("1 "+sock.recv(65535).decode())
print("2 "+sock.recv(65535).decode())
print("3 "+sock.recv(65535).decode())

print("recv gui.print_info() end")

while(True):
# recv get_cmd

    print("4 "+sock.recv(65535).decode())

    # send cmd

    # mode = "proxy"
    # mode = "set capture_list send"

    mode = input(": ")

    if mode == "proxy": # not completed..
        msg = "proxy"
        sock.send(msg.encode())

        print("SEND END")

        print(sock.recv(65535).decode())
        print(sock.recv(65535).decode())
        print(sock.recv(65535).decode())
        print(sock.recv(65535).decode())

    elif mode.startswith("set"):

        msg = mode
        sock.send(msg.encode())
        print("SEND END")

        print(sock.recv(65535).decode())
        print(sock.recv(65535).decode())

sock.close()

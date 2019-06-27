import socket
import os
import threading
import json

def msg_recv(sock):
    while(True):
        data = sock.recv(65535).decode()
        #print(data)
        data = json.loads(data)
        #print(data)
        recv_handler(sock, data)

def recv_handler(sock, data):
    if(data["data"]["res"] == "success"):
        msg = '{"type":"response","data":{"service":"response","res":"success","message":"response success"}}'
        #print(msg)
        sock.send(msg.encode())
        print("SEND: "+msg)
    

#wait client

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(0)
client_socket, addr = server_socket.accept()

my_thread = threading.Thread(target=msg_recv, args=(client_socket,))
my_thread.start()

while(True):
    msg = input(": ")
    #msg = '{"type":"boot","data":{"service":"init","res":"success","message":"core init success"}'
    print(client_socket.recv().decode())
    client_socket.send(msg.encode())



client_socket.close()

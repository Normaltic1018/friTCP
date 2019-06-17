import socket
import time

class TCP_SOCKET:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 12345))
        self.server_socket.listen(0)
        self.client_socket, addr = self.server_socket.accept()
        
    def send(self,data):
        try:
            print("send: "+data)
            self.client_socket.send(data.encode())
            
            # sleep 안주면 한번에 두번 보내는 경우가 생김.. 동기화를 위해 필수!
            time.sleep(0.2)
        except Exception as e:
            self.client_socket.send(str(e).encode())

    def recv(self):
        try:
            data = self.client_socket.recv(65535).decode()
            print("recv: "+data)
            return data
        except Exception as e:
            return str(e)



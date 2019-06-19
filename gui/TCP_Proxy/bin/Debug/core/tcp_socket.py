import socket
import time

class TCP_SOCKET:
    def __init__(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', port))
        
    def send(self,data):
        try:
            print("send: "+data)
            self.sock.send(data.encode())
            
            # sleep 안주면 한번에 두번 보내는 경우가 생김.. 동기화를 위해 필수!
            time.sleep(0.2)
        except Exception as e:
            self.sock.send(str(e).encode())

    def recv(self):
        try:
            data = self.sock.recv(65535).decode()
            print("recv: "+data)
            return data
        except Exception as e:
            return str(e)



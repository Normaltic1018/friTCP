import socket
import time
import json

class TCP_SOCKET:
    def __init__(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', port))
        
    def send(self,data):
        try:
            print("send: "+data)
            self.sock.send(data.encode())
            
            # sleep 안주면 한번에 두번 보내는 경우가 생김.. 동기화를 위해 필수!
            time.sleep(1)
			
			
        except Exception as e:
            return str(e)

    def recv(self):
        try:
            data = self.sock.recv(65535).decode()

            print("recv: "+data)

            return data
        except Exception as e:
            return str(e)

    ### 동기화 - 수신여부를 검증함으로써 한 타이밍에 한번의 통신만 되도록 할 수 있음.
    ### 현재 비동기화 -> 한 타이밍에 여러 통신이 전달되어(다중 json) parsing 에러가 있으며,
    ### 동기화로 전환
    # 서버 수신여부 검증.			
    def send2(self,data):
        try:
            print("send: "+data)
            self.sock.send(data.encode())
            
            # sleep 안주면 한번에 두번 보내는 경우가 생김.. 동기화를 위해 필수!
            time.sleep(0.2)
            
            data = self.sock.recv(65535).decode()

            print("recv: "+data)			
			
        except Exception as e:
            return str(e)

    # 나의 수신여부 전송.
    def recv2(self):
        try:
            data = self.sock.recv(65535).decode()

            json_data = json.loads(data)
            result = json_data["data"]["res"]
            print("json result: result")

            #print("recv: "+data)
            return result
        except Exception as e:
            return str(e)
			

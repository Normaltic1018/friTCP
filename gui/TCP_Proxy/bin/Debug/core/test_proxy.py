import tcp_socket
import os
import threading
import psutil
import sys



cmd_sock = tcp_socket.TCP_SOCKET(12345)
proxy_sock = tcp_socket.TCP_SOCKET(12344)

ppid = os.getppid()
proxy_sock.send("ppid: "+str(ppid))

def clean_all(cmd_sock, proxy_sock):
	cmd_sock.close()
	proxy_sock.close()


def my_thread(cmd_sock, proxy_sock, ppid):
	try:
		print("ppid: "+str(ppid))
		while(True):
			print(psutil.pid_exists(ppid))
			if not psutil.pid_exists(ppid):
				break
		

		f1 = open("log.txt","w")
		f1.write("thread success exited!")
		f1.close()
		print("my_thread exit")
		clean_all(cmd_sock, proxy_sock)
		sys.exit()
	except(Exception,e):
		f1 = open("log.txt","w")
		f1.write(e)
		f1.close()
	
	
t1 = threading.Thread(target = my_thread, args=(cmd_sock, proxy_sock, ppid))
t1.start()


while(True):
        try:
                proxy_sock.send("hello GUI?")
        except:
                f1 = open("log.txt","w")
                f1.write("thread success exited!")
                f1.close()
                sys.exit()

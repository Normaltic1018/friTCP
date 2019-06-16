#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *
from tcp_socket import *

sock = TCP_SOCKET()

def print_info():
        print("1version:{}".format(version))
        sock.send("1version:{}".format(version))

        print("2[SETTING]:"+str(settings))
        sock.send("2[SETTING]:"+str(settings))

        print("3[SETTING]:"+str(commands))
        sock.send("3[SETTING]:"+str(commands))

def get_cmd():
	sock.send("[GET_CMD]")
	cmd = sock.recv()
	return cmd

def print_error(message):
	send_data = '{"type":"cmd","data":{"res":"fail","message":"%s"}}' % message
	print("print_error: "+send_data)
	sock.send(send_data)

def print_response(message):
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % message
	print("print_response: "+send_data)
	sock.send(send_data)


def print_current_settings():
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % "[SETTING]:"+str(settings)
	print("print_current_settings: "+send_data)
	sock.send(send_data)
def print_command():
	send_data = '{"type":"cmd","data":{"res":"success","message":%s}}' % "[COMMAND]:"+str(settings)
	print("print_command: "+send_data)
	sock.send(send_data)

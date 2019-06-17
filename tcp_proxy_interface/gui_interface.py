#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *
from tcp_socket import *

#sock = TCP_SOCKET()

def print_info():
	#print('{"type":"boot","data":{"version":"%s","settings":"%s","commands":"%s"}}' % (version, str(settings), str(commands)))
	
    #print("1version:{}".format(version))
    sock.send("1version:{}".format(version))

    #print("2[SETTING]:"+str(settings))
    sock.send("2[SETTING]:"+str(settings))

    #print("3[SETTING]:"+str(commands))
    sock.send("3[SETTING]:"+str(commands))
	

def get_cmd():
	sock.send("[GET_CMD]")
	#print("[GET_CMD]")
	
	#cmd = input()
	cmd = sock.recv()
	return cmd

def print_error(message):
	send_data = '{"type":"cmd","data":{"res":"fail","message":"%s"}}' % message
	#print("print_error: "+send_data)
	sock.send(send_data)

def print_response(message):
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % message
	#print("print_response: "+send_data)
	sock.send(send_data)


def print_current_settings():
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % ("[SETTING]:"+str(settings))
	#print("print_current_settings: "+send_data)
	sock.send(send_data)

def print_command():
	send_data = '{"type":"cmd","data":{"res":"success","message":%s}}' % ("[COMMAND]:"+str(settings))
	#print("print_command: "+send_data)
	sock.send(send_data)
	
def print_js_response(message,hex_data):
	if(message.startswith("[HEXDUMP]")):
		send_data = '{"type":"frida","data":{"res":"success","message":{"hex_dump":"%s"}}}' % (str(hex_data))
		print(send_data)
	elif(message.startswith("[frida_error]")):
		send_data = '{"type":"frida","data":{"res":"fail","message":{"error":"%s"}}}' % (str(hex_data))
		print(send_data)
	else:
		send_data = '{"type":"frida","data":{"res":"success","message":{"data":"%s"}}}' % (str(hex_data))
		print(send_data)

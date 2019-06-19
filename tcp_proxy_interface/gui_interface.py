#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *
from tcp_socket import *

console_mode = True

if(console_mode == False):
	sock = TCP_SOCKET()

def print_info():
	if(console_mode):
		print('{"type":"boot","data":{"version":"%s","settings":"%s","commands":"%s"}}' % (version, str(settings), str(commands)))
	else:
    #print("1version:{}".format(version))
		sock.send("1version:{}".format(version))

    #print("2[SETTING]:"+str(settings))
		sock.send("2[SETTING]:"+str(settings))

    #print("3[SETTING]:"+str(commands))
		sock.send("3[SETTING]:"+str(commands))
	

def get_cmd():
	if(console_mode):
		print("[GET_CMD]")
		cmd = input()
	else:
		sock.send("[GET_CMD]")
		cmd = sock.recv()
		
	return cmd

def print_error(message):
	send_data = '{"type":"cmd","data":{"res":"fail","message":"%s"}}' % message
	if(console_mode):
		print("print_error: "+send_data)
	else:
		sock.send(send_data)

def print_response(message):
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % message
	if(console_mode):
		print("print_response: "+send_data)
	else:
		sock.send(send_data)


def print_current_settings():
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % ("[SETTING]:"+str(settings))
	
	if(console_mode):
		print("print_current_settings: "+send_data)
	else:
		sock.send(send_data)

def print_command():
	send_data = '{"type":"cmd","data":{"res":"success","message":%s}}' % ("[COMMAND]:"+str(settings))
	
	if(console_mode):
		print("print_command: "+send_data)
	else:
		sock.send(send_data)

def input_data():
	if(console_mode):
		res = input("Data : ")
	else:
		# recv 로 바꿔주세요!
		res = input("Data : ")
		
	return res
	
def print_js_response(message,hex_data):
	if(console_mode):
		if(message.startswith("[HEXDUMP]")):
			send_data = '{"type":"frida","data":{"res":"success","message":{"hex_dump":"%s"}}}' % (str(hex_data))
			print(send_data)
		elif(message.startswith("[frida_error]")):
			send_data = '{"type":"frida","data":{"res":"fail","message":{"error":"%s"}}}' % (str(hex_data))
			print(send_data)
		else:
			send_data = '{"type":"frida","data":{"res":"success","message":{"data":"%s"}}}' % (str(hex_data))
			print(send_data)
	else:
		if(message.startswith("[HEXDUMP]")):
			send_data = '{"type":"frida","data":{"res":"success","message":{"hex_dump":"%s"}}}' % (str(hex_data))
			sock.send(send_data)
		elif(message.startswith("[frida_error]")):
			send_data = '{"type":"frida","data":{"res":"fail","message":{"error":"%s"}}}' % (str(hex_data))
			sock.send(send_data)
		else:
			send_data = '{"type":"frida","data":{"res":"success","message":{"data":"%s"}}}' % (str(hex_data))
			sock.send(send_data)

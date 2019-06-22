#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *
from tcp_socket import *

console_mode = False

if(console_mode == False):
	cmd_sock = TCP_SOCKET(12345)
	proxy_sock = TCP_SOCKET(12344)

def print_info():
	if(console_mode):
		print('{"type":"boot","data":{"version":"%s","settings":"%s","commands":"%s"}}' % (version, str(settings), str(commands)))
	else:
    #print("1version:{}".format(version))
		cmd_sock.send("1version:{}".format(version))

    #print("2[SETTING]:"+str(settings))
		cmd_sock.send("2[SETTING]:"+str(settings))

    #print("3[SETTING]:"+str(commands))
		cmd_sock.send("3[SETTING]:"+str(commands))
	

def get_cmd():
	if(console_mode):
		print("[GET_CMD]")
		cmd = input()
	else:
		cmd_sock.send("[GET_CMD]")
		cmd = cmd_sock.recv()
		
	return cmd

def print_error(message):
	send_data = '{"type":"cmd","data":{"res":"fail","message":"%s"}}' % message
	if(console_mode):
		print("print_error: "+send_data)
	else:
		cmd_sock.send(send_data)

def print_response(message):
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % message
	if(console_mode):
		print("print_response: "+send_data)
	else:
		cmd_sock.send(send_data)


def print_current_settings():
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % ("[SETTING]:"+str(settings))
	
	if(console_mode):
		print("print_current_settings: "+send_data)
	else:
		cmd_sock.send(send_data)

def print_command():
	send_data = '{"type":"cmd","data":{"res":"success","message":%s}}' % ("[COMMAND]:"+str(settings))
	
	if(console_mode):
		print("print_command: "+send_data)
	else:
		cmd_sock.send(send_data)

def input_data():
	if(console_mode):
		res = input("Data : ")
	else:
		# recv 로 바꿔주세요!
		res = input("Data : ")
		
	return res
	
def print_js_response(message,proxy_info,hex_data):
	if(console_mode):
		if(message.startswith("[PROXY]")):
			send_data = '{"type":"frida","data":{"service":"proxy","res":"success","message":{"IP":"%s","PORT":"%s","hex_dump":"%s"}}}' % (proxy_info[0],proxy_info[1],str(hex_data))
			print(send_data)
		elif(message.startswith("[HOOK_INFO]")):
			send_data = '{"type":"frida","data":{"service":"hook_info","res":"success","message":{"PID":"%s","MODULE":"%s","FUNCTION":"%s","ADDRESS":"%s"}}}' % (proxy_info[0],proxy_info[1],proxy_info[2],proxy_info[3])
			print(send_data)		
		elif(message.startswith("[HEXDUMP]")):
			send_data = '{"type":"frida","data":{"service":"hexdump","res":"success","message":{"hex_dump":"%s"}}}' % (str(hex_data))
			print(send_data)
		elif(message.startswith("[frida_error]")):
			send_data = '{"type":"frida","data":{"service":"frida_error","res":"fail","message":{"error":"%s"}}}' % proxy_info
			print(send_data)
		else:
			send_data = '{"type":"frida","data":{"service":"else","res":"success","message":{"data":"%s"}}}' % (str(hex_data))
			print(send_data)
	else:
		if(message.startswith("[PROXY]")):
			send_data = '{"type":"frida","data":{"service":"proxy","res":"success","message":{"IP":"%s","PORT":"%s","hex_dump":"%s"}}}' % (proxy_info[0],proxy_info[1],str(hex_data))
			proxy_sock.send(send_data)
		elif(message.startswith("[HOOK_INFO]")):
			send_data = '{"type":"frida","data":{"service":"hook_info","res":"success","message":{"PID":"%s","MODULE":"%s","FUNCTION":"%s","ADDRESS":"%s"}}}' % (proxy_info[0],proxy_info[1],proxy_info[2],proxy_info[3])
			proxy_sock.send(send_data)	
		elif(message.startswith("[HEXDUMP]")):
			send_data = '{"type":"frida","data":{"service":"hexdump","res":"success","message":{"hex_dump":"%s"}}}' % (str(hex_data))
			proxy_sock.send(send_data)
		elif(message.startswith("[frida_error]")):
			send_data = '{"type":"frida","data":{"service":"frida_error","res":"fail","message":{"error":"%s"}}}' % proxy_info
			proxy_sock.send(send_data)
		else:
			send_data = '{"type":"frida","data":{"service":"else","res":"success","message":{"data":"%s"}}}' % (str(hex_data))
			proxy_sock.send(send_data)

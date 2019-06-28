#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *
from tcp_socket import *

console_mode = False
count = 0
if(console_mode == False):
	cmd_sock = TCP_SOCKET(12345)
	proxy_sock = TCP_SOCKET(12344)

def print_info():
	print("print_info called")
	send_data = '{"type":"boot","data":{"service":"init","res":"success","message":"core init success"}}'
	cmd_send_out(send_data)
	
	#print('{"type":"boot","data":{"version":"%s","settings":"%s","commands":"%s"}}' % (version, str(settings), str(commands)))
                
def get_cmd():
	print("get_cmd called")
	if(console_mode):
		print("[GET_CMD]")
		cmd = input()
	else:
		cmd_send_out("[GET_CMD]")
		cmd = cmd_sock.recv()
		
	return cmd

def print_error(message):
	print("print_error called")
	send_data = '{"type":"cmd","data":{"res":"fail","message":"%s"}}' % message
	cmd_send_out(send_data)

def print_response(message):
	print("print_response called")
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % message
	cmd_send_out(send_data)


def print_current_settings():
	print("print_current_settings called")
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % ("[SETTING]:"+str(settings))
	cmd_send_out(send_data)

def print_command():
	print("print_command called")
	send_data = '{"type":"cmd","data":{"res":"success","message":%s}}' % ("[COMMAND]:"+str(settings))
	cmd_send_out(send_data)

def input_data():
	print("input_data called")
	if(console_mode):
		res = input("Data : ")
	else:
		# recv 로 바꿔주세요!
		res = proxy_sock.recv()
		
	return res
	
def print_js_response(message,proxy_info,hex_data):
	print("print_js_response called")
	# cmd_send_out과 buf_send_out은 추후 프로토콜 정하면서 구분할 것.
	if(message.startswith("[PROXY]")):
		send_data = '{"type":"frida","data":{"service":"proxy","res":"success","message":{"INTERCEPT":"%s","IP":"%s","PORT":"%s","hex_dump":"%s"}}}' % (proxy_info[0],proxy_info[1],proxy_info[2],str(hex_data))
		buff_send_out(send_data)
	elif(message.startswith("[HOOK_INFO]")):
		send_data = '{"type":"frida","data":{"service":"hook_info","res":"success","message":{"PID":"%s","MODULE":"%s","FUNCTION":"%s","ADDRESS":"%s"}}}' % (proxy_info[0],proxy_info[1],proxy_info[2],proxy_info[3])
		buff_send_out(send_data)		
	elif(message.startswith("[frida_error]")):
		send_data = '{"type":"frida","data":{"service":"frida_error","res":"fail","message":{"error":"%s"}}}' % proxy_info
		buff_send_out(send_data)
	elif(message.startswith("[frida_response]")):
		send_data = '{"type":"frida","data":{"service":"frida_response","res":"?","message":{"proxy_info":"%s"}}}' % proxy_info
		buff_send_out(send_data)		
	else:
		send_data = '{"type":"frida","data":{"service":"else","res":"success","message":{"data":"%s"}}}' % (str(hex_data))
		buff_send_out(send_data)


def cmd_send_out(send_data):
	print("cmd_send_out called")
	if(console_mode):
		print(send_data)
	else:
		cmd_sock.send(send_data)
		
def buff_send_out(send_data):
	global count
	count = count + 1
	print("count: "+str(count))
	print("buff_send_out!: "+send_data)
	if(console_mode):
		print(send_data)
	else:
		proxy_sock.send(send_data)
		#proxy_sock.recv()

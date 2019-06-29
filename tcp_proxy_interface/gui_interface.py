#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *
from tcp_socket import *
import json
import time

console_mode = True

cmd_channel =1
proxy_channel = 2

sendable = True

if(console_mode == False):
	cmd_sock = TCP_SOCKET(12345)
	proxy_sock = TCP_SOCKET(12344)

def print_info():
	send_data = '{"type":"boot","data":{"service":"init","res":"success","message":"core init success"}}'
	data = {}
	data["process"] = "core_boot"
	data["res"] = "success"
	
	send_message_channel("init_process",data,cmd_channel)
	
def get_cmd():
	if(console_mode):
		print("[GET_CMD]")
		cmd = input()
	else:
		#cmd_sock.send("[GET_CMD]")
		cmd = cmd_sock.recv()
		
	return cmd

def print_error(message):
	send_data = '{"type":"boot","data":{"service":"init","res":"success","message":"core init success"}}'
	data = {}
	data["process"] = "core_boot"
	data["res"] = "fail"
	data["err"] = message
	
	send_message_channel("init_process",data,cmd_channel)

def cmd_response(process,res,message):
	#send_data = '{"type":"cmd","data":{"service":"init","res":"success","message":"core init success"}}'
	data = {}
	data["process"] = process
	data["res"] = res
	if(res == "fail"):
		data["err"] = message
	else:
		data["res_data"] = message
	
	send_message_channel("cmd",data,cmd_channel)

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
		res = proxy_sock.recv()
		
	return res
	
def print_js_response(message,proxy_info,hex_data):
	
	# cmd_send_out과 buf_send_out은 추후 프로토콜 정하면서 구분할 것.
	if(message.startswith("[PROXY]")):
		data = {}
		data["process"] = "proxy"
		data["res"] = "success"
		message = {}
		message["INTERCEPT"] = proxy_info[0]
		message["IP"] = proxy_info[1]
		message["PORT"] = proxy_info[2]
		message["hex_dump"] = str(hex_data)
		data["message"] = message
		
		send_message_channel("tcp_proxy",data,proxy_channel)
	
	elif(message.startswith("[frida_error]")):
		data = {}
		data["process"] = proxy_info[0]
		data["res"] = "fail"
		data["err"] = hex_data
		
		send_message_channel("exception",data,proxy_channel)
		send_data = '{"type":"frida","data":{"service":"frida_error","res":"fail","message":{"error":"%s"}}}' % proxy_info
		buff_send_out(send_data)	
	else:
		send_data = '{"type":"frida","data":{"service":"else","res":"success","message":{"data":"%s"}}}' % (str(hex_data))
		buff_send_out(send_data)

def send_message_channel(type,data,channel):
	send_data = {}
	send_data["type"] = type
	send_data["data"] = data
	
	send_data = json.dumps(send_data)
	
	if(channel == cmd_channel):
		cmd_send_out(send_data)
	else:
		buff_send_out(send_data)

def cmd_send_out(send_data):
	if(console_mode):
		print(send_data)
	else:
		cmd_sock.send(send_data)
		
def buff_send_out(send_data):
	if(console_mode):
		print(send_data)
	else:
		proxy_sock.send(send_data)
		while True:
			res = proxy_sock.recv()
			if(res == "[ACK]"):
				break
		
		
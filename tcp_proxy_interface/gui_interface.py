#For GUI interface
# tcp socket 으로 print, input 들 다 바꿀꺼
from tcp_proxy_core.tcp_proxy_config import *

def print_info():
	print("version:{}".format(version))
	print("[SETTING]:"+str(settings))
	print("[SETTING]:"+str(commands))

def get_cmd():
	print("[GET_CMD]")
	cmd = input()
	return cmd

def print_error(message):
	send_data = '{"type":"cmd","data":{"res":"fail","message":"%s"}}' % message
	print(send_data)
	
def print_response(message):
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % message
	print(send_data)
	
	
def print_current_settings():
	send_data = '{"type":"cmd","data":{"res":"success","message":"%s"}}' % "[SETTING]:"+str(settings)
	print(send_data)

def print_command():
	send_data = '{"type":"cmd","data":{"res":"success","message":%s}}' % "[COMMAND]:"+str(settings)
	print(send_data)

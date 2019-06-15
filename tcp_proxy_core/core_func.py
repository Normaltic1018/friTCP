# core Function Library
from tcp_proxy_interface import gui_interface as gui
from tcp_proxy_core.tcp_proxy_config import *

def get_script(script_name):
	with open('js_script\\'+script_name, 'r') as f:
		script = f.read()
	return script

def validate_setting(mode, value):
	if value in settings_validation[mode]:
		return True

	return False

def set_cmd(cmd):
	cmd = cmd.split()
	if len(cmd) > 1 :
		if cmd[1] in settings:
			if cmd[1] == "capture_list":
				list_num = len(cmd) - 2
				new_api_list = []
				for i in range(list_num):
					if(validate_setting(cmd[1], cmd[2+i])):
						new_api_list.append(cmd[2+i])
					else:
						gui.print_error("\"{}\" is not API Name".format(cmd[2+i]))
						
				if len(new_api_list) != 0:
					settings[cmd[1]] = new_api_list
					gui.print_response("NOT_CHANGED")
					gui.print_current_settings()
					#dev.show_current_settings()
				else:
					print("#>Not Changed...")
			else:
				if(validate_setting(cmd[1],cmd[2])):
					settings[cmd[1]] = cmd[2]
					gui.print_response("CHANGE")
					gui.print_current_settings()
					#dev.show_current_settings()
				else:
					gui.print_error("WRONG_VALUE")
		else:
			gui.print_error("WRONG_SET_CMD")
			#dev.show_settings()
	else:
		gui.print_error("WRONG_CMD_ARG")

def hook_api(session,capture_api):
	global script
	script = session.create_script(get_script('func_proxy.js') % (capture_api, settings["mode"]))
	script.on('message', on_input_message)
	script.load()

		
def on_message(message, data):
	if message['type'] == 'send':
		print(message['payload'])
	elif message['type'] == 'error':
		print(message['stack'])
		
def on_input_message(message, data):
	print(message)
	if message['type'] == 'send':
		if(message['payload'] == "interactive"):
			user_input = input("Data : ")
			script.post({'type':'input','payload':user_input})
		else:
			print(message['payload'])
	elif message['type'] == 'error':
		print(message['stack'])
		
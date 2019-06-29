# core Function Library
from tcp_proxy_interface import gui_interface as gui
from tcp_proxy_core.tcp_proxy_config import *
import os

def get_script(script_name):
	with open(js_path+script_name, 'r') as f:
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
                                        gui.print_response("#>Not Changed...")
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
	
	if(settings["intercept"] == "on"):
		intercept = True
	else:
		intercept = False
	#gui.print_current_settings()

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
	#print(message)
	if message['type'] == 'send':
		if(message['payload'] == "interactive"):
			user_input = gui.input_data()
			if(settings["mode"] == "hex"):
				if(validate_hex_input(user_input) == False):
					gui.print_js_response("[frida_error]",["NOT HEX VALUE"],"")
					user_input = ""
			script.post({'type':'input','payload':user_input})
		elif(message['payload'] == "[intercept_on/off]"):
			script.post({'type':'intercept','payload':settings["intercept"]})
			#print("Intercept Check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		elif(message['payload'].startswith("[HOOK_INFO]")):
			hook_info = parsing_hook_info(message['payload'])
			#gui.print_js_response("[HOOK_INFO]", hook_info, [])
		elif(message['payload'].startswith("[GET_MODE]")):
			script.post({'type':'input','payload':settings["mode"]})
		elif(message['payload'].startswith("[PROXY]")):
			parsing_info_data = parsing_info(message['payload'])
			parsing_hex_data = parsing_hex(message['payload'])
			gui.print_js_response("[PROXY]", parsing_info_data, parsing_hex_data)\
	elif message['type'] == 'error':
		gui.print_js_response("[frida_error]",['proxy'],message['stack'])
		#print(message['stack'])

def parsing_hex(hexdump):
	hexdata = hexdump.split("[HEXDUMP]")[1].split()

	hex_len = int(hexdata[0])
	start_address = int(hexdata[1],16)

	hex_list = []
	
	for i in range(hex_len):
		indexing = format(start_address + (int(i/16)*16),'x').zfill(8)
	
		start_index = hexdata.index(indexing)
		hex_list.append(hexdata[start_index+1+(i%16)])

	return hex_list

def parsing_info(data):
	intercept_mode = data.split("[INTERCEPT]")[1].split()[0]
	ip_info = data.split("[IP]")[1].split()[0]
	port_info = data.split("[PORT]")[1].split()[0]

	return [intercept_mode, ip_info, port_info]

def parsing_hook_info(data):
	hook_pid = data.split("[PID]")[1].split()[0]
	hook_module = data.split("[MODULE]")[1].split()[0]
	hook_function = data.split("[FUNCTION]")[1].split()[0]
	hook_address = data.split("[ADDRESS]")[1].split()[0]
	
	return hook_pid, hook_module, hook_function, hook_address
	
def validate_hex_input(hex_data):
	hex_data = hex_data.split()
	
	for hex in hex_data:
		try:
			res = int(hex,16)
		except:
			return False
			
	return True
		
# core Function Library
from tcp_proxy_interface import gui_interface as gui
from tcp_proxy_core.tcp_proxy_config import *

def get_script(script_name):
	with open('js_script\\'+script_name, 'r') as f:
		script = f.read()
	return script

def validate_setting(mode, value):
	if value in settings_validation[mode]:
                print("true")
                return True

	print("false")
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
			script.post({'type':'input','payload':user_input})
		elif(message['payload'].startswith("[HEXDUMP]")):
			#print("Parsing Process")
			parsing_data = parsing_hexdata(message['payload'])
			gui.print_js_response("[HEXDUMP]",parsing_data)
		else:
			gui.print_js_response("[frida_response]",message['payload'])
	elif message['type'] == 'error':
		gui.print_js_response("[frida_error]",message['stack'])
		#print(message['stack'])

def parsing_hexdata(hexdump):
	hexdata = hexdump.split("[HEXDUMP]")[1].split()

	start_address = int(hexdata[0],16)

	hex_list = []
	for i in range(4):
		indexing = format(start_address + (i*16),'x').zfill(8)
		
		start_index = hexdata.index(indexing)

		for hex_byte in hexdata[start_index+1:start_index+1+16]:
			hex_list.append(hex_byte)

	return hex_list




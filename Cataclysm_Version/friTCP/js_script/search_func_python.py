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

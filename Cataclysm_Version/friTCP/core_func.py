#core.py
import psutil
import frida
import sys, os
from core.tcp_proxy_config import *
from PyQt5.QtCore import QObject, pyqtSignal

def get_process_list():
	process_list = []

	for proc in psutil.process_iter():
		processName = proc.name()
		processID = proc.pid
		
		process_list.append((processID,processName))
		
	return process_list

def get_script(script_name):
	try:
		with open(js_path+script_name, 'r') as f:
			script = f.read()
	except Exception as e:
		return ""
	return script

def parsing_info(data):
	func_name = data.split("[FUNC_NAME]")[1].split()[0]
	ip_info = data.split("[IP]")[1].split()[0]
	port_info = data.split("[PORT]")[1].split()[0]

	return func_name, ip_info, port_info

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
	
class FridaAgent(QObject):
	from_agent_data = pyqtSignal(str)
	def __init__(self, pid, gui_window,parent=None):
		super(FridaAgent, self).__init__(parent)
		self.pid = int(pid)
		self.session = frida.attach(self.pid)
		self.gui_window = gui_window
		self.hook_list = ["send"]
		self.intercept_on = True
		self.script_list = {}
		self.current_isIntercept = False
		
		
		for func in self.hook_list:
			self.inject_script(func)
		
	def inject_script(self,function_name):
		global script
		script_name = "{}_proxy.js".format(function_name)
	
		script = get_script(script_name)
		
		if(script == ""):
			return False
		
		script = self.session.create_script(script)
		#script.on('message', self.gui_window.from_fridaJS)
		script.on('message', self.on_message)
		script.load()
		self.script_list[function_name] = script
				
	def send_spoofData(self, hexList):
		
		strHex = ""
		for hex in hexList:
			strHex += hex + " "
		
		self.script_list['send'].post({'type':'input','payload':strHex})
		self.current_isIntercept = False
		
	
	def on_message(self,message, data):
		while self.current_isIntercept == True:
			pass
			
		self.from_agent_data.emit(message['payload'])
	
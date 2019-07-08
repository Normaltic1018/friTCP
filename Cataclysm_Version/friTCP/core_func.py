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

def parsing_pid(data):
	return data.split("[PID]")[1].split()[0]

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

def hexDump2Str(hex_list):
	hex_text =""
	str_text = ""
	for hex in hex_list:
		hex_text += hex + " "
		str_text += chr(int(hex,16)) + " "

	return hex_text, str_text
	
def get_process_name(pid):
	p = psutil.Process(int(pid))
	return p.name()
	
class FridaAgent(QObject):
	from_agent_data = pyqtSignal(str)
	error_signal = pyqtSignal(str)
	
	def __init__(self, gui_window,parent=None):
		super(FridaAgent, self).__init__(parent)
		
		self.session_list = {}
		self.gui_window = gui_window
		self.hook_list = ["send"]
		self.intercept_on = True
		self.script_list = {}
		self.current_isIntercept = False
		self.proxy_history = []
		
	def inject_frida_agent(self, pid):
		int_pid = int(pid)
		
		try:
			self.session_list[pid] = frida.attach(int_pid)
			#session = frida.attach(int_pid)
		except Exception:
			self.error_signal.emit("Can not Inject frida agent dll")

		
	def inject_script(self,pid):
		
		for func in self.hook_list:
			self.script_load(pid,func)
			
	def script_load(self,pid,function_name):
		session = self.session_list[pid]

		script_name = "{}_proxy.js".format(function_name)
	
		script = get_script(script_name)
		
		if(script == ""):
			return False
		
		script = session.create_script(script)
		#script.on('message', self.gui_window.from_fridaJS)
		script.on('message', self.on_message)
		script.load()
		self.script_list[pid] = {function_name:script}
	
	def reload_script(self, function_name):
		#unload_script
		self.script_list[function_name].unload()
		
		self.inject_script(function_name)
	
	def send_spoofData(self, intercept_pid,hexList):
		
		strHex = ""
		if(len(hexList)>0):
			
			for hex in hexList:
				strHex += hex + " "
		
		self.script_list[intercept_pid]['send'].post({'type':'input','payload':strHex})
		# 만약 op.wait 에서 멈추는 문제가 계속 발생한다면 여기서 체크하고 멈췄으면 reload 하는 코드를 넣을 것. 
		self.current_isIntercept = False
		
	
	def on_message(self,message, data):
		while self.current_isIntercept == True:
			pass
			
		self.from_agent_data.emit(message['payload'])
	
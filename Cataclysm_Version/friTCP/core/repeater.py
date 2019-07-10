#core.py
import psutil
import frida
import sys, os
from core.tcp_proxy_config import *
from PyQt5.QtCore import QObject, pyqtSignal

class Repeater(QObject):
	def __init__(self, gui_window,parent=None):
		super(FridaAgent, self).__init__(parent)
		
		self.socket_list = []
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
		
		if message['type'] == 'send':
			self.from_agent_data.emit(message['payload'])
		elif message['type'] == 'error':
			self.error_signal.emit(message['stack'])
		
	
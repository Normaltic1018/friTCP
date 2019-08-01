#core.py
import psutil
import frida
import sys, os, time, queue
from core.tcp_proxy_config import *
from PyQt5.QtCore import QObject, pyqtSignal
import threading
from Queue_Monitor import *

def get_process_list():
	print("get_process_list called!")
	process_list = []

	for proc in psutil.process_iter():
		processName = proc.name()
		processID = proc.pid
		
		process_list.append((processID,processName))
		
	return process_list

def get_script(script_name):
	print("get_script called!")
	try:
		with open(js_path+script_name, 'r') as f:
			script = f.read()
	except Exception as e:
		return ""
	return script

def parsing_info(data):
	print("parsing_info called!")
	func_name = data.split("[FUNC_NAME]")[1].split()[0]
	ip_info = data.split("[IP]")[1].split()[0]
	port_info = data.split("[PORT]")[1].split()[0]

	return func_name, ip_info, port_info

def parsing_func(data):
	print("parsing_func called!")
	return data.split("[FUNC_NAME]")[1].split()[0]

def parsing_pid(data):
	print("parsing_pid called!")
	return data.split("[PID]")[1].split()[0]

def parsing_threadId(data):
	print("parsing_threadId called!")
	return data.split("[THREAD_ID]")[1].split()[0]
	
def parsing_hex(hexdump):
	print("parsing_hex called!")
	hexdata = hexdump.split("[HEXDUMP]")[1].split()

	hex_len = int(hexdata[0])
	hex_list = []
	if(hex_len > 0):
		start_address = int(hexdata[1],16)
		
		for i in range(hex_len):
			indexing = format(start_address + (int(i/16)*16),'x').zfill(8)
		
			start_index = hexdata.index(indexing)
			hex_list.append(hexdata[start_index+1+(i%16)])

	return hex_list

def hexDump2Str(hex_list):
	print("hexDump2Str called!")
	hex_text =""
	str_text = ""
	for hex in hex_list:
		hex_text += hex + " "
		str_text += chr(int(hex,16))

	return hex_text, str_text
	
def get_process_name(pid):
	print("get_process_name called!")
	p = psutil.Process(int(pid))
	return p.name()
	
class FridaAgent(QObject):

	from_agent_data = pyqtSignal(str)
	error_signal = pyqtSignal(str)
	queue_get_signal = pyqtSignal(str)
	
	def __init__(self, gui_window,parent=None):
		print("FridaAgent __init__ called!")
		super(FridaAgent, self).__init__(parent)
		
		self.session_list = {}
		self.gui_window = gui_window
		self.hook_list = ["send","recv"]
		self.intercept_on = True
		self.script_list = {}
		self.current_isIntercept = False
		self.proxy_history = []
		self.thread_queue = queue.Queue()
		#monitor_thread = threading.Thread(target=self.monitor_queue)
		#monitor_thread.start()
		self.queue_monitor = Queue_Monitor(self)
	
	def init_fridaAgent(self):
		print("REFRESH %!%!%!%!%!%!%!%!%!%%!%!")
		for pid in self.session_list:
			self.session_list[pid].detach()
			self.current_isIntercept = False
			self.script_list = {}
			self.thread_queue = queue.Queue()
			
			self.session_list[pid] = frida.attach(int(pid))
			self.script_list[pid] = {}
			self.inject_script(pid)
			
			
	# 프로세스를 실행시키고 frida를 inject한 후 resume 그리고 pid를 return 함.
	def start_process(self,cmd, args):
		print("FridaAgent start_process called!")
		#cmd = "C:\\Users\\A0502571\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe"	# using sysnative to force x64 process
		#args = [ cmd, "C:\\Users\A0502571\\Desktop\\private\\2019.07.15\\friTCP\\Cataclysm_Version\\friTCP\\ikeeby_socket_test\\client.py" ]

		cmd_args = [cmd, args]
		int_pid = frida.spawn(cmd_args)
		pid = str(int_pid)
		self.session_list[pid] = frida.attach(int_pid)
		
		self.script_list[pid] = {}
		self.inject_script(pid)
		frida.resume(int_pid)
		
		return pid
	
	def resume_process(self, pid):
		print("FridaAgent resume_process called!")
		frida.resume(pid)
	
	def inject_frida_agent(self, pid):
		print("FridaAgent inject_frida_agent called!")
		int_pid = int(pid)
		
		try:
			self.session_list[pid] = frida.attach(int_pid)
			self.script_list[pid] = {}
			#session = frida.attach(int_pid)
		except Exception:
			self.error_signal.emit("Can not Inject frida agent dll")

		
	def inject_script(self,pid):
		print("FridaAgent inject_script called!")		
		for func in self.hook_list:
			self.script_load(pid,func)
			
	def script_load(self,pid,function_name):
		print("FridaAgent script_load called!")		
		session = self.session_list[pid]

		script_name = "{}_proxy.js".format(function_name)
		
		script = get_script(script_name)
		
		if(script == ""):
			return False
		
		script = session.create_script(script)
		self.script_list[pid].update({function_name:script})
		
		#script.on('message', self.gui_window.from_fridaJS)
		script.on('message', self.on_message)
		script.load()
		
	
	def reload_script(self, function_name):
		print("FridaAgent reload_script called!")	
		#unload_script
		self.script_list[function_name].unload()
		
		self.inject_script(function_name)
	
	def continue_script(self):
		if(self.thread_queue.empty() == False):
			print("GET_THEAD_QUEUE~~~~~")
			try:
				data = self.thread_queue.get_nowait()
				intercept_pid = data["pid"]
				func_name = data["func"]
				thread_id = data["thread_id"]
				
				print("CONTINUE script Thread : {} / func_name : {}".format(thread_id,func_name))
				self.current_isIntercept = True
				self.script_list[intercept_pid][func_name].post({'type':thread_id,'payload':'continue'})
			except:
				print("ERROR RAISE EMPTY QUEUE")
		else:
			print("EMPTY QUEUE @@@")
		
	def send_spoofData(self, intercept_pid,func_name,hexList):
		print("send_spoofData called!")
		
		strHex = ""
		if(len(hexList)>0):
			
			for hex in hexList:
				strHex += hex + " "
		

		print("Send GOGO!")
		self.script_list[intercept_pid][func_name].post({'type':'input','payload':strHex})
		print("Send GOGO Complete!")
		# 만약 op.wait 에서 멈추는 문제가 계속 발생한다면 여기서 체크하고 멈췄으면 reload 하는 코드를 넣을 것.
		
		#self.current_isIntercept = False

		#self.continue_script()
		
		"""
		if(self.thread_queue.empty() == False):
			self.continue_script()
		else:
			print("CLOSE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			self.current_isIntercept = False
		"""
		#print(self.thread_queue.empty())
		#self.continue_script()
		#print("Send Finished")
		
	def on_message(self,message, data):
		print("FridaAgent on_message called!")
		
		if message['type'] == 'send':
			if(message['payload'].startswith('[KNOCK]')):
				knock_pid = parsing_pid(message['payload'])
				knock_func = parsing_func(message['payload'])
				knock_threadId = parsing_threadId(message['payload'])
				
				queue_data = {"pid":knock_pid,"func":knock_func,"thread_id":knock_threadId}
				self.thread_queue.put_nowait(queue_data)
				#print("Q SIZE !! : {}".format(self.thread_queue.qsize()))
				if(self.current_isIntercept == False):
					self.continue_script()
				"""
				if(self.current_isIntercept == True):
					# insert queue
					print("Add Queue")
					self.thread_queue.put_nowait(queue_data)
				else:
					# insert queue and call continue_script
					self.thread_queue.put_nowait(queue_data)
					self.continue_script()
					"""
			elif(message['payload'].startswith('[END]')):
				knock_pid = parsing_pid(message['payload'])
				self.current_isIntercept = False
				self.queue_get_signal.emit("END")
			else:
				self.from_agent_data.emit(message['payload'])
			#self.current_isIntercept = True
		elif message['type'] == 'error':
			self.error_signal.emit(message['stack'])
		
	
	def hook_js(self, func_name):
		print("FridaAgent hook_js called!")
		for pid in self.session_list:
			session = self.session_list[pid]

			script_name = "{}_proxy.js".format(func_name)
			
			script = get_script(script_name)
			
			if(script == ""):
				return False
			
			script = session.create_script(script)
			self.script_list[pid].update({func_name:script})
			self.hook_list.append(func_name)
			
			script.on('message', self.on_message)
			script.load()
			self.gui_window.ui.textBrowser_log.append("[+] [PID:{}] Hook {} Function".format(pid,func_name))
	
	def unhook_js(self,func_name):
		print("FridaAgent unhook_js called!")
		for pid in self.session_list:
			session = self.session_list[pid]

			self.script_list[pid][func_name].unload()
			self.hook_list.remove(func_name)
			self.gui_window.ui.textBrowser_log.append("[-] [PID:{}] UnHook {} Function".format(pid,func_name))
			
				
#Queue_Monitor.py
import psutil
import frida
import sys, os, time, queue
from PyQt5.QtCore import QObject, pyqtSignal,pyqtSlot

class Queue_Monitor(QObject):
	
	def __init__(self,frida_agent,parent=None):
		print("Queue_Monitor __init__ called!")
		super(Queue_Monitor, self).__init__(parent)
		self.frida_agent = frida_agent
		self.make_connection_signal(self.frida_agent)
		
		
	def make_connection_signal(self, class_object):
		print("Queue_Monitor make_connection_signal called!")
		class_object.queue_get_signal.connect(self.queue_get)
		
	@pyqtSlot(str)	
	def queue_get(self,data):
		print("Queue_Monitor queue_get called!")
		self.frida_agent.continue_script()
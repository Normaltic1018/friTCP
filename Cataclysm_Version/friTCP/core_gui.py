# core_gui.py
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox,QLineEdit,QAbstractItemView, QAction, QMenu
from PyQt5.QtGui import QStandardItemModel,QStandardItem, QPixmap,QIcon, QRegExpValidator, QCursor
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal, pyqtSlot
from core_func import *
import ast
import socket
import frida
from Match_and_Replace import *

Ui_MainWindow, QtBaseClass = uic.loadUiType("main_window.ui")
hook_alert_Ui_MainWindow, hook_alert_QtBaseClass = uic.loadUiType("hook_alert_window.ui")
open_process_Ui_MainWindow, open_process_QtBaseClass = uic.loadUiType("open_process.ui")
			
class MyWindow(QMainWindow):
	def __init__(self, parent=None):
		print("MyWindow __init__ called!")
		super(MyWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.process_list_set()
			
		self.ui.pushButton_hook.clicked.connect(self.hook_btn_clicked)
		self.ui.pushButton_refresh.clicked.connect(self.process_list_set)
		
		# Open Process
		self.ui.pushButton_openProcess.clicked.connect(self.openProcess)
		
		self.ui.pushButton_go.clicked.connect(self.intercept_go_button)
		self.ui.pushButton_interceptToggle.toggled.connect(self.toggle_intercept_on)
		
		# 아래 4 줄은 헥스뷰와 스트링뷰를 연동하기 위한 것.
		self.ui.tableWidget_hexTable.cellChanged.connect(self.intercept_hexTable_changed)
		self.ui.tableWidget_hexTable.itemSelectionChanged.connect(self.hexTable_itemSelected)
		
		self.ui.tableWidget_stringTable.cellChanged.connect(self.intercept_strTable_changed)
		self.ui.tableWidget_stringTable.itemSelectionChanged.connect(self.strTable_itemSelected)
	
		# ikeeby
		# Repeater HEX, String VIEW
		# Repeater REQUEST 만 바꾸기 이벤트
		self.ui.tableWidget_hexTable_3.cellChanged.connect(self.intercept_hexTable_changed_3)
		self.ui.tableWidget_hexTable_3.itemSelectionChanged.connect(self.hexTable_itemSelected_3)
		
		self.ui.tableWidget_stringTable_3.cellChanged.connect(self.intercept_strTable_changed_3)
		self.ui.tableWidget_stringTable_3.itemSelectionChanged.connect(self.strTable_itemSelected_3)
		
		# Repeater RESPONSE 는 바꾸지 못하도록
		
		self.ui.tableWidget_hexTable_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.ui.tableWidget_stringTable_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
		
		# Repeater go button
		self.ui.pushButton_go_2.clicked.connect(self.repeater_go_button)
		
		# custom mouse right click event init
		self.tableWidget_proxyHistory_right_click()
		######## ikeeby

	
		# Core Frida Agent 클래스 생성
		self.frida_agent = FridaAgent(self)
		self.ui.textBrowser_log.append("[#] Create Frdia Agent")
		
		#################################################
		self.match_and_replace = Match_and_Replace(self.ui.tableWidget_MatchAndReplace)
		#################################################
		
		# Core Frida Agent로 부터 넘어오는 시그널 연결
		self.make_connection(self.frida_agent)
		self.make_connection_err(self.frida_agent)
		
		# Process Open을 위한 [+] 버튼 누르면 나오는 창 만들기
		self.open_process_window = QMainWindow()
		self.open_process_ui = open_process_Ui_MainWindow()
		self.open_process_ui.setupUi(self.open_process_window)
		self.open_process_window.setWindowFlags(Qt.FramelessWindowHint)
			
		self.open_process_ui.pushButton_start.clicked.connect(self.gui_start_process)
		self.open_process_ui.pushButton_cancleProcOpen.clicked.connect(self.closeOpenProc)

		# Option - hook checkbox
		self.ui.checkBox_send.stateChanged.connect(self.click_hook_send)
		self.ui.checkBox_recv.stateChanged.connect(self.click_hook_recv)
		self.ui.checkBox_sendto.stateChanged.connect(self.click_hook_sendto)
		self.ui.checkBox_recvfrom.stateChanged.connect(self.click_hook_recvfrom)
		self.ui.checkBox_wsasend.stateChanged.connect(self.click_hook_wsasend)
		self.ui.checkBox_wsarecv.stateChanged.connect(self.click_hook_wsarecv)
		self.ui.checkBox_encryptmessage.stateChanged.connect(self.click_hook_encryptmessage)
		self.ui.checkBox_decryptmessage.stateChanged.connect(self.click_hook_decryptmessage)
	
	def click_hook_send(self, state):
		print("MyWindow click_hook_send called!")
		if state == Qt.Checked:
			#hook
			self.frida_agent.hook_js("send")
		else:
			#unhook
			self.frida_agent.unhook_js("send")

	def click_hook_recv(self, state):
		print("MyWindow click_hook_recv called!")
		if state == Qt.Checked:
			#hook
			self.frida_agent.hook_js("recv")
		else:
			#unhook
			self.frida_agent.unhook_js("recv")

	def click_hook_sendto(self, state):
		print("MyWindow click_hook_sendto called!")
		if state == Qt.Checked:
			#hook
			self.frida_agent.hook_js("sendto")
		else:
			#unhook
			self.frida_agent.unhook_js("sendto")

	def click_hook_recvfrom(self, state):
		print("MyWindow click_hook_recvfrom called!")
		if state == Qt.Checked:
			#hook
			self.frida_agent.hook_js("recvfrom")
		else:
			#unhook
			self.frida_agent.unhook_js("recvfrom")

	def click_hook_wsasend(self, state):
		print("MyWindow click_hook_wsasend called!")
		if state == Qt.Checked:
			#hook
			self.frida_agent.hook_js("wsasend")
		else:
			#unhook
			self.frida_agent.unhook_js("wsasend")

	def click_hook_wsarecv(self, state):
		print("MyWindow click_hook_wsarecv called!")
		if state == Qt.Checked:
			#hook
			self.frida_agent.hook_js("wsarecv")
		else:
			#unhook
			self.frida_agent.unhook_js("wsarecv")
	
	def click_hook_encryptmessage(self, state):
		print("MyWindow click_hook_encryptmessage called!")
		if state == Qt.Checked:
			#hook
			self.ui.textBrowser_log.append("[^] Encryptmessage is not supported yet...")
		else:
			#unhook
			self.ui.textBrowser_log.append("[^] Encryptmessage is not supported yet...")

	def click_hook_decryptmessage(self, state):
		print("MyWindow click_hook_decryptmessage called!")
		if state == Qt.Checked:
			#hook
			self.ui.textBrowser_log.append("[^] Decryptmessage is not supported yet...")
		else:
			#unhook
			self.ui.textBrowser_log.append("[^] Decryptmessage is not supported yet...")	
	
	#################################################
	def resizeEvent(self, event):
		print("MyWindow resizeEvent called!")
		#print("resize")
		self.match_and_replace.resize()
	#################################################
	
	# openProcess Click 하면 실행되는 함수
	def openProcess(self):
		print("MyWindow openProcess called!")
		self.open_process_window.show()
		# 아래 있는 코드들은 실제 실행 되는 코드

		#self.frida_agent.inject_script(pid)
		#self.frida_agent.resume_process(int(pid))

	def closeOpenProc(self):
		print("MyWindow closeOpenProc called!")
		self.open_process_window.close()

	def gui_start_process(self):
		print("MyWindow gui_start_process called!")
		filePath = self.open_process_ui.lineEdit_filePath.text()
		argument = self.open_process_ui.lineEdit_arg.text()
		
		pid = self.frida_agent.start_process(filePath,argument)
	
		self.open_alert_window(pid,True)
		
		# 위에 openProcess 랑 연결할 것임. 지금은 윈도우 창 닫는걸로 테스트
		self.open_process_window.close()
	
	def close_alertwindow(self):
		print("MyWindow close_alertwindow called!")
		self.alert_window.close()
		
		# 두번째 proxy 탭으로 이동
		self.ui.tabWidget_tab.setCurrentIndex(1)
	# customs context menu	
	def tableWidget_proxyHistory_right_click(self):
		print("MyWindow tableWidget_proxyHistory_right_click called!")
		
		self.ui.tableWidget_proxyHistory.setContextMenuPolicy(Qt.ActionsContextMenu)
		send_repeater = QAction("Send to Repeater", self.ui.tableWidget_proxyHistory)
		self.ui.tableWidget_proxyHistory.addAction(send_repeater)
		
		send_repeater.triggered.connect(self.tableWidget_proxyHistory_right_click_event)
		
	def tableWidget_proxyHistory_right_click_event(self):
		print("MyWindow tableWidget_proxyHistory_right_click_event called!")
		
		# get mouse pos
		pos = QCursor.pos() # PyQt5.QtCore.QPoint(262, 215)
		
		# get proxyHistory row 
		row = self.ui.tableWidget_proxyHistory.rowAt(self.ui.tableWidget_proxyHistory.viewport().mapFromGlobal(pos).y())
		
		if(row>-1):
			
			self.send_packet_to_Repeater(row)
			self.ui.tabWidget_tab.setCurrentIndex(2)
		
	############ikeeby
	
	def process_list_set(self):
		print("MyWindow process_list_set called!")
		header = self.ui.tableWidget_procList.horizontalHeader()       
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		
		process_list = get_process_list()
		
		self.ui.tableWidget_procList.setRowCount(len(process_list))
				
		c = 0
		for proc in process_list:
			self.ui.tableWidget_procList.setItem(c, 0, QTableWidgetItem(str(proc[0])))
			self.ui.tableWidget_procList.setItem(c, 1, QTableWidgetItem(proc[1]))
			c += 1
			
		self.ui.tableWidget_procList.cellClicked.connect(self.process_clicked)
		self.ui.tableWidget_procList.cellDoubleClicked.connect(self.hook_btn_clicked)
	
	def process_clicked(self,row, col):
		print("MyWindow process_clicked called!")
		proc_pid = self.ui.tableWidget_procList.item(row, 0).text()
		proc_name = self.ui.tableWidget_procList.item(row, 1).text()
		
		
		self.ui.lineEdit_pid_input.setText(proc_pid)
		# 상태바에 선택한 프로세스 정보 보여주기
		message = "PID : {} / Process Name : {}".format(proc_pid,proc_name)
		self.ui.statusbar.showMessage(message)

	def hook_btn_clicked(self):
		print("MyWindow hook_btn_clicked called!")
		user_input_pid = self.ui.lineEdit_pid_input.text()
		
		self.open_alert_window(user_input_pid)
	
		#hook_function(pid)
	
	def open_alert_window(self,pid,start_process_flag=False):
		print("MyWindow open_alert_window called!")
		self.hook_pid = pid
		self.alert_window = QMainWindow()
		self.alert_ui = hook_alert_Ui_MainWindow()
		self.alert_ui.setupUi(self.alert_window)
		self.alert_window.setWindowFlags(Qt.FramelessWindowHint)
		self.alert_window.show()
		
		if(start_process_flag == False):
			self.frida_agent.inject_frida_agent(pid)
			self.frida_agent.inject_script(pid)
		
		self.alert_ui.pushButton_gogo.clicked.connect(self.close_alertwindow)
		
	def close_alertwindow(self):
		print("MyWindow close_alertwindow called!")
		self.alert_window.close()
		
		# 두번째 proxy 탭으로 이동
		self.ui.tabWidget_tab.setCurrentIndex(1)
	
	def make_connection(self, class_object):
		print("MyWindow make_connection called!")
		class_object.from_agent_data.connect(self.from_fridaJS)
		
	def make_connection_err(self, class_object):
		print("MyWindow make_connection_err called!")
		class_object.error_signal.connect(self.error_message_box)
	
	@pyqtSlot(str)	
	def from_fridaJS(self,data):
		print("MyWindow from_fridaJS called!")
		#self.ui.textBrowser_hexData.setText(data)
		#self.ui.textBrowser_hexData.append(str(message))
			
		if(data.startswith("[PROXY]")):
			func_name, ip_info, port_info = parsing_info(data)
			pid = parsing_pid(data)
			hex_data = parsing_hex(data)

			# packet이 들어오면 먼저 match_and_replace !
			change_flag, hex_data = self.match_and_replace_func(pid, func_name, ip_info, port_info, hex_data)
			

			
			#hex_data = parsing_hex(data)

			# 인터셉트 모드일 경우
			if(self.frida_agent.intercept_on):
				self.frida_agent.current_isIntercept = True
					
				self.intercept_view(pid,func_name,ip_info,port_info,hex_data)
				self.ui.tabWidget_proxyTab.setCurrentIndex(0)
				# 클릭을 연결해두기. (go button)
			else:
				# 빈 문자 전송
							
				if(change_flag):
					self.frida_agent.send_spoofData(pid,func_name,hex_data)
				else:
					self.frida_agent.send_spoofData(pid,func_name,[])
					
				self.history_addRow(pid, func_name, ip_info, port_info, hex_data)
					
			# 전송 후, 히스토리에 기록
			
			#self.history_addRow(pid, func_name, ip_info, port_info, hex_data)

	def match_and_replace_func(self, pid, func_name, ip_info, port_info, hex_data):
		print("MyWindow match_and_replace_func called!")	
		strHex = ""
		change_flag = False
		
		if(len(hex_data)>0 and len(self.match_and_replace.enabled_list)>0):

			for hex in hex_data:
				strHex += hex + " "
			strHex = strHex[:-1] # remove " "
			
			for enabled_data in self.match_and_replace.enabled_list:
				filter_ip = enabled_data["ip"]
				filter_port = enabled_data["port"]
				filter_function = enabled_data["function"]
				
				print(filter_function)
				print(func_name)

				if(filter_ip == ip_info and filter_port == port_info and filter_function == func_name):
					print("match and replace start")
					# match and replace start!
					
					match_data = enabled_data["match"]
					replace_data = enabled_data["replace"]
					'''
					idx = strHex.find(match_data)
					if(idx > -1):
						strHex = strHex[:idx] + replace_data + strHex[idx+len(match_data):]
						hex_data = strHex.split(' ')
						change_flag = True
					'''
					idx = strHex.find(match_data)
					if(idx > -1):
						print("match find! replace complete")
						strHex = strHex.replace(match_data,replace_data)
						hex_data = strHex.split(' ')
						change_flag = True
						#print(hex_data)
					
		return change_flag, hex_data
					
	#def history_addRow(self,history_item):
	def history_addRow(self,pid, func_name, ip_info, port_info, hex_data):
		print("MyWindow history_addRow called!")	
		#pid = parsing_pid(history_item)
		proc_name = get_process_name(pid)
		#func_name, ip_info, port_info = parsing_info(history_item)
		#hex_data = parsing_hex(history_item)
		hex_text, str_text = hexDump2Str(hex_data)
		
		append_data = {"pid":pid,"proc_name":proc_name,"func_name":func_name,"ip":ip_info,"port":port_info,"hex_data":hex_data,"hex_text":hex_text,"str_text":str_text}
		# History 기록
		self.frida_agent.proxy_history.append(append_data)
		
		numRows = self.ui.tableWidget_proxyHistory.rowCount()
		
		self.ui.tableWidget_proxyHistory.insertRow(numRows)

		add_item = self.frida_agent.proxy_history[-1]
		
		self.ui.tableWidget_proxyHistory.setItem(numRows, 0, QTableWidgetItem(add_item['pid']))
		self.ui.tableWidget_proxyHistory.setItem(numRows, 1, QTableWidgetItem(add_item["proc_name"]))
		self.ui.tableWidget_proxyHistory.setItem(numRows, 2, QTableWidgetItem(add_item["func_name"]))
		self.ui.tableWidget_proxyHistory.setItem(numRows, 3, QTableWidgetItem(add_item["ip"]))
		self.ui.tableWidget_proxyHistory.setItem(numRows, 4, QTableWidgetItem(add_item["port"]))
		self.ui.tableWidget_proxyHistory.setItem(numRows, 5, QTableWidgetItem(add_item["str_text"]))
		
		self.ui.tableWidget_proxyHistory.cellClicked.connect(self.history_detail)
		
		if(self.ui.checkBox_autoScroll.isChecked()):
			current_item = self.ui.tableWidget_proxyHistory.item(numRows, 0)
			self.ui.tableWidget_proxyHistory.scrollToItem(current_item, QAbstractItemView.PositionAtBottom)
			#self.ui.tableWidget_proxyHistory.selectRow(numRows)

	
	def history_detail(self,row, col):
		print("MyWindow history_detail called!")	
		hex_text = self.frida_agent.proxy_history[row]['hex_text']
		str_text = self.frida_agent.proxy_history[row]['str_text']
		self.ui.textBrowser_hexData.setText(hex_text)
		self.ui.textBrowser_stringData.setText(str_text)
		
		# test용
		self.ui.statusbar.showMessage("PID : {} / Process Name : {}".format(self.frida_agent.proxy_history[row]['pid'],self.frida_agent.proxy_history[row]['proc_name']))

	#ikeeby
	def send_packet_to_Repeater(self,row):
		print("MyWindow send_packet_to_Repeater called!")	
		# 기존 데이터 초기화
		self.ui.tableWidget_hexTable_3.setRowCount(0)
		self.ui.tableWidget_stringTable_3.setRowCount(0)
		#
		
		# Destination IP, PORT Setting
		ip = self.frida_agent.proxy_history[row]['ip']
		port = self.frida_agent.proxy_history[row]['port']
		
		self.ui.repeater_ip_box.setText(ip)
		self.ui.repeater_port_box.setText(port)

		# Hex, String View Setting
		hex_text = self.frida_agent.proxy_history[row]['hex_text']
		str_text = self.frida_agent.proxy_history[row]['str_text']
		hex_data = hex_text.split(' ')[:-1] 

		# 기존 intercept_view function pid 부분 빼고 복붙
		need_row_num = int(len(hex_data) / 16)
				
		#self.ui.tableWidget_hexTable.clearContents()
		
		for row in range(need_row_num+1):
			numRows = self.ui.tableWidget_hexTable_3.rowCount()
		
			self.ui.tableWidget_hexTable_3.insertRow(numRows)
			self.ui.tableWidget_stringTable_3.insertRow(numRows)
			
			if(row< need_row_num):
				# 16번 반복
				for i in range(16):
					self.ui.tableWidget_hexTable_3.setItem(row, i, QTableWidgetItem(hex_data[(16*row)+i]))
					self.ui.tableWidget_hexTable_3.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
					self.ui.tableWidget_stringTable_3.setItem(row, i, QTableWidgetItem(chr(int(hex_data[(16*row)+i],16))))
					self.ui.tableWidget_stringTable_3.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
			else:
				# total_length - (need_row_num * 16)
				for i in range((len(hex_data)-(need_row_num * 16))):
					self.ui.tableWidget_hexTable_3.setItem(row, i, QTableWidgetItem(hex_data[(16*row)+i]))
					self.ui.tableWidget_hexTable_3.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
					self.ui.tableWidget_stringTable_3.setItem(row, i, QTableWidgetItem(chr(int(hex_data[(16*row)+i],16))))
					self.ui.tableWidget_stringTable_3.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)


	def recv_packet_to_Repeater(self, packet):
		print("MyWindow recv_packet_to_Repeater called!")	
		# 기존 데이터 초기화
		self.ui.tableWidget_hexTable_2.setRowCount(0)
		self.ui.tableWidget_stringTable_2.setRowCount(0)

		# Hex, String View Setting
		#hex_text = packet
		hex_data = packet
		#print(hex_data)

		# 기존 intercept_view function pid 부분 빼고 복붙
		need_row_num = int(len(hex_data) / 16)
				
		#self.ui.tableWidget_hexTable.clearContents()
		
		for row in range(need_row_num+1):
			numRows = self.ui.tableWidget_hexTable_2.rowCount()
		
			self.ui.tableWidget_hexTable_2.insertRow(numRows)
			self.ui.tableWidget_stringTable_2.insertRow(numRows)
			
			if(row< need_row_num):
				# 16번 반복
				for i in range(16):
					self.ui.tableWidget_hexTable_2.setItem(row, i, QTableWidgetItem(hex_data[(16*row)+i]))
					self.ui.tableWidget_hexTable_2.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
					self.ui.tableWidget_stringTable_2.setItem(row, i, QTableWidgetItem(chr(int(hex_data[(16*row)+i],16))))
					self.ui.tableWidget_stringTable_2.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
			else:
				# total_length - (need_row_num * 16)
				for i in range((len(hex_data)-(need_row_num * 16))):
					self.ui.tableWidget_hexTable_2.setItem(row, i, QTableWidgetItem(hex_data[(16*row)+i]))
					self.ui.tableWidget_hexTable_2.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
					self.ui.tableWidget_stringTable_2.setItem(row, i, QTableWidgetItem(chr(int(hex_data[(16*row)+i],16))))
					self.ui.tableWidget_stringTable_2.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

	
	
	######### ikeeby
	
	
	#"[PROXY][FUNC_NAME]"+hook_function_name+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res
	
	def intercept_view(self,pid,func_name,ip_info,port_info,hex_data):
		print("MyWindow intercept_view called!")	
		proc_name = get_process_name(pid)
		self.ui.lineEdit_intercept_info.setText("PID : {} / Process Name : {} / FUNCTION : {} / ADDRESS : {}:{}".format(pid,proc_name,func_name,ip_info,port_info))
		need_row_num = int(len(hex_data) / 16)
				
		#self.ui.tableWidget_hexTable.clearContents()
		
		for row in range(need_row_num+1):
			numRows = self.ui.tableWidget_hexTable.rowCount()
		
			self.ui.tableWidget_hexTable.insertRow(numRows)
			self.ui.tableWidget_stringTable.insertRow(numRows)
			
			if(row< need_row_num):
				# 16번 반복
				for i in range(16):
					self.ui.tableWidget_hexTable.setItem(row, i, QTableWidgetItem(hex_data[(16*row)+i]))
					self.ui.tableWidget_hexTable.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
					self.ui.tableWidget_stringTable.setItem(row, i, QTableWidgetItem(chr(int(hex_data[(16*row)+i],16))))
					self.ui.tableWidget_stringTable.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
			else:
				# total_length - (need_row_num * 16)
				for i in range((len(hex_data)-(need_row_num * 16))):
					self.ui.tableWidget_hexTable.setItem(row, i, QTableWidgetItem(hex_data[(16*row)+i]))
					self.ui.tableWidget_hexTable.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
					
					self.ui.tableWidget_stringTable.setItem(row, i, QTableWidgetItem(chr(int(hex_data[(16*row)+i],16))))
					self.ui.tableWidget_stringTable.item(numRows,i).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
	
	
	def hexTableToList(self):
		print("MyWindow hexTableToList called!")	
		hexTable = self.ui.tableWidget_hexTable
		hexList = []
		
		numRows = hexTable.rowCount()
		
		for i in range(numRows):
			for j in range(16):
				hexDataItem = hexTable.item(i, j)
				if hexDataItem != None:
					hexList.append(hexDataItem.text())
					
		return hexList
		
	def intercept_go_button(self):
		print("MyWindow intercept_go_button called!")			
		#self.ui.textBrowser_hexData.setText(str(hexList))
		intercept_info = self.ui.lineEdit_intercept_info.text().split()
		#print("intercept_info!")
		#print(intercept_info)
		
		
		pid = intercept_info[2]
		func_name = intercept_info[11]
		ip_info, port_info = intercept_info[-1].split(":")
		
		if(self.frida_agent.current_isIntercept):
			hex_data = self.hexTableToList()
			
			self.frida_agent.send_spoofData(pid, func_name, hex_data)
			
			self.history_addRow(pid, func_name, ip_info, port_info, hex_data)
			
			for i in reversed(range(self.ui.tableWidget_hexTable.rowCount())):
				self.ui.tableWidget_hexTable.removeRow(i)
				
			for i in reversed(range(self.ui.tableWidget_stringTable.rowCount())):
				self.ui.tableWidget_stringTable.removeRow(i)
				
			self.ui.lineEdit_intercept_info.setText("")
		
		self.ui.tableWidget_hexTable.setRowCount(0)
		self.ui.tableWidget_stringTable.setRowCount(0)

	def repeater_hexTableToList(self):
		print("MyWindow repeater_hexTableToList called!")		
		hexTable = self.ui.tableWidget_hexTable_3
		hexList = []
		
		numRows = hexTable.rowCount()
		
		for i in range(numRows):
			for j in range(16):
				hexDataItem = hexTable.item(i, j)
				if hexDataItem != None:
					hexList.append(hexDataItem.text())
					
		return hexList
				
	def repeater_go_button(self):
		print("MyWindow repeater_go_button called!")	

		hexList = self.repeater_hexTableToList()		
		
		# change hexlist to byte array
		data = bytes([int(x,16) for x in hexList])

		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.ui.repeater_ip_box.text(), int(self.ui.repeater_port_box.text())))
			sock.settimeout(1) # timeout 설정
			
			sock.send(data)

			recv_data = sock.recv(1024)
			
			recv_data2 = recv_data.hex()
			recv_data_list = []
			for i in range(0,len(recv_data2),2):
				recv_data_list.append(recv_data2[i:i+2])
			#print(recv_data_list)
			
			self.recv_packet_to_Repeater(recv_data_list)

		except socket.timeout:
			print("repeater_go_button: ")
			print("timeout error")
		except Exception as e:
			print("repeater_go_button: ")
			print(e)
		finally:
			sock.close()
			


		
	def toggle_intercept_on(self):
		print("MyWindow toggle_intercept_on called!")	
		self.frida_agent.intercept_on = self.ui.pushButton_interceptToggle.isChecked()
		
		if(self.frida_agent.current_isIntercept):
			# 현재 인터셉트 중인지 확인, 인터셉트 중이라면 intercept_go 버튼 클릭
			self.intercept_go_button()
		
		if(self.frida_agent.intercept_on):
			self.ui.pushButton_interceptToggle.setText("Intercept ON")
		else:
			self.ui.pushButton_interceptToggle.setText("Intercept OFF")
			
	def intercept_hexTable_changed(self, row, col):
		print("MyWindow intercept_hexTable_changed called!")	
		changed_data = self.ui.tableWidget_hexTable.item(row, col).text()
		print(changed_data)
		
		try:
			tmp = int(changed_data,16)
		except Exception as e:
			print("exception")
			print(e)
			changed_data = "00"
			
		if(len(changed_data) != 2):
			changed_data = "0" + changed_data
		
		if(self.ui.tableWidget_hexTable.item(row, col) != None):
			self.ui.tableWidget_hexTable.item(row, col).setText(changed_data)
		if(self.ui.tableWidget_stringTable.item(row, col) != None):
			self.ui.tableWidget_stringTable.item(row, col).setText(chr(int(changed_data,16)))
		
		
	def hexTable_itemSelected(self):
		print("MyWindow hexTable_itemSelected called!")	
		for sel_item in self.ui.tableWidget_hexTable.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_stringTable.setCurrentCell(row,col)

	def intercept_strTable_changed(self,row, col):
		print("MyWindow intercept_strTable_changed called!")	
		changed_data = self.ui.tableWidget_stringTable.item(row, col).text()
		print(changed_data)	
		if(len(changed_data) != 1):
			changed_data = " "
			
		self.ui.tableWidget_hexTable.item(row, col).setText(hex(ord(changed_data))[2:])
		self.ui.tableWidget_stringTable.item(row, col).setText(changed_data)
		
	def strTable_itemSelected(self):
		print("MyWindow strTable_itemSelected called!")	
		for sel_item in self.ui.tableWidget_stringTable.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_hexTable.setCurrentCell(row,col)

	# ikeeby
	def intercept_hexTable_changed_3(self, row, col):
		print("MyWindow intercept_hexTable_changed_3 called!")	
		changed_data = self.ui.tableWidget_hexTable_3.item(row, col).text()
		
		try:
			tmp = int(changed_data,16)
		except Exception:
			changed_data = "00"
			
		if(len(changed_data) != 2):
			changed_data = "0" + changed_data
		
		if(self.ui.tableWidget_hexTable_3.item(row, col) != None):
			self.ui.tableWidget_hexTable_3.item(row, col).setText(changed_data)
		if(self.ui.tableWidget_stringTable_3.item(row, col) != None):
			self.ui.tableWidget_stringTable_3.item(row, col).setText(chr(int(changed_data,16)))
	# ikeeby	
	def hexTable_itemSelected_3(self):
		print("MyWindow hexTable_itemSelected_3 called!")	
		for sel_item in self.ui.tableWidget_hexTable_3.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_stringTable_3.setCurrentCell(row,col)
	# ikeeby
	def intercept_strTable_changed_3(self,row, col):
		print("MyWindow intercept_strTable_changed_3 called!")	
		changed_data = self.ui.tableWidget_stringTable_3.item(row, col).text()
			
		if(len(changed_data) != 1):
			changed_data = " "
			
		self.ui.tableWidget_hexTable_3.item(row, col).setText(hex(ord(changed_data))[2:])
		self.ui.tableWidget_stringTable_3.item(row, col).setText(changed_data)
	# ikeeby
	def strTable_itemSelected_3(self):
		print("MyWindow strTable_itemSelected_3 called!")	
		for sel_item in self.ui.tableWidget_stringTable_3.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_hexTable_3.setCurrentCell(row,col)

			
	@pyqtSlot(str)	
	def error_message_box(self,data):
		print("MyWindow error_message_box called!")	
		# 에러 메시지 박스 오픈
		# 임시로 아래 상태바에 출력
		self.ui.statusbar.showMessage(data)
		self.ui.textBrowser_log.append("[*] Error : "+str(data))
		#self.ui.textBrowser_hexData.setText(data)
		#self.ui.textBrowser_hexData.append(str(message))

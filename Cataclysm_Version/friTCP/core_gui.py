# core_gui.py
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox,QLineEdit,QAbstractItemView, QAction, QMenu
from PyQt5.QtGui import QStandardItemModel,QStandardItem, QPixmap,QIcon, QRegExpValidator, QCursor
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal, pyqtSlot
from core_func import *
import ast
import socket

Ui_MainWindow, QtBaseClass = uic.loadUiType("main_window.ui")
hook_alert_Ui_MainWindow, hook_alert_QtBaseClass = uic.loadUiType("hook_alert_window.ui")
			
class MyWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MyWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.process_list_set()
			
		self.ui.pushButton_hook.clicked.connect(self.hook_btn_clicked)
		self.ui.pushButton_refresh.clicked.connect(self.process_list_set)
		
		self.ui.pushButton_go.clicked.connect(self.intercept_go_button)
		self.ui.pushButton_interceptToggle.toggled.connect(self.toggle_intercept_on)
		
		# 아래 4 줄은 헥스뷰와 스트링뷰를 연동하기 위한 것.
		self.ui.tableWidget_hexTable.cellChanged.connect(self.intercept_hexTable_changed)
		self.ui.tableWidget_hexTable.itemSelectionChanged.connect(self.hexTable_itemSelected)
		
		self.ui.tableWidget_stringTable.cellChanged.connect(self.intercept_strTable_changed)
		self.ui.tableWidget_stringTable.itemSelectionChanged.connect(self.strTable_itemSelected)
	
		# ikeeby
		# Repeater HEX, String VIEW
		# REQUEST 만 바꾸기 이벤트
		self.ui.tableWidget_hexTable_2.cellChanged.connect(self.intercept_hexTable_changed_2)
		self.ui.tableWidget_hexTable_2.itemSelectionChanged.connect(self.hexTable_itemSelected_2)
		
		self.ui.tableWidget_stringTable_2.cellChanged.connect(self.intercept_strTable_changed_2)
		self.ui.tableWidget_stringTable_2.itemSelectionChanged.connect(self.strTable_itemSelected_2)
		# RESPONSE 는 바꿀 필요가 없음
		
		# Repeater go button
		self.ui.pushButton_go_2.clicked.connect(self.repeater_go_button)
		
		######## ikeeby

	
		# Core Frida Agent 클래스 생성
		self.frida_agent = FridaAgent(self)
		self.ui.textBrowser_log.append("[#] Create Frdia Agent")
		
		# Core Frida Agent로 부터 넘어오는 시그널 연결
		self.make_connection(self.frida_agent)
		self.make_connection_err(self.frida_agent)

	
	#ikeeby
	# default context menu (mouse right click) event listener
	def contextMenuEvent(self, event):

		pos = event.globalPos()
		row = self.ui.tableWidget_proxyHistory.rowAt(self.ui.tableWidget_proxyHistory.viewport().mapFromGlobal(pos).y())
		
		# proxyHistory table 에서 클릭할 시에만 메뉴 보이기
		if(row > -1):
			menu = QMenu()
			sendRepeater = menu.addAction("Send To Repeater")
			action = menu.exec_(pos)
			
			if action == sendRepeater:
				self.send_packet_to_Repeater(row)
	
	############ikeeby
	
	def process_list_set(self):
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
		proc_pid = self.ui.tableWidget_procList.item(row, 0).text()
		proc_name = self.ui.tableWidget_procList.item(row, 1).text()
		
		
		self.ui.lineEdit_pid_input.setText(proc_pid)
		# 상태바에 선택한 프로세스 정보 보여주기
		message = "PID : {} / Process Name : {}".format(proc_pid,proc_name)
		self.ui.statusbar.showMessage(message)

	def hook_btn_clicked(self):
		user_input_pid = self.ui.lineEdit_pid_input.text()
		
		self.open_alert_window(user_input_pid)
	
		#hook_function(pid)
	
	def open_alert_window(self,pid):
		self.hook_pid = pid
		self.alert_window = QMainWindow()
		self.alert_ui = hook_alert_Ui_MainWindow()
		self.alert_ui.setupUi(self.alert_window)
		self.alert_window.setWindowFlags(Qt.FramelessWindowHint)
		self.alert_window.show()
		
		self.frida_agent.inject_frida_agent(pid)
		self.frida_agent.inject_script(pid)
		
		self.alert_ui.pushButton_gogo.clicked.connect(self.close_alertwindow)
		
	def close_alertwindow(self):
		self.alert_window.close()
		
		# 두번째 proxy 탭으로 이동
		self.ui.tabWidget_tab.setCurrentIndex(1)
	
	def make_connection(self, class_object):
		class_object.from_agent_data.connect(self.from_fridaJS)
		
	def make_connection_err(self, class_object):
		class_object.error_signal.connect(self.error_message_box)
	
	@pyqtSlot(str)	
	def from_fridaJS(self,data):
		#self.ui.textBrowser_hexData.setText(data)
		#self.ui.textBrowser_hexData.append(str(message))
			
		if(data.startswith("[PROXY]")):
			func_name, ip_info, port_info = parsing_info(data)
			pid = parsing_pid(data)
			
			# 히스토리에 기록
			self.history_addRow(data)
			
			# 인터셉트 모드일 경우
			if(self.frida_agent.intercept_on):
				self.frida_agent.current_isIntercept = True
				hex_data = parsing_hex(data)	
				self.intercept_view(pid,func_name,ip_info,port_info,hex_data)
				self.ui.tabWidget_proxyTab.setCurrentIndex(0)
				# 클릭을 연결해두기. (go button)
			else:
				# 빈 문자 전송
				self.frida_agent.send_spoofData(pid,[])
	
	def history_addRow(self,history_item):
		pid = parsing_pid(history_item)
		proc_name = get_process_name(pid)
		func_name, ip_info, port_info = parsing_info(history_item)
		hex_list = parsing_hex(history_item)
		hex_text, str_text = hexDump2Str(hex_list)
		
		append_data = {"pid":pid,"proc_name":proc_name,"func_name":func_name,"ip":ip_info,"port":port_info,"hex_list":hex_list,"hex_text":hex_text,"str_text":str_text}
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
	
		

		
		
		current_item = self.ui.tableWidget_proxyHistory.item(numRows, 0)
		self.ui.tableWidget_proxyHistory.scrollToItem(current_item, QAbstractItemView.PositionAtBottom)
		#self.ui.tableWidget_proxyHistory.selectRow(numRows)

	
	def history_detail(self,row, col):
		hex_text = self.frida_agent.proxy_history[row]['hex_text']
		str_text = self.frida_agent.proxy_history[row]['str_text']
		self.ui.textBrowser_hexData.setText(hex_text)
		self.ui.textBrowser_stringData.setText(str_text)
		
		# test용
		self.ui.statusbar.showMessage("PID : {} / Process Name : {}".format(self.frida_agent.proxy_history[row]['pid'],self.frida_agent.proxy_history[row]['proc_name']))

	#ikeeby
	def send_packet_to_Repeater(self,row):
		# 기존 데이터 초기화
		self.ui.tableWidget_hexTable_2.setRowCount(0)
		self.ui.tableWidget_stringTable_2.setRowCount(0)
		#
		
		# Destination IP, PORT Setting
		ip = self.frida_agent.proxy_history[row]['ip']
		port = self.frida_agent.proxy_history[row]['port']
		
		self.ui.repeater_ip_box.setText(ip)
		self.ui.repeater_port_box.setText(port)

		# Hex, String View Setting
		hex_text = self.frida_agent.proxy_history[row]['hex_text']
		str_text = self.frida_agent.proxy_history[row]['str_text']
		hex_data = hex_text.split(' ')[:-1] # 
		#print(hex_data)
		''' 마지막 지우기!
		['48', '65', '6c', '6c', '6f', '20', '53', '65', '72', '76', '65', '72', '21', '
		31', '32', '33', '34', '35', '36', '37', '38', '39', '30', '31', '32', '33', '34
		', '35', '36', '37', '38', '39', '30', '31', '32', '33', '34', '35', '36', '37',
		 '38', '39', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '30', '']
		'''

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


	def recv_packet_to_Repeater(self, packet):
		# 기존 데이터 초기화
		self.ui.tableWidget_hexTable_3.setRowCount(0)
		self.ui.tableWidget_stringTable_3.setRowCount(0)
		#
		

		# Hex, String View Setting
		#hex_text = packet
		hex_data = packet
		#print(hex_data)
		''' 마지막 지우기!
		['48', '65', '6c', '6c', '6f', '20', '53', '65', '72', '76', '65', '72', '21', '
		31', '32', '33', '34', '35', '36', '37', '38', '39', '30', '31', '32', '33', '34
		', '35', '36', '37', '38', '39', '30', '31', '32', '33', '34', '35', '36', '37',
		 '38', '39', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '30', '']
		'''

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

	
	
	######### ikeeby
	
	
	#"[PROXY][FUNC_NAME]"+hook_function_name+" [IP]"+socket_address.ip+" [PORT]"+socket_address.port+" "+"[HEXDUMP]"+buf_length+" " + res
	
	def intercept_view(self,pid,func_name,ip_info,port_info,hex_data):

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
		
		#self.ui.textBrowser_hexData.setText(str(hexList))
		intercept_info = self.ui.lineEdit_intercept_info.text()
		intercept_pid = intercept_info.split()[2]
		
		if(self.frida_agent.current_isIntercept):
			hexList = self.hexTableToList()
			self.frida_agent.send_spoofData(intercept_pid, hexList)
			
			for i in reversed(range(self.ui.tableWidget_hexTable.rowCount())):
				self.ui.tableWidget_hexTable.removeRow(i)
				
			for i in reversed(range(self.ui.tableWidget_stringTable.rowCount())):
				self.ui.tableWidget_stringTable.removeRow(i)
				
			self.ui.lineEdit_intercept_info.setText("")
		
		self.ui.tableWidget_hexTable.setRowCount(0)
		self.ui.tableWidget_stringTable.setRowCount(0)

	def repeater_hexTableToList(self):
		hexTable = self.ui.tableWidget_hexTable_2
		hexList = []
		
		numRows = hexTable.rowCount()
		
		for i in range(numRows):
			for j in range(16):
				hexDataItem = hexTable.item(i, j)
				if hexDataItem != None:
					hexList.append(hexDataItem.text())
					
		return hexList
				
	def repeater_go_button(self):

		hexList = self.repeater_hexTableToList()		
		
		'''hexList
		['48', '65', '6c', '6c', '6f', '20', '53', '65', '72', '76', '65', '72', '21', '
		31', '32', '33', '34', '35', '36', '37', '38', '39', '30', '31', '32', '33', '34
		', '35', '36', '37', '38', '39', '30', '31', '32', '33', '34', '35', '36', '37',
		 '38', '39', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '30']
		'''
		
		# change hexlist to byte array
		data = bytes([int(x,16) for x in hexList])
		#print("send data")
		#print(data)
		
		
		
		#print("received!")

		

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
		self.frida_agent.intercept_on = self.ui.pushButton_interceptToggle.isChecked()
		
		if(self.frida_agent.current_isIntercept):
			# 현재 인터셉트 중인지 확인, 인터셉트 중이라면 intercept_go 버튼 클릭
			self.intercept_go_button()
		
		if(self.frida_agent.intercept_on):
			self.ui.pushButton_interceptToggle.setText("Intercept ON")
		else:
			self.ui.pushButton_interceptToggle.setText("Intercept OFF")
			
	def intercept_hexTable_changed(self, row, col):
		changed_data = self.ui.tableWidget_hexTable.item(row, col).text()
		
		try:
			tmp = int(changed_data,16)
		except Exception:
			changed_data = "00"
			
		if(len(changed_data) != 2):
			changed_data = "00"
		
		if(self.ui.tableWidget_hexTable.item(row, col) != None):
			self.ui.tableWidget_hexTable.item(row, col).setText(changed_data)
		if(self.ui.tableWidget_stringTable.item(row, col) != None):
			self.ui.tableWidget_stringTable.item(row, col).setText(chr(int(changed_data,16)))
		
	def hexTable_itemSelected(self):
		for sel_item in self.ui.tableWidget_hexTable.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_stringTable.setCurrentCell(row,col)

	def intercept_strTable_changed(self,row, col):
		changed_data = self.ui.tableWidget_stringTable.item(row, col).text()
			
		if(len(changed_data) != 1):
			changed_data = " "
			
		self.ui.tableWidget_hexTable.item(row, col).setText(hex(ord(changed_data))[2:])
		self.ui.tableWidget_stringTable.item(row, col).setText(changed_data)
		
	def strTable_itemSelected(self):
		for sel_item in self.ui.tableWidget_stringTable.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_hexTable.setCurrentCell(row,col)

	# ikeeby
	def intercept_hexTable_changed_2(self, row, col):
		changed_data = self.ui.tableWidget_hexTable_2.item(row, col).text()
		
		try:
			tmp = int(changed_data,16)
		except Exception:
			changed_data = "00"
			
		if(len(changed_data) != 2):
			changed_data = "00"
		
		if(self.ui.tableWidget_hexTable_2.item(row, col) != None):
			self.ui.tableWidget_hexTable_2.item(row, col).setText(changed_data)
		if(self.ui.tableWidget_stringTable_2.item(row, col) != None):
			self.ui.tableWidget_stringTable_2.item(row, col).setText(chr(int(changed_data,16)))
	# ikeeby	
	def hexTable_itemSelected_2(self):
		for sel_item in self.ui.tableWidget_hexTable_2.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_stringTable_2.setCurrentCell(row,col)
	# ikeeby
	def intercept_strTable_changed_2(self,row, col):
		changed_data = self.ui.tableWidget_stringTable_2.item(row, col).text()
			
		if(len(changed_data) != 1):
			changed_data = " "
			
		self.ui.tableWidget_hexTable_2.item(row, col).setText(hex(ord(changed_data))[2:])
		self.ui.tableWidget_stringTable_2.item(row, col).setText(changed_data)
	# ikeeby
	def strTable_itemSelected_2(self):
		for sel_item in self.ui.tableWidget_stringTable_2.selectedItems():
			row = sel_item.row()
			col = sel_item.column()
			
			self.ui.tableWidget_hexTable_2.setCurrentCell(row,col)

			
	@pyqtSlot(str)	
	def error_message_box(self,data):
		# 에러 메시지 박스 오픈
		# 임시로 아래 상태바에 출력
		self.ui.statusbar.showMessage(data)
		self.ui.textBrowser_log.append("[*] Error : "+str(data))
		#self.ui.textBrowser_hexData.setText(data)
		#self.ui.textBrowser_hexData.append(str(message))

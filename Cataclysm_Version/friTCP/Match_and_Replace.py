from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox,QLineEdit,QAbstractItemView, QAction, QMenu, QCheckBox, QHBoxLayout, QWidget, QTableView
from PyQt5.QtGui import QStandardItemModel,QStandardItem, QPixmap,QIcon, QRegExpValidator, QCursor, QResizeEvent
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal, pyqtSlot, QPersistentModelIndex
from core_func import *

match_and_replace_add_Ui_MainWindow, match_and_replace_add_QtBaseClass = uic.loadUiType("match_and_replace_add.ui")
match_and_replace_modify_Ui_MainWindow, match_and_replace_modify_QtBaseClass = uic.loadUiType("match_and_replace_modify.ui")

class Match_and_Replace():
	#arg0 = self.ui.tableWidget_MatchAndReplace
	
	def __init__(self, tableWidget_MatchAndReplace):
		# data init
		self.tableWidget = tableWidget_MatchAndReplace
		self.tableWidget.verticalHeader().setVisible(False)
		self.data_list = []
		self.enabled_list = []
		
		# tablewidget event init
		self.tableWidget_right_click()	
	
		# tablewidget cell click? then select row all -> get row index를 위함
		self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
		
		self.match_former_text=""
		self.replace_former_text=""
		self.ip_former_text=""
		
		self.qCheckbox_list = []
		
		# idx
		self.tableWidget_count = 0

		
	def add(self, data_structure):
		self.data_list.append(data_structure)
	
	def modify(self, new_data):
		idx = new_data['idx']
		for i in range(0,len(self.data_list)):
			print(self.data_list[i]['idx'])
			print(idx)
			if self.data_list[i]['idx'] == idx:
				self.data_list[i] = new_data
				
	
	def remove(self, row):
		del self.data_list[row]
		
	def get_list(self):
		return self.data_list
		
	def refresh(self):
		print("refresh")
		
		#remove all
		numRows = self.tableWidget.rowCount()
		for i in range(0,numRows):
			self.tableWidget.removeRow(0)
		
		#refresh gui
		for my_dict in self.data_list:
			print("refresh for loop")
			numRows = self.tableWidget.rowCount()
			self.tableWidget.insertRow(numRows)
			
			pCheckBox = QCheckBox()
			
			# refresh 할때만 pcheckbox를 넣어주자.
			# my_dict['use']는 pcheckbox filter enable/disable 여부를 설정하기 위한 로직에 사용
			print(my_dict)
			if my_dict["use"] == "True":
				pCheckBox.setChecked(True)

			self.tableWidget.setCellWidget(numRows, 0, pCheckBox)
			pCheckBox.clicked.connect(self.enable_checkbox_clicked)
			
		
			self.tableWidget.setItem(numRows, 1, QTableWidgetItem(my_dict["idx"]))
			self.tableWidget.setItem(numRows, 2, QTableWidgetItem(my_dict["name"]))
			self.tableWidget.setItem(numRows, 3, QTableWidgetItem(my_dict["function"]))
			self.tableWidget.setItem(numRows, 4, QTableWidgetItem(my_dict["ip"]))
			self.tableWidget.setItem(numRows, 5, QTableWidgetItem(my_dict["port"]))
			self.tableWidget.setItem(numRows, 6, QTableWidgetItem(my_dict["match"]))
			self.tableWidget.setItem(numRows, 7, QTableWidgetItem(my_dict["replace"]))
		
		# checkbox click listener
		
	#gui
	
		
	
	def add_addbtn_clicked(self):
		print("add clicked!")
	
		
		self.tableWidget_count += 1
		
		
		my_dict = {}
		#my_dict["use"] = pCheckBox
		my_dict["use"] = "False"
		my_dict["idx"] = str(self.tableWidget_count)
		my_dict["name"] = self.ui.name.text()
		my_dict["function"] = self.ui.function.currentText()
		my_dict["ip"] = self.ui.ip.text()
		my_dict["port"] = self.ui.port.text()
		my_dict["match"] = self.ui.match.text()
		my_dict["replace"] = self.ui.replace.text()
		
		self.add(my_dict)
		self.refresh()

		# checkbox with aligncenter
		'''
		pWidget = QWidget()
		pCheckBox = QCheckBox()
		pLayout = QHBoxLayout(pWidget)
		pLayout.addWidget(pCheckBox)
		pLayout.setAlignment(Qt.AlignCenter)
		pLayout.setContentsMargins(0,0,0,0)
		pWidget.setLayout(pLayout)
		'''

		print(self.data_list)
		self.main.close()
	
	# checkbox click listener
	def enable_checkbox_clicked(self):
		print("enable_checkbox_clicked")
		index_list = []                                                          
		for model_index in self.tableWidget.selectionModel().selectedRows():       
			index = QPersistentModelIndex(model_index)         
			index_list.append(index)                                             
		
		for index in index_list:
			print(index.row())
			print(self.data_list[index.row()]["use"])
			if(self.data_list[index.row()]["use"] == "False"):
				print("enabled_list append")
				self.data_list[index.row()]["use"] = "True"
				self.enabled_list.append(self.data_list[index.row()])	
			else:
				print("enabled_list remove!")
				self.data_list[index.row()]["use"] = "False"
				print("enabled_length")
				print(len(self.enabled_list))
				for count in range(0, len(self.enabled_list)):
					if self.enabled_list[count]['idx'] == self.data_list[index.row()]['idx']:
						print("delete enabled_list")
						del self.enabled_list[count]
						break
		print("enabled_list: ")
		print(self.enabled_list)
		
	def add_cancelbtn_clicked(self):
		print("cancel clicked!")
		self.main.close()
		
	def open_add_window(self):
		print("open_add_window called!")
		# ui init ## window text clear를 시키기 위해 open 할때 ui를 새로 호출함
		self.main = QMainWindow()
		self.ui = match_and_replace_add_Ui_MainWindow()
		self.ui.setupUi(self.main)
		
		# window event init
		
		self.ui.add_btn.clicked.connect(self.add_addbtn_clicked)
		self.ui.cancel_btn.clicked.connect(self.add_cancelbtn_clicked)
		
		self.ui.ip.textEdited.connect(self.ip_text_changed)
		self.ui.port.textEdited.connect(self.port_text_changed)
		#self.ui.ip.setInputMask('000.000.000.000;')

		self.ui.match.textEdited.connect(self.match_text_changed)
		self.ui.replace.textEdited.connect(self.replace_text_changed)
		
		self.main.show()

	def modify_enable_handler_add(self, my_dict):
		# enabled check 되어 있으면 등록
		print("enabled_list append")
		self.enabled_list.append(my_dict)	
		print("enabled_list")
		print(self.enabled_list)

	def modify_enable_handler_remove(self, my_dict):
		# enabled_list remove!
			
		print("enabled_list remove!")
		print("enabled_length")
		print(len(self.enabled_list))
		
		for count in range(0, len(self.enabled_list)):
			if self.enabled_list[count]['idx'] == my_dict['idx']:
				print("delete enabled_list")
				del self.enabled_list[count]
				break
			
	def modify_modifybtn_clicked(self):
		print("modify_modifybtn_clicked!")
		

		my_dict = {}
		my_dict["use"] = self.ui.use.text()
		my_dict["idx"] = self.ui.idx.text()
		my_dict["name"] = self.ui.name.text()
		my_dict["function"] = self.ui.function.currentText()
		my_dict["ip"] = self.ui.ip.text()
		my_dict["port"] = self.ui.port.text()
		my_dict["match"] = self.ui.match.text()
		my_dict["replace"] = self.ui.replace.text()
		
		
		self.modify(my_dict)
		
		# enabled check 되어 있으면 등록
		if(my_dict["use"] == "True"):
			self.modify_enable_handler_add(my_dict)
		
		#refresh data and gui
		self.refresh()
		
		print(self.data_list)
		
		self.main.close()

	def modify_cancelbtn_clicked(self):
		print("cancel clicked!")

		my_dict = {}
		my_dict["use"] = self.ui.use.text()
		my_dict["idx"] = self.ui.idx.text()
		my_dict["name"] = self.ui.name.text()
		my_dict["function"] = self.ui.function.currentText()
		my_dict["ip"] = self.ui.ip.text()
		my_dict["port"] = self.ui.port.text()
		my_dict["match"] = self.ui.match.text()
		my_dict["replace"] = self.ui.replace.text()
		
		# enabled check 되어 있으면 등록
		if(my_dict["use"] == "True"):
			self.modify_enable_handler_add(my_dict)
		self.main.close()
	
	#def ip_textEvent(self):
	def open_modify_window(self, idx):
		print("open_modify_window called!")
		print(idx)
		my_dict = {}
		for data in self.data_list:
			if data['idx'] == idx:
				print("idx same!")
				my_dict = data
		
		print(my_dict)
		
		# ui init ## window text clear를 시키기 위해 open 할때 ui를 새로 호출함
		self.main = QMainWindow()
		self.ui = match_and_replace_modify_Ui_MainWindow()
		self.ui.setupUi(self.main)
		self.ui.idx.hide()
		self.ui.use.hide()
		
		self.ui.modify_btn.clicked.connect(self.modify_modifybtn_clicked)
		self.ui.cancel_btn.clicked.connect(self.modify_cancelbtn_clicked)

		self.ui.idx.setText(idx)
		self.ui.use.setText(my_dict['use'])
		
		self.ui.name.setText(my_dict["name"])

		index = self.ui.function.findText(my_dict["function"], Qt.MatchFixedString)
		self.ui.function.setCurrentIndex(index)
		
		self.ui.ip.setText(my_dict['ip'])
		self.ui.port.setText(my_dict['port'])
		self.ui.match.setText(my_dict['match'])
		self.ui.replace.setText(my_dict['replace'])
		
		self.ui.ip.textEdited.connect(self.ip_text_changed)
		self.ui.port.textEdited.connect(self.port_text_changed)
		#self.ui.ip.setInputMask('000.000.000.000;')

		self.ui.match.textEdited.connect(self.match_text_changed)
		self.ui.replace.textEdited.connect(self.replace_text_changed)

		self.main.show()		
		
	def text_format(self, x):
		if('0'<= x <= '9' or 'A' <= x <= 'F'):
			return x
		else:
			return None
	def ip_format(self, x):
		if('0'<= x <= '9' or '.'==x or '*'==x):
			return x
		else:
			return None
	def port_format(self, x):
		if('0'<= x <= '9' or '*'==x):
			return x
		else:
			return None
			
	def replace_text_changed(self, text):
		print(text)
		text = text.upper()
		text = text.replace(' ','')
		filtered_text = filter(self.text_format,text)
		
		'''
		# filter 된 값이 있었던 것. 헥스 값이 아니므로 clear
		if(len(list(filtered_text)) != len(text)):
			self.ui.replace.setText("")
		'''
		filtered_text = "".join(filtered_text)
		
		tmp_text = ""
		for i in range(0,len(filtered_text),2):
			tmp_text = tmp_text + filtered_text[i:i+2]
			if(len(filtered_text[i:i+2])%2==0):
				tmp_text = tmp_text + " "
				
		if(tmp_text == self.replace_former_text and len(filtered_text) == len(text)):
			tmp_text = tmp_text[:-2]
		
		self.ui.replace.setText(tmp_text)
		self.replace_former_text = tmp_text
			
	def match_text_changed(self, text):
		print(text)
		text = text.lower()
		text = text.replace(' ','')
		filtered_text = filter(self.text_format,text)
		filtered_text = "".join(filtered_text)
		
		tmp_text = ""
		for i in range(0,len(filtered_text),2):
			tmp_text = tmp_text + filtered_text[i:i+2]
			if(len(filtered_text[i:i+2])%2==0):
				tmp_text = tmp_text + " "
				
		if(tmp_text == self.match_former_text and len(filtered_text) == len(text)):
			tmp_text = tmp_text[:-2]
		
		self.ui.match.setText(tmp_text)
		self.match_former_text = tmp_text

		
	def port_text_changed(self, text):
		print(text)
		text = text.lower()
		text = text.replace(' ','')
		filtered_text = filter(self.port_format,text)
		filtered_text = "".join(filtered_text)
		try:
			if(filtered_text == ''):
				pass
			elif(int(filtered_text)<1 or int(filtered_text)>65535):
				filtered_text = filtered_text[:-1]
		except:
			tmp = filtered_text.split('*')
			if(len(tmp)>1):
				filtered_text = '*'
				self.ui.port.setText(filtered_text)	
				return
		self.ui.port.setText(filtered_text)		
		
	def ip_text_changed(self, text):
		print(text)
		text = text.lower()
		text = text.replace(' ','')
		filtered_text = filter(self.ip_format,text)
		
		filtered_str = "".join(filtered_text)

		filtered_list = filtered_str.split('.')
		

		
		tmp_text = filtered_str

		# wrong input logic
		flag = True
		if len(filtered_list)>4:
			flag = False
		for j in filtered_list:
			if j == '':
				break
			print(j)
			
			try:	
				if(int(j)<0 or int(j)>255):
					flag = False
			except:
				tmp = j.split('*')
				if(len(tmp)>1):
					tmp_text = '*'
					self.ui.ip.setText(tmp_text)
					return
					
			if(j.startswith("0") and len(j)!=1):
				flag = False
		# . add logic & . remove logic
		if(flag):
			if len(filtered_list[-1][0:3])%3==0 and len(filtered_list[-1][0:3])!=0 and len(filtered_list)<4:
				tmp_text = tmp_text + "."
			
			if(tmp_text == self.ip_former_text and len(filtered_str) == len(text)):
				tmp_text = tmp_text[:-2]

		else:
			tmp_text = tmp_text[:-1]


				
		self.ui.ip.setText(tmp_text)
		self.ip_former_text = tmp_text
	
	def custom_context_menu(self):
		print("custom_context_menu")
		main_menu = QMenu()
		
		add = main_menu.addAction("Add")
		main_menu.addAction(add)
		add.triggered.connect(self.tableWidget_right_click_add_event)

		remove = main_menu.addAction("Remove")
		main_menu.addAction(remove)		
		remove.triggered.connect(self.tableWidget_right_click_remove_event)		

		modify = main_menu.addAction("Modify")
		main_menu.addAction(modify)		
		modify.triggered.connect(self.tableWidget_right_click_modify_event)			
		
		action = main_menu.exec_(QCursor.pos())	
		
	def tableWidget_right_click(self):
		self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget.customContextMenuRequested.connect(self.custom_context_menu)

		
	def tableWidget_right_click_add_event(self):
		self.open_add_window()

	def tableWidget_right_click_modify_event(self):
		print("tableWidget_right_click_modify_event called!")
		index_list = []                                                          
		for model_index in self.tableWidget.selectionModel().selectedRows():       
			index = QPersistentModelIndex(model_index)         
			index_list.append(index)
			
		my_dict = self.data_list[index_list[0].row()]
		idx = my_dict['idx']
		print("IDX: "+idx)
		self.open_modify_window(idx)
		
		# enabled_list remove!
		if my_dict["use"] == "True":	
			self.modify_enable_handler_remove(my_dict)
		
	def tableWidget_right_click_remove_event(self):
		index_list = []                                                          
		for model_index in self.tableWidget.selectionModel().selectedRows():       
			index = QPersistentModelIndex(model_index)         
			index_list.append(index)                                             
		
		for index in index_list:
			
			# first, remove data if it is in enabled_list
			if self.data_list[index.row()] in self.enabled_list:
				self.enabled_list.remove(self.data_list[index.row()])
				
			self.remove(index.row()) #remove internal data in list
			self.tableWidget.removeRow(index.row()) #remove gui

		print(self.data_list)
		# get mouse pos
		#row = self.tableWidget.currentItem().row()
		
		#print(self.tableWidget.selectionModel().selectedRows())
		#print(len(self.tableWidget.selectedIndexes()))
		#pos = QCursor.pos() # PyQt5.QtCore.QPoint(262, 215)
		#print(pos)
		#row = self.tableWidget.rowAt(self.tableWidget.viewport().mapFromGlobal(pos).y())
		#print(row)
		
		#if(row>-1):
		#	self.tableWidget.removeRow(row)
		#	self.remove(row)	
			
	'''		
	def resize_proxyHistory(self):
		#self.frida_agent.match_and_response_list
		#print("called match_and_response_refresh!")
		#print(self.tableWidget.width())
		
		# match and replace column size init
		print("this is proxyHistory resize..")
		#size = self.tableWidget_proxyHistory.width()
		
		# history column size init
		size = self.ui.tableWidget_proxyHistory.width()
		if(size < 978):
			size = 978
		print(size)
		self.ui.tableWidget_proxyHistory.setColumnWidth(0,size/3/5*2)
		self.ui.tableWidget_proxyHistory.setColumnWidth(1,size/3/5*2)
		self.ui.tableWidget_proxyHistory.setColumnWidth(2,size/3/5*2)
		self.ui.tableWidget_proxyHistory.setColumnWidth(3,size/3/5*2)
		self.ui.tableWidget_proxyHistory.setColumnWidth(4,size/3/5*2)
		self.ui.tableWidget_proxyHistory.setColumnWidth(5,size/3/1)	
		'''
		
	def resize(self, size):
		print("match_and_replace resize called!")
		# match and replace column size init
		#size = self.tableWidget.width()
		#default minimum size 978.. but initial size 622
		if(size < 978):
			size = 978
		print(size)
		self.tableWidget.setColumnWidth(0,size/3/6/1)
		self.tableWidget.setColumnWidth(1,size/3/6/1)
		self.tableWidget.setColumnWidth(2,size/3/6/1)
		self.tableWidget.setColumnWidth(3,size/3/6/1)
		self.tableWidget.setColumnWidth(4,size/3/6/1)
		self.tableWidget.setColumnWidth(5,size/3/6/1)
		self.tableWidget.setColumnWidth(6,size/3/1)
		self.tableWidget.setColumnWidth(7,size/3/1)
		
		#return size
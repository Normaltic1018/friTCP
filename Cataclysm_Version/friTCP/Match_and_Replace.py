from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox,QLineEdit,QAbstractItemView, QAction, QMenu
from PyQt5.QtGui import QStandardItemModel,QStandardItem, QPixmap,QIcon, QRegExpValidator, QCursor, QResizeEvent
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal, pyqtSlot
from core_func import *

match_and_replace_add_Ui_MainWindow, match_and_replace_add_QtBaseClass = uic.loadUiType("match_and_replace_add.ui")

class Match_and_Replace():
	#arg0 = self.ui.tableWidget_MatchAndReplace
	
	def __init__(self, tableWidget_MatchAndReplace):
		# data init
		self.tableWidget = tableWidget_MatchAndReplace
		self.data_list = []
		
		# tablewidget event init
		self.tableWidget_right_click()		
		
	def add(self, data_structure):
		self.data_list.append(data_structure)
				
	def remove(self, idx):
		del self.data_list[idx-1]
		
	def get_list(self):
		return self.data_list
		
		
	#gui
	def add_btn_clicked(self):
		print("add clicked!")
		
		my_list = []
		my_list.append(self.ui.name.text())
		my_list.append(self.ui.function.currentText())
		my_list.append(self.ui.ip.text())
		my_list.append(self.ui.port.text())
		my_list.append(self.ui.match.text())
		my_list.append(self.ui.replace.text())
		self.add(my_list)
		
		#show list
		numRows = self.tableWidget.rowCount()
		self.tableWidget.insertRow(numRows)
		
		self.tableWidget.setItem(numRows, 0, QTableWidgetItem(str(self.ui.name.text())))
		self.tableWidget.setItem(numRows, 1, QTableWidgetItem(str(self.ui.name.text())))
		self.tableWidget.setItem(numRows, 2, QTableWidgetItem(str(self.ui.function.currentText())))
		self.tableWidget.setItem(numRows, 3, QTableWidgetItem(str(self.ui.ip.text())))
		self.tableWidget.setItem(numRows, 4, QTableWidgetItem(str(self.ui.port.text())))
		self.tableWidget.setItem(numRows, 5, QTableWidgetItem(str(self.ui.match.text())))
		self.tableWidget.setItem(numRows, 6, QTableWidgetItem(str(self.ui.replace.text())))
		
		print(numRows)
		print(self.data_list)
		self.main.close()

	def cancel_btn_clicked(self):
		print("cancel clicked!")
		self.main.close()
		
	def open_window(self):
		print("open_window called!")
		# ui init ## window text clear를 시키기 위해 open 할때 ui를 새로 호출함
		self.main = QMainWindow()
		self.ui = match_and_replace_add_Ui_MainWindow()
		self.ui.setupUi(self.main)
		
		# window event init
		
		self.ui.add_btn.clicked.connect(self.add_btn_clicked)
		self.ui.cancel_btn.clicked.connect(self.cancel_btn_clicked)
		
		self.main.show()

	def tableWidget_right_click(self):
		self.tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		add = QAction("add", self.tableWidget)
		remove = QAction("remove", self.tableWidget)
		self.tableWidget.addAction(add)
		self.tableWidget.addAction(remove)		
		add.triggered.connect(self.tableWidget_right_click_add_event)
		remove.triggered.connect(self.tableWidget_right_click_remove_event)
		
	def tableWidget_right_click_add_event(self):
		self.open_window()
	
	def tableWidget_right_click_remove_event(self):
		# get mouse pos
		pos = QCursor.pos() # PyQt5.QtCore.QPoint(262, 215)
		
		row = self.tableWidget.rowAt(self.tableWidget.viewport().mapFromGlobal(pos).y())
		print(row)
		
		if(row>-1):
			
			self.send_packet_to_Repeater(row)	
	
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
		
	def resize(self):
		# match and replace column size init
		size = self.tableWidget.width()
		#default minimum size 978.. but initial size 622
		if(size < 978):
			size = 978
		self.tableWidget.setColumnWidth(0,size/3/5/1)
		self.tableWidget.setColumnWidth(1,size/3/5/1)
		self.tableWidget.setColumnWidth(2,size/3/5/1)
		self.tableWidget.setColumnWidth(3,size/3/5/1)
		self.tableWidget.setColumnWidth(4,size/3/5/1)
		self.tableWidget.setColumnWidth(5,size/3/1)
		self.tableWidget.setColumnWidth(6,size/3/1)
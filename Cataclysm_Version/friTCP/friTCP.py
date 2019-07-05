import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QHeaderView,QTableWidget, QMessageBox
from PyQt5.QtGui import QStandardItemModel,QStandardItem, QPixmap,QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from core_func import *
from normaltic_splash import Splash
from core_gui import MyWindow
import time
"""
class ThreadProgress(QThread):
	mysignal = pyqtSignal(int)
	def __init__(self,app,parent=None):
		QThread.__init__(self, parent)
		self.app = app
		self.finish_flag = False
	def run(self):
		i = 0
		
		t = time.time()
        while time.time() < t + 0.1:
           app.processEvents()
		
		t = time.time()
		while i<101:
			#time.sleep(0.1)
			self.app.processEvents()
			self.mysignal.emit(i)
			i += 1
			
		self.mysignal.emit(i)
		
	def onFinished(self):
		self.finish_flag = True
	"""	
			
if __name__ == '__main__':

	app = QApplication(sys.argv)
	splash_window = Splash()
	splash_window.show()
	
	# splash 표현용 (로딩과정)
	for i in range(1, 51):
		splash_window.ui.progressBar.setValue(i*2)
		t = time.time()
		while time.time() < t + 0.1:
			app.processEvents()
		   
	time.sleep(1)
	splash_window.close()
	
	# Main 윈도우 실행
	main_window = MyWindow()
	main_window.show()

	sys.exit(app.exec_())
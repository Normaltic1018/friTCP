import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import time
from core_gui import MyWindow

FROM_SPLASH,_ = uic.loadUiType("pica_splash.ui")

class Splash(QMainWindow):
	def __init__(self, parent = None):
		super(Splash, self).__init__(parent)
		#QMainWindow.__init__(self)
		self.ui = FROM_SPLASH()
		self.ui.setupUi(self)
		
		self.setWindowFlags(Qt.FramelessWindowHint)
		pixmap = QPixmap("resource/splash.png")
		movie = QMovie("resource/pica.gif")
		
		self.ui.splah_image.setMovie(movie)
		movie.start()
		#self.ui.splah_image.setPixmap(pixmap.scaled(350, 300))
		
	def run_splash(self):
		progress = ThreadProgress(self)
		progress.mysignal.connect(self.progress)
		progress.start()
        
	@pyqtSlot(int)
	def progress(self, i):
		self.ui.progressBar.setValue(i)
		if i == 100:
			return

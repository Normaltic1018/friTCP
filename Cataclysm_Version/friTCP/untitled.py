# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 782)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/mew.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget_tab = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("D2Coding")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget_tab.setFont(font)
        self.tabWidget_tab.setObjectName("tabWidget_tab")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tableWidget_procList = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget_procList.setGeometry(QtCore.QRect(20, 90, 980, 601))
        self.tableWidget_procList.setMaximumSize(QtCore.QSize(980, 601))
        font = QtGui.QFont()
        font.setFamily("D2Coding ligature")
        font.setPointSize(12)
        self.tableWidget_procList.setFont(font)
        self.tableWidget_procList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_procList.setObjectName("tableWidget_procList")
        self.tableWidget_procList.setColumnCount(2)
        self.tableWidget_procList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_procList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_procList.setHorizontalHeaderItem(1, item)
        self.widget = QtWidgets.QWidget(self.tab_1)
        self.widget.setGeometry(QtCore.QRect(22, 12, 981, 92))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_pid = QtWidgets.QLabel(self.widget)
        self.label_pid.setObjectName("label_pid")
        self.horizontalLayout.addWidget(self.label_pid)
        self.lineEdit_pid_input = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_pid_input.setMaximumSize(QtCore.QSize(9777215, 16777215))
        self.lineEdit_pid_input.setObjectName("lineEdit_pid_input")
        self.horizontalLayout.addWidget(self.lineEdit_pid_input)
        self.pushButton_hook = QtWidgets.QPushButton(self.widget)
        self.pushButton_hook.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_hook.setObjectName("pushButton_hook")
        self.horizontalLayout.addWidget(self.pushButton_hook)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_refresh = QtWidgets.QPushButton(self.widget)
        self.pushButton_refresh.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.tabWidget_tab.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_tab.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidget_tab, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        self.tabWidget_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "friTCP"))
        item = self.tableWidget_procList.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "PID"))
        item = self.tableWidget_procList.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Process Name"))
        self.label_pid.setText(_translate("MainWindow", "PID"))
        self.pushButton_hook.setText(_translate("MainWindow", "HOOK"))
        self.pushButton_refresh.setText(_translate("MainWindow", "Refresh"))
        self.tabWidget_tab.setTabText(self.tabWidget_tab.indexOf(self.tab_1), _translate("MainWindow", "Process"))
        self.tabWidget_tab.setTabText(self.tabWidget_tab.indexOf(self.tab_2), _translate("MainWindow", "Proxy"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


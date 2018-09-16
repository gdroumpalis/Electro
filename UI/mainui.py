# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/terminux/Documents/Projects/Electro/Resources/mainui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startpushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.startpushbutton.setGeometry(QtCore.QRect(10, 10, 94, 34))
        self.startpushbutton.setObjectName("startpushbutton")
        self.stoppushbutton = QtWidgets.QPushButton(self.centralwidget)
        self.stoppushbutton.setGeometry(QtCore.QRect(110, 10, 94, 34))
        self.stoppushbutton.setObjectName("stoppushbutton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Plot_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_Plot_File.setObjectName("actionOpen_Plot_File")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionOpen_Plot_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Electro"))
        self.startpushbutton.setText(_translate("MainWindow", "Start"))
        self.stoppushbutton.setText(_translate("MainWindow", "Stop"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_Plot_File.setText(_translate("MainWindow", "Open Plot File"))
        self.actionClose.setText(_translate("MainWindow", "Close"))


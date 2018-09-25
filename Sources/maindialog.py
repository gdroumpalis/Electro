from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QListWidgetItem, QMessageBox, QFileDialog
import UI.mainui
from Utilities.GlobalUtilities import *
from Sources.settingsdialog import SettingUI
from subprocess import check_call
import os


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.selecteddevice = None
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.initializeelectro()
        self.connectuicomponetstosignal()
        self.attachkeyboardshortcuts()
        self.initializewidgets()

    def initializewidgets(self):
        self.ui.customnamecheckbox.setChecked(False)
        self.ui.filename.setEnabled(False)
        self.ui.customnamecheckbox_2.setChecked(False)
        self.ui.filename2.setEnabled(False)

    def connectuicomponetstosignal(self):
        connect(self.ui.actionClose.triggered, self.closeapplication)
        connect(self.ui.actionopen_settings.triggered, self.opensettingsdialog)
        connect(self.ui.addhandlerbutton.clicked, self.addhandler)
        connect(self.ui.removehandlerbutton.clicked, self.removehandler)
        connect(self.ui.actionRefresh_Devices.triggered, self.initializeelectro)
        connect(self.ui.actionClear_Device_List.triggered, self.fillcombowithnone)
        connect(self.ui.filepathtoolbutton.clicked, self.selectfilepath)
        connect(self.ui.filepathtoolbutton_2.clicked, self.selecteddevice2)
        connect(self.ui.customnamecheckbox.clicked , self.setcustomfilenameenabled)
        connect(self.ui.customnamecheckbox_2.clicked , self.setcustomfilenameenabled2)
    def attachkeyboardshortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")
        self.ui.actionopen_settings.setShortcut("ctrl+p")
        self.ui.actionRefresh_Devices.setShortcut("ctrl+shift+r")

    def closeapplication(self):
        self.close()

    def opensettingsdialog(self):
        settingsdialog = SettingUI(maindlg=self)
        ShowDialog(settingsdialog)

    def initializeelectro(self):
        check_call("dmesg | grep tty|grep USB|rev|awk '{print $1}'|rev > devices.txt", shell=True)
        with open("devices.txt", "r") as f:
            devices = f.readlines()
        if len(devices) > 0:
            self.clearcombo()
            for dev in devices:
                self.deviceaddtocombo(dev)
        else:
            self.fillcombowithnone()

    def deviceaddtocombo(self, dev):
        self.ui.selecteddevicecombobox.addItem("/dev/" + dev.replace("\n", ""))

    def fillcombowithnone(self):
        self.clearcombo()
        self.ui.selecteddevicecombobox.addItem("None")

    def clearcombo(self):
        self.ui.selecteddevicecombobox.clear()

    def addhandler(self):
        # test = QListElectroItem()
        # test.setText("hello"+str(self.counter))
        # test.Metallica = "lalalalalalalalal" + str(self.counter)
        # self.counter+= 1
        # self.ui.handlerslist.addItem(test)
        pass

    def removehandler(self):
        # test = self.ui.handlerslist.takeItem(self.ui.handlerslist.currentRow())
        # del test
        pass

    def printmessage(self):
        # mb  = QMessageBox()
        # mb.setText(self.ui.handlerslist.currentItem().Metallica)
        # mb.exec_()
        pass

    def selectfilepath(self):
        self.ui.filepathlineedit.setText(str(QFileDialog.getExistingDirectory(self, "Select Save path")))

    def selecteddevice2(self):
        self.ui.filepathlineedit_2.setText(str(QFileDialog.getExistingDirectory(self, "Select Save path")))

    def setcustomfilenameenabled2(self):
        self.ui.filename2.setEnabled(self.ui.customnamecheckbox_2.isChecked())

    def setcustomfilenameenabled(self):
        self.ui.filename.setEnabled(self.ui.customnamecheckbox.isChecked())
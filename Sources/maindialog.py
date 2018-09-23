from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import UI.mainui
from Utilities.GlobalUtilities import *
from Sources.settingsdialog import SettingUI
from subprocess import check_call
import os

class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.devices = list()
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.startdevicesinitialization()
        self.connectuicomponetstosignal()
        self.attachkeyboardshortcuts()

    def connectuicomponetstosignal(self):
        connect(self.ui.actionClose.triggered, self.closeapplication)
        connect(self.ui.actionopen_settings.triggered, self.opensettingsdialog)

    def attachkeyboardshortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")
        self.ui.actionopen_settings.setShortcut("ctrl+p")

    def closeapplication(self):
        self.close()

    def opensettingsdialog(self):
        settingsdialog = SettingUI()
        ShowDialog(settingsdialog)

    def startdevicesinitialization(self):
        check_call("dmesg | grep tty|grep USB|rev|awk '{print $1}'|rev > devices.txt",shell=True)
        devices = list()
        with open("devices.txt","r") as f:
            devices = f.readlines()
        for dev in devices:
            self.devices.append("/dev/"+dev.replace("\n",""))

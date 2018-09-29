from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QListWidgetItem, QMessageBox, QFileDialog
import UI.mainui
from Utilities.GlobalUtilities import *
from Sources.settingsdialog import SettingUI
from subprocess import check_call, call
import os


# TODO See if RunsOnRaspberry could be readonly
# TODO test renderer with timer
# TODO See What is going on with Handlers


class MainUI(QMainWindow):
    RunsOnRaspberry = False

    def __init__(self, rasp):
        """

        :type runsonraspberry: bool
        """
        super().__init__()
        self.ui = UI.mainui.Ui_MainWindow()
        MainUI.RunsOnRaspberry = rasp
        self.ui.setupUi(self)
        self.initializeMainWindowSize()
        self.initializeelectro()
        self.connectuicomponetstosignal()
        self.attachkeyboardshortcuts()
        self.initializewidgets()

    def initializeMainWindowSize(self):
        if not MainUI.RunsOnRaspberry:
            self.resize(QSize(1600, 900))

    def initializewidgets(self):
        self.ui.customnamecheckbox.setChecked(False)
        self.ui.filename.setEnabled(False)
        self.ui.customnamecheckbox_2.setChecked(False)
        self.ui.filename2.setEnabled(False)
        self.ui.filepathlineedit.setEnabled(False)
        self.ui.filepathtoolbutton.setEnabled(False)
        self.ui.customnamecheckbox.setEnabled(False)

    def connectuicomponetstosignal(self):
        connect(self.ui.actionClose.triggered, self.closeapplication)
        connect(self.ui.actionopen_settings.triggered, self.opensettingsdialog)
        connect(self.ui.addhandlerbutton.clicked, self.addhandler)
        connect(self.ui.removehandlerbutton.clicked, self.removehandler)
        connect(self.ui.actionRefresh_Devices.triggered, self.initializeelectro)
        connect(self.ui.actionClear_Device_List.triggered, self.fillcombowithnone)
        connect(self.ui.filepathtoolbutton.clicked, self.selectfilepath)
        connect(self.ui.filepathtoolbutton_2.clicked, self.selecteddevice2)
        connect(self.ui.customnamecheckbox.clicked, self.setcustomfilenameenabled)
        connect(self.ui.customnamecheckbox_2.clicked, self.setcustomfilenameenabled2)
        connect(self.ui.actionStart_Plotting.triggered, self.startplotting)
        connect(self.ui.filecheckbox.clicked, self.setfilepathenabled)

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
        if MainUI.RunsOnRaspberry:
            self.ui.selecteddevicecombobox.addItem(dev.replace("\n"))
        else:
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
        self.ui.filename.setEnabled(self.ui.customnamecheckbox.isChecked() & self.ui.filecheckbox.isChecked())

    def setfilepathenabled(self):
        self.ui.filepathlineedit.setEnabled(self.ui.filecheckbox.isChecked())
        self.ui.filepathtoolbutton.setEnabled(self.ui.filecheckbox.isChecked())
        self.ui.customnamecheckbox.setEnabled(self.ui.filecheckbox.isChecked())
        self.ui.filename.setEnabled(self.ui.filecheckbox.isChecked() and self.ui.customnamecheckbox.isChecked())

    def startplotting(self):
        if self.ui.selecteddevicecombobox.findText("None"):
            selectedtab = self.ui.tabWidget.currentWidget()
            if selectedtab is self.ui.liveplottingtab:
                self.startliveplotting()
            elif selectedtab is self.ui.samplingtab:
                self.startsampling()
            elif selectedtab is self.ui.handlerslist:
                self.startmonitoring()
            else:
                print("unknown tab selected")
        else:
            self.showmessagebox("There is no proper device selected")

    def startliveplotting(self):
        # call("python35 ../Renderer/MRenderer.py ",args=,shell=True)
        # TODO finish implementation off plotting. See whats going on with arguments
        if self.ui.loggingcheckbox.isChecked() or self.ui.loggingcheckbox.isChecked() or self.ui.filecheckbox.isChecked():  # todo check if this is right
            call([self.getpythonversion(), "../Renderer/MRenderer.py", self.ui.selecteddevicecombobox.currentText(),
                  self.ui.speedspinbox.text(), self.ui.filename.text()])

    def startsampling(self):
        # TODO Implement sampling function
        pass

    def startmonitoring(self):
        # TODO implement monitoring.. this is affected by handlers.
        pass

    def getpythonversion(self) -> str:
        if MainUI.RunsOnRaspberry:
            return "python3"
        else:
            return "python35"

    def showmessagebox(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

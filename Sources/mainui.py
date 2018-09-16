from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import UI.mainui
from Utilities.EventConnector import *
from Sources.RendererUtilities import *
from Renderer.MRenderer import *
class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectuicomponetstosignal()
        self.attachkeyboardshortcuts()


    def connectuicomponetstosignal(self):
        connect(self.ui.actionClose.triggered, self.closeapplication)
        connect(self.ui.startpushbutton.clicked , self.startthread)
        connect(self.ui.stoppushbutton.clicked,self.stopmethod)

    def attachkeyboardshortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")

    def closeapplication(self):
        self.close()

    def startthread(self):
        self.rthreadparams = RendererParameters(False, False, 600, 600,"")
        self.rthread = RendererThread(self.rthreadparams )
        connect(self.rthread.finished , self.threadfinished)
        self.rthread.start()

    def stopmethod(self):
        self.rthread.abort = True

    def threadfinished(self):
        print("thread finished")
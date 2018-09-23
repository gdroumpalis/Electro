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


    def attachkeyboardshortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")

    def closeapplication(self):
        self.close()

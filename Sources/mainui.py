from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import UI.mainui
import Utilities.EventConnector as EVC


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectuicomponetstosignal()
        self.attachkeyboardshortcuts()

    def connectuicomponetstosignal(self):
        EVC.connect(self.ui.actionClose.triggered, self.closeapplication)

    def attachkeyboardshortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")

    def closeapplication(self):
        self.close()

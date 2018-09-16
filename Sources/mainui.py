from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import UI.mainui
import Utilities.EventConnector as EVC

class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.InitializeFileMenu()

    def InitializeFileMenu(self):
        EVC.connect(self.ui.actionClose.triggered, self.CloseApplication)
        self.ui.actionClose.setShortcut("ctrl+q")

    def CloseApplication(self):
        self.close()
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import UI.mainui
import Utilities.EventConnector as EVC
import Renderer.MRenderer as Megaman


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ConnectUIComponentToEvents()
        self.SetShortcuts()

    def ConnectUIComponentToEvents(self):
        EVC.connect(self.ui.actionClose.triggered, self.CloseApplication)
        EVC.connect(self.ui.test.clicked, self.StartRendering)

    def SetShortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")

    def CloseApplication(self):
        self.close()

    def StartRendering(self):
        Megaman.StatRendering()

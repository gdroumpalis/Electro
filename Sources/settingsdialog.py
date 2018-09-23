

from PyQt5.QtWidgets import QDialog
from UI.settings import Ui_Settings

class SettingUI(QDialog):

    def __init__(self):
        super().__init__()
        self.ui  = Ui_Settings()
        self.ui.setupUi(self)
        self.initializedevicesfromfile()

    def initializedevicesfromfile(self):

            for device in devices:

                self.ui.usbdevicesdropdown.addItem(device)

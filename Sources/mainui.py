from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import UI.mainui
import Utilities.EventConnector as EVC
import Sources.RendererUtilities as rutils
import Renderer.MRenderer as mrenderer
class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI.mainui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectuicomponetstosignal()
        self.attachkeyboardshortcuts()


    def connectuicomponetstosignal(self):
        EVC.connect(self.ui.actionClose.triggered, self.closeapplication)
        EVC.connect(self.ui.startpushbutton.clicked , self.startthread)
        EVC.connect(self.ui.stoppushbutton.clicked,self.stopmethod)

    def attachkeyboardshortcuts(self):
        self.ui.actionClose.setShortcut("ctrl+q")

    def closeapplication(self):
        self.close()

    def startthread(self):
        rthreadparams = rutils.RendererParameters(False, False, 600, 600,"")
        self.cancel = False
        self.rthread = mrenderer.RendererThread(rthreadparams , self.cancel)
        self.rthread.start()

    def stopmethod(self):
        self.rthread.cancel = True
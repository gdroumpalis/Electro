from PyQt5.QtCore import QThread
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import datetime
import Sources.RendererUtilities as rutils


class RendererThread(QThread):

    def __init__(self, rendererparams=rutils.RendererParameters(False, False, 600, 600), cancel=False):
        QThread.__init__(self)
        # self.params = rendererparams
        # self.win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window
        # self.p = self.win.addPlot(title="Temp plot")  # creates empty space for the plot in the window
        # self.p2 = self.win.addPlot(title="Avg Temp Plot")
        # self.curve = self.p.plot()  # create an empty "plot" (a curve to plot)
        # self.curve2 = self.p2.plot()
        # self.windowWidth = 500  # width of the window displaying the curve
        # self.Xm = linspace(0, 0, rendererparams.renderingwindowheigh)  # create array that will contain the relevant time series
        # self.Am = linspace(0, 0, rendererparams.renderingwindowwidth)
        # self.ptr = 1
        self.cancel = cancel

    def run(self):
        try:
            # f = open("log.txt", "w+")
            while not self.cancel:
                self.update()
        finally:
            self.finished()


    def update(self):
        print("testing")


    def finished(self):
        print("finished")

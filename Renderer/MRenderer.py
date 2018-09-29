from enum import Enum

from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import datetime
import sys

class RendererOperationsType(Enum):
    LivePlotting =1
    Sampling = 2
    Handling = 3

def GetOperationMethodFromArgs(argv: int) -> RendererOperationsType:
    type = int(argv[1])
    if type == 1:
        return RendererOperationsType.LivePlotting
    elif type ==2:
        return RendererOperationsType.Sampling
    elif type == 3:
        return RendererOperationsType.Handling


def GetDeviceName(argv):
    return argv[2]


def GetBaudrate(argv):
    if argv[3] == "None":
        return 1200
    else:
        return int(argv[3])


def GetDefaultFilepath(argv):
    if argv[4] == "None":
        return os.path.join(os.getcwd(), "sampling")
    else:
        return argv[4]


def GetDefaultMaxStep(argv):
    if argv[5] == "None":
        return 200
    else:
        return int(argv[5])


RendererOperation = GetOperationMethodFromArgs(sys.argv)  # type: RendererOperationsType

devicename = GetDeviceName(sys.argv)
baudrate = GetBaudrate(sys.argv)
filename = GetDefaultFilepath(sys.argv)
ser = serial.Serial(devicename, baudrate)
maxstep = GetDefaultMaxStep(sys.argv)
timer = QtCore.QTimer()
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window
p = win.addPlot(title="Temp plot")  # creates empty space for the plot in the window
p2 = win.addPlot(title="Avg Temp Plot")
curve = p.plot()  # create an empty "plot" (a curve to plot)
curve2 = p2.plot()
windowWidth = 500  # width of the window displaying the curve
Xm = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
Am = linspace(0, 0, windowWidth)
ptr = 1  # set first x position


# Realtime data plot. Each time this function is called, the data display is updated
def updateforliveplottin(f, logging):
    """
    :type logging: bool
    """
    global curve, curve2, ptr, Xm, Am
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    Am[:-1] = Am[1:]
    value = ser.readline()  # read line (single value) from the serial port
    try:
        Xm[-1] = float(value)  # vector containing the instantaneous values
    except :
        Xm[-1] = 0.0

    if ptr <= 500:
        Am[-1] = sum(Xm) / ptr
    else:
        Am[-1] = sum(Xm) / len(Xm)
    if logging:
        print("current temp:{} , avg temp{}".format(Xm[-1], Am[-1]))
    # f.write("datetime:{} => current temp:{} , avg temp{}\n".format(datetime.datetime.now(), Xm[-1], Am[-1]))
    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 1)  # set x position in the graph to 0
    curve2.setData(Am)
    curve2.setPos(ptr, 1)
    QtGui.QApplication.processEvents()  # you MUST process the plot now


def updateforsampling(f, step):
    global curve, curve2, ptr, Xm, Am
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    Am[:-1] = Am[1:]
    value = ser.readline()  # read line (single value) from the serial port
    Xm[-1] = float(value)  # vector containing the instantaneous values
    if ptr <= 500:
        Am[-1] = sum(Xm) / ptr
    else:
        Am[-1] = sum(Xm) / len(Xm)
    print("current temp:{} , avg temp{}".format(Xm[-1], Am[-1]))
    f.write("datetime:{} => current temp:{} , avg temp{}\n".format(datetime.datetime.now(), Xm[-1], Am[-1]))
    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 1)  # set x position in the graph to 0
    curve2.setData(Am)
    curve2.setPos(ptr, 1)
    step += 1
    QtGui.QApplication.processEvents()  # you MUST process the plot now


def updateforhandling(f):
    global curve, curve2, ptr, Xm, Am
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    Am[:-1] = Am[1:]
    value = ser.readline()  # read line (single value) from the serial port
    Xm[-1] = float(value)  # vector containing the instantaneous values
    if ptr <= 500:
        Am[-1] = sum(Xm) / ptr
    else:
        Am[-1] = sum(Xm) / len(Xm)
    print("current temp:{} , avg temp{}".format(Xm[-1], Am[-1]))
    #f.write("datetime:{} => current temp:{} , avg temp{}\n".format(datetime.datetime.now(), Xm[-1], Am[-1]))
    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 1)  # set x position in the graph to 0
    curve2.setData(Am)
    curve2.setPos(ptr, 1)
    QtGui.QApplication.processEvents()  # you MUST process the plot now


if RendererOperation == RendererOperationsType.LivePlotting:
    timer.timeout.connect(lambda: updateforliveplottin(filename,True))
    timer.start(0)
    print("Plotting Started")
elif RendererOperation == RendererOperationsType.Sampling:
    step = 0
    timer.timeout.connect(lambda: updateforsampling(filename, step))
    timer.setInterval(700)
    timer.start(0)

elif RendererOperation == RendererOperationsType.Handling:
    timer.timeout.connect(lambda: updateforhandling(filename))
    timer.setInterval(700)
    timer.start(0)
else:
    raise Exception("Rendering prosses cannot start")

if __name__ == '__main__':
    pg.QtGui.QApplication.exec_()
    print("Proccess Ended")
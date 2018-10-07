from enum import Enum

from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import datetime
import sys
from threading import Thread


class RenderingThreadLooper:

    def __init__(self, target, timeout=-1, name="Processing_Thread"):
        self.executing = True
        self.runnablemethod = target
        self.timeout = timeout
        self.threadname = name
        self.renderthread = None

    def executiontarget(self):
        if self.timeout == -1:
            while self.executing:
                self.runnablemethod()
        else:
            for i in range(0, self.timeout):
                self.runnablemethod()
                print(i)

    def finishexecution(self):
        self.executing = False
        print(self.renderthread.name + " finished")

    def run(self):
        self.renderthread = Thread(target=self.executiontarget)
        self.renderthread.setName(self.threadname)
        self.renderthread.start()
        print(self.renderthread.name + " started")

    def wait(self):
        self.renderthread.join()

class RendererOperationsType(Enum):
    LivePlotting = 1
    Sampling = 2
    Handling = 3


def releaseresources():
    global f, ser, loopers
    if f is not None:
        f.close()
    ser.close()
    for looper in loopers:
        looper.finishexecution()
    del loopers[:]


def attachloopertogloballooperpool(looper):
    global loopers
    loopers.append(looper)


def GetOperationMethodFromArgs(argv: int) -> RendererOperationsType:
    type = int(argv[1])
    if type == 1:
        return RendererOperationsType.LivePlotting
    elif type == 2:
        return RendererOperationsType.Sampling
    elif type == 3:
        return RendererOperationsType.Handling


def openfilewithproperfilename():
    if GetFileLogging(sys.argv):
        return open(GetDefaultFilepath(sys.argv), "w+")
    else:
        return None


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


def GetTerminalLogging(argv):
    if argv[6] == "None":
        return False
    else:
        if argv[6] == "True":
            return True
        else:
            return False


def GetFileLogging(argv):
    if argv[7] == "None":
        return False
    else:
        if argv[7] == "True":
            return True
        else:
            return False


loopers = []
RendererOperation = GetOperationMethodFromArgs(sys.argv)  # type: RendererOperationsType
terminallogging = GetTerminalLogging(sys.argv)
filelogging = GetFileLogging(sys.argv)
devicename = GetDeviceName(sys.argv)
baudrate = GetBaudrate(sys.argv)
filename = GetDefaultFilepath(sys.argv)
ser = serial.Serial(devicename, baudrate, timeout=0.15)
maxstep = GetDefaultMaxStep(sys.argv)
timer = QtCore.QTimer()
f = openfilewithproperfilename()
print(RendererOperation.name)
### START QtApp #####
if RendererOperation == RendererOperationsType.LivePlotting:
    app = QtGui.QApplication([])  # you MUST do this once (initialize things)
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
def updateforliveplottin(f, logging, filelogging, t):
    """
    :param t:
    :type logging: bool
    """
    global curve, curve2, ptr, Xm, Am, ser
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    Am[:-1] = Am[1:]
    value = ser.readline()  # read line (single value) from the serial port
    try:
        Xm[-1] = float(value)  # vector containing the instantaneous values
    except:
        Xm[-1] = 0.0

    if ptr <= 500:
        Am[-1] = sum(Xm) / ptr
    else:
        Am[-1] = sum(Xm) / len(Xm)
    if logging:
        print("current temp:{} , avg temp{}".format(Xm[-1], Am[-1]))

    if filelogging:
        if not f.closed:
            f.write("datetime:{} => current temp:{} , avg temp{}\n".format(datetime.datetime.now(), Xm[-1], Am[-1]))

    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 1)  # set x position in the graph to 0
    curve2.setData(Am)
    curve2.setPos(ptr, 1)
    QtGui.QApplication.processEvents()  # you MUST process the plot now


def updateforsampling(f):
    global ptr, Xm, Am, ser
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    Am[:-1] = Am[1:]
    value = ser.readline()  # read line (single value) from the serial port
    try:
        Xm[-1] = float(value)  # vector containing the instantaneous values
    except:
        Xm[-1] = 0.0
    if ptr <= 500:
        Am[-1] = sum(Xm) / ptr
    else:
        Am[-1] = sum(Xm) / len(Xm)
    if not f.closed:
        f.write("{0},{1}\n".format(Xm[-1], Am[-1]))
    ptr += 1  # update x position for displaying the curve


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
    # f.write("datetime:{} => current temp:{} , avg temp{}\n".format(datetime.datetime.now(), Xm[-1], Am[-1]))
    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 1)  # set x position in the graph to 0
    curve2.setData(Am)
    curve2.setPos(ptr, 1)
    QtGui.QApplication.processEvents()  # you MUST process the plot now


if RendererOperation == RendererOperationsType.LivePlotting:
    renderlooper = RenderingThreadLooper(lambda: updateforliveplottin(f, terminallogging, filelogging, True),
                                         name="Live Plotting Thread")
    renderlooper.run()
    attachloopertogloballooperpool(renderlooper)
    print("Plotting Started")

elif RendererOperation == RendererOperationsType.Sampling:  # TODO implement those

    renderlooper = RenderingThreadLooper(lambda: updateforsampling(f), timeout=maxstep, name="Sampling Thread")
    attachloopertogloballooperpool(renderlooper)
    renderlooper.run()
    renderlooper.wait()
    print("Sampling started")

elif RendererOperation == RendererOperationsType.Handling:  # TODO implement those
    pass
    # timer.timeout.connect(lambda: updateforhandling(filename))
    # timer.setInterval(700)
    # timer.start(0)
else:
    raise Exception("Rendering prosses cannot start")

if __name__ == '__main__':
    if RendererOperation == RendererOperationsType.LivePlotting:
        pg.QtGui.QApplication.instance().exec_()
        print("UI Proccess Ended")

    releaseresources()  # TODO do not forget to update releasesources method

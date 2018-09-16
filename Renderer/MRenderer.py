from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import datetime
# Create object serial port
# portName = "/dev/ttyUSB0"                      # replace this port name by yours!
# baudrate = 1200
# ser = serial.Serial(portName,baudrate)
#
# ### START QtApp #####
# app = QtGui.QApplication([])            # you MUST do this once (initialize things)
# ####################
#
# win = pg.GraphicsWindow(title="Signal from serial port") # creates a window
# p = win.addPlot(title="Temp plot")  # creates empty space for the plot in the window
# p2 = win.addPlot(title="Avg Temp Plot")
# curve = p.plot()                        # create an empty "plot" (a curve to plot)
# curve2 = p2.plot()
# windowWidth = 500                       # width of the window displaying the curve
# Xm = linspace(0,0,windowWidth)          # create array that will contain the relevant time series
# Am = linspace(0,0,windowWidth)
# ptr = 1                      # set first x position

# Realtime data plot. Each time this function is called, the data display is updated
def update(f,curve,curve2, ptr, Xm , Am):
    # global curve,curve2, ptr, Xm , Am
    Xm[:-1] = Xm[1:]                      # shift data in the temporal mean 1 sample left
    Am[:-1] = Am[1:]
    value = ser.readline()                # read line (single value) from the serial port
    Xm[-1] = float(value)                 # vector containing the instantaneous values
    if ptr<=500:
        Am[-1] = sum(Xm)/ptr
    else:
        Am[-1] = sum(Xm)/len(Xm)
    print("current temp:{} , avg temp{}".format(Xm[-1],Am[-1]))
    f.write("datetime:{} => current temp:{} , avg temp{}\n".format(datetime.datetime.now(),Xm[-1],Am[-1]))
    ptr += 1                              # update x position for displaying the curve
    curve.setData(Xm)                     # set the curve with this data
    curve.setPos(ptr,1)                   # set x position in the graph to 0
    curve2.setData(Am)
    curve2.setPos(ptr,1)
    QtGui.QApplication.processEvents()    # you MUST process the plot now


def StatRendering():
    portName = "/dev/ttyUSB0"  # replace this port name by yours!
    baudrate = 1200
    ser = serial.Serial(portName, baudrate)

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
    ptr = 1
    try:
        f = open("log.txt", "w+")
        while True:
            update(f,curve,curve2, ptr, Xm , Am)
    except KeyboardInterrupt:
        print("finished")
    finally:
        ser.close()
        f.close()
        pg.QtGui.QApplication.exec_()


### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot


### END QtApp ####
#pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
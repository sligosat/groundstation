from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from communication import Communication
import math
from dataBase import data_base
from PyQt5.QtWidgets import QPushButton

pg.setConfigOption('background', (34,39,46))
pg.setConfigOption('foreground', (79,89,99))
# Interface variables
app = QtGui.QApplication([])
view = pg.GraphicsView()
Layout = pg.GraphicsLayout()
view.setCentralItem(Layout)
view.show()
view.setWindowTitle('Ground Station')
view.resize(960, 540)

# declare object for serial Communication
ser = Communication()
# declare object for storage in CSV
data_base = data_base()
# Fonts for text items
font = QtGui.QFont()
font.setPixelSize(90)


# Title at top
text = """
Ground Station Developed by SligoSat (https://github.com/sligosat)
"""
Layout.addLabel(text, col=1, colspan=19)
Layout.nextRow()

Layout.nextRow()
# Save data buttons

# buttons style
style = "background-color:rgb(77,138,210);color:rgb(0,0,0);font-size:14px;"

lb = Layout.addLayout(colspan=25)
proxy = QtGui.QGraphicsProxyWidget()
save_button = QtGui.QPushButton('Start storage')
save_button.setStyleSheet(style)
save_button.clicked.connect(data_base.start)
proxy.setWidget(save_button)
lb.addItem(proxy)
lb.nextCol()


proxy2 = QtGui.QGraphicsProxyWidget()
end_save_button = QtGui.QPushButton('Stop storage')
end_save_button.setStyleSheet(style)
end_save_button.clicked.connect(data_base.stop)
proxy2.setWidget(end_save_button)
lb.addItem(proxy2)


Layout.nextRow()

# Altitude graph
l1 = Layout.addLayout(colspan=25, rowspan=2)
l11 = l1.addLayout(rowspan=1, border=(83, 83, 83))
p1 = l11.addPlot(title="Altitude (m)")
altitude_plot = p1.plot(pen=(29, 185, 84))
altitude_data = np.linspace(0, 0, 30)
ptr1 = 0


def update_altitude(value_chain):
    global altitude_plot, altitude_data,  ptr1
    altitude_data[:-1] = altitude_data[1:]
    altitude_data[-1] = float(value_chain[1])
    ptr1 += 1
    altitude_plot.setData(altitude_data)
    altitude_plot.setPos(ptr1, 0)



# Speed graph
p2 = l11.addPlot(title="Speed (m/s)")
vel_plot = p2.plot(pen=(29, 185, 84))
vel_data = np.linspace(0, 0, 30)
ptr6 = 0
vx = 0
vy = 0
vz = 0
vel = 0


def update_vel(value_chain):
    global vel_plot, vel_data, ptr6, vx, vy, vz, vel
    # 500 
    i = 0
    if(i == 0):
        vzo = float(value_chain[10])
        i += 1

    vx += (float(value_chain[8])) * 500
    vy += (float(value_chain[9])) * 500
    vz += (float(value_chain[10]) - vzo) * 500
    sum = math.pow(vx, 2) + math.pow(vy, 2) + math.pow(vz, 2)
    vel = math.sqrt(sum)
    vel_data[:-1] = vel_data[1:]
    vel_data[-1] = vel
    ptr6 += 1
    vel_plot.setData(vel_data)
    vel_plot.setPos(ptr6, 0)


l1.nextRow()
l12 = l1.addLayout(rowspan=1, border=(90, 90, 90))

# Acceleration graph
acc_graph = l12.addPlot(title="Accelerations (m/s??)")
# adding legend
acc_graph.addLegend()
acc_graph.hideAxis('bottom')
accX_plot = acc_graph.plot(pen=(102, 252, 241), name="X")
accY_plot = acc_graph.plot(pen=(29, 185, 84), name="Y")
accZ_plot = acc_graph.plot(pen=(203, 45, 111), name="Z")

accX_data = np.linspace(0, 0)
accY_data = np.linspace(0, 0)
accZ_data = np.linspace(0, 0)
ptr2 = 0


def update_acc(value_chain):
    global accX_plot, accY_plot, accZ_plot, accX_data, accY_data, accZ_data, ptr2
    accX_data[:-1] = accX_data[1:]
    accY_data[:-1] = accY_data[1:]
    accZ_data[:-1] = accZ_data[1:]

    accX_data[-1] = float(value_chain[8])
    accY_data[-1] = float(value_chain[9])
    accZ_data[-1] = float(value_chain[10])
    ptr2 += 1

    accX_plot.setData(accX_data)
    accY_plot.setData(accY_data)
    accZ_plot.setData(accZ_data)

    accX_plot.setPos(ptr2, 0)
    accY_plot.setPos(ptr2, 0)
    accZ_plot.setPos(ptr2, 0)


# Gyro graph
gyro_graph = l12.addPlot(title="Gyro")
gyro_graph.hideAxis('bottom')
# adding legend
gyro_graph.addLegend()
pitch_plot = gyro_graph.plot(pen=(102, 252, 241), name="Pitch")
roll_plot = gyro_graph.plot(pen=(29, 185, 84), name="Roll")
yaw_plot = gyro_graph.plot(pen=(203, 45, 111), name="Yaw")

pitch_data = np.linspace(0, 0)
roll_data = np.linspace(0, 0)
yaw_data = np.linspace(0, 0)
ptr3 = 0


def update_gyro(value_chain):
    global pitch_plot, roll_plot, yaw_plot, pitch_data, roll_data, yaw_data, ptr3
    pitch_data[:-1] = pitch_data[1:]
    roll_data[:-1] = roll_data[1:]
    yaw_data[:-1] = yaw_data[1:]

    pitch_data[-1] = float(value_chain[5])
    roll_data[-1] = float(value_chain[6])
    yaw_data[-1] = float(value_chain[7])

    ptr3 += 1

    pitch_plot.setData(pitch_data)
    roll_plot.setData(roll_data)
    yaw_plot.setData(yaw_data)

    pitch_plot.setPos(ptr3, 0)
    roll_plot.setPos(ptr3, 0)
    yaw_plot.setPos(ptr3, 0)


# Pressure Graph
pressure_graph = l12.addPlot(title="Barometric pressure")
pressure_plot = pressure_graph.plot(pen=(102, 252, 241))
pressure_data = np.linspace(0, 0, 30)
ptr4 = 0


def update_pressure(value_chain):
    global pressure_plot, pressure_data,  ptr4
    pressure_data[:-1] = pressure_data[1:]
    pressure_data[-1] = float(value_chain[4])
    ptr4 += 1
    pressure_plot.setData(pressure_data)
    pressure_plot.setPos(ptr4, 0)


# Temperature graph
graf_temp = l12.addPlot(title="Temperature (??c)")
temp_plot = graf_temp.plot(pen=(29, 185, 84))
temp_data = np.linspace(0, 0, 30)
ptr5 = 0


def update_temp(value_chain):
    global temp_plot, temp_data,  ptr5
    temp_data[:-1] = temp_data[1:]
    temp_data[-1] = float(value_chain[3])
    ptr5 += 1
    temp_plot.setData(temp_data)
    temp_plot.setPos(ptr5, 0)




def update():
    try:
        value_chain = []
        value_chain = ser.getData()
        update_altitude(value_chain)
        update_vel(value_chain)
        update_acc(value_chain)
        update_gyro(value_chain)
        update_pressure(value_chain)
        update_temp(value_chain)
        data_base.guardar(value_chain)
    except IndexError:
        print('starting, please wait a moment')



if(ser.isOpen()) or (ser.dummyMode()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(500)
else:
    print("something is wrong with the update call")
# Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

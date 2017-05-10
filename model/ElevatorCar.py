import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
'''
It is the second version:

'''


class ElevatorCar(QtGui.QLabel):
    """
    elevatorcar inherited from the Qlabel and add a method to move up and down
    """
    # move_signal = QtCore.pyqtSignal(bool)

    def __init__(self, order, location, parent=None, direction=None):
        super(ElevatorCar, self).__init__(parent)
        self.order = order
        self.direction = direction
        self.location = location  # the location would be sorted as 4
        self.height = self.geometry().height()  # set the hight here to male it convenient to get in the moving function in redefineUI.py
        self.thread = EleMove(self, self.direction)
        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        # self.setText("EleBox %s" % str(self.order))
        self.setText("+*" * self.order)
        # self.setAlignment()
        self.setAlignment(QtCore.Qt.AlignCenter)

    def moveUp(self):
        self.direction = 'up'
        self.thread.exit()
        self.thread.start()

    def moveDown(self):
        self.direction = 'down'
        self.thread.exit()
        self.thread.start()

    def moveStop(self):
        self.thread.exit()


class EleMove(QtCore.QThread):
    '''
    changelog:
        add the method to change the direction
    '''
    # handle_id_signal = QtCore.pyqtSignal(QtCore.QThread)
    obj_signal = pyqtSignal(ElevatorCar)

    def __init__(self, ele, direction):
        super(EleMove, self).__init__()
        self.ele = ele
        self.direction = direction

    def run(self):
        for i in range(800):
            self.obj_signal.emit(self.ele)
            time.sleep(0.05)

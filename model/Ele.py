import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

'''
It is the second version:

'''


class ElevatorCar(QtGui.QLabel):
    """
    elevatorcar inherited from the Qlabel and add a method to move up and down
    """
    y_loc_signal = pyqtSignal(int)
    # is_move_signal = pyqtSignal(bool)
    is_move_signal = pyqtSignal()
    not_move_signal = pyqtSignal()
    des_signal = pyqtSignal(int)
    obj_signal = pyqtSignal(QObject)
    phase1_signal = pyqtSignal() # the signal after one move is done
    step1_1_signal = pyqtSignal()  # the signal after one step1_1 is done
    step1_2_signal = pyqtSignal()  # the signal after one step1_2 is done, the step1_2 is specificly to the ele in the latter place of a route that needs ele exchange
    def __init__(self, order, location, parent=None, direction=None, ele_name=None, des=None):
        super(ElevatorCar, self).__init__(parent)
        self.order = order
        self.des = des
        self.ele_name = ele_name
        self.direction = direction
        self.location = location  # the location would be sorted as 4
        # self.is_move_signal.emit(False)
        self.height = self.geometry().height()  # set the hight here to male it convenient to get in the moving function in redefineUI.py
        # self.thread = EleMove(self, self.direction)
        self._thread = EleMove(ele=self)
        self.ready = False
        # self.thread.setAutoDelete(False)
        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        # self.setText("EleBox %s" % str(self.order))
        self.setText("*" * self.order)
        # self.setAlignment()
        self.setAlignment(QtCore.Qt.AlignCenter)

    def moveUp(self):
        self.direction = 'up'
        # self._thread.exit()
        # self._thread.terminate()
        if not self._thread.isRunning():
            self._thread.start()

    def moveDown(self):
        self.direction = 'down'
        # self._thread.exit()
        # self._thread.terminate()
        if not self._thread.isRunning():
            self._thread.start()

    def moveStop(self):
        self.direction = 'stop'
        # self._thread.terminate()
        # self._thread.exit()
        if not self._thread.isRunning():
            self._thread.start()

    @property
    def ele_thread(self):
        return self._thread

    @ele_thread.setter
    def ele_thread(self, new_ele):
        self._thread = EleMove(ele=new_ele)

    def reset_thread(self):
        self._thread = EleMove(ele=self)

    def set_ready(self):
        self.ready = True

    def reset_signal(self):
        # reset_signal
        ElevatorCar.phase1_signal = pyqtSignal()  # the signal after one move is done
        ElevatorCar.step1_1_signal = pyqtSignal()  # the signal after one step1_1 is done
        ElevatorCar.step1_2_signal = pyqtSignal()  # the signal after one step1_2 is done

    def getLocation(self):
        '''
        get the floor the elecar is in
        '''
        fr_num = 60
        f_height = 590
        y_loc = self.geometry().y()
        return self._calculateFloor(fr_num, f_height, y_loc)

    def new_move(self, x, y):
        '''
        rewrite the method to emit the y_loc_signal when moving
        '''
        self.move(x, y)
        self.y_loc_signal.emit(self.geometry().y())
        self.is_move_signal.emit()
        self.des_signal.emit(self.des)

    def y_loc(self):
        y_loc = self.geometry().y()
        self.y_loc_signal.emit(y_loc)

    def whether_move(self):
        y_1 = self.geometry().y()
        time.sleep(0.1)
        y_2 = self.geometry().y()
        if y_1 == y_2:
            self.not_move_signal.emit()



    def _calculateFloor(self, fr_num, f_height, loc_y):
        # ############### this method should changed cause it is too dependent with other variables############
        # the simple way, just one line
        # return sum(map(lambda j: (fr_num - j) if (50 + f_height / fr_num * j) <= loc_y < (50 + f_height / fr_num * (j + 1)) else 0, range(fr_num)))


        for i in range(1, fr_num + 1):
            # if y is between (30 + (60-(i+1)*10), 30 + (60-i)*10], then it is in ith floor
            L = 30 + f_height / (fr_num - 1) * (fr_num - (i + 1))
            R = 30 + f_height / (fr_num - 1) * (fr_num - i)
            if L < loc_y <= R:
                return i
        # a more concrete way；

        # for i in range(1, fr_num + 1):
        #     if i == 1:
        #         # make sure the 1st floor displayed properly
        #         L = 30 + f_height / fr_num * (fr_num - i + 1) + 1
        #     U = 30 + f_height / fr_num * (fr_num - (i + 1) + 1)
        #     # print(L)
        #     # print(U)
        #     if U <= loc_y < L:
        #         return i


class EleMove(QtCore.QThread):
    '''
    changelog:
        add the method to change the direction
    '''
    # handle_id_signal = QtCore.pyqtSignal(QtCore.QThread)
    # obj_signal = pyqtSignal(ElevatorCar)
    is_running_signal = pyqtSignal(bool)
    begin_signal = pyqtSignal()
    done_signal = pyqtSignal()

    def __init__(self, ele):
        super(EleMove, self).__init__()
        self.ele = ele
        self.direction = ele.direction

    def run(self):
        self.begin_signal.emit()
        # print('y in thread is {}, and the expected y should be {}'.format(self.ele.geometry().y(), self.ele.des))
        # stop the thread if direction is 'stop'
        if self.direction == 'stop':
            self.done_signal.emit()
            return
        # else:
        #     self.is_running_signal.emit(True)
        #     # self.obj_signal.emit(self.ele)
        #     for i in range(100):
        #         self.obj_signal.emit(self.ele)
        #
        #         time.sleep(0.05)

        else:
            self.is_running_signal.emit(True)
            while self.ele.des != self.ele.geometry().y():
                # self.obj_signal.emit(self.ele)
                self.ele.obj_signal.emit(self.ele)
                # print('the signal is emitted')
                time.sleep(0.05)
            if self.ele.direction == 'up':
                self.ele.obj_signal.emit(self.ele)
            # self.obj_signal.emit(self.ele)
            print('y in thread is {}, and the expected y should be {}'.format(self.ele.geometry().y(), self.ele.des))
            self.done_signal.emit()
            return
#
# class WorkerSignals(QObject):
#     obj_signal = pyqtSignal(ElevatorCar)
#     is_running_signal = pyqtSignal(bool)
#     begin_signal = pyqtSignal()
#     done_signal = pyqtSignal()
#
#
# class EleMove(QtCore.QRunnable):
#     '''
#     changelog:
#         add the method to change the direction
#     '''
#     # handle_id_signal = QtCore.pyqtSignal(QtCore.QThread)
#
#     def __init__(self, ele):
#         super(EleMove, self).__init__()
#         self.ele = ele
#         self.direction = ele.direction
#         self.signals = WorkerSignals()
#
#     def run(self):
#         self.signals.begin_signal.emit()
#         # print('y in thread is {}, and the expected y should be {}'.format(self.ele.geometry().y(), self.ele.des))
#         # stop the thread if direction is 'stop'
#         if self.direction == 'stop':
#             self.signals.done_signal.emit()
#             return
#         # else:
#         #     self.is_running_signal.emit(True)
#         #     # self.obj_signal.emit(self.ele)
#         #     for i in range(100):
#         #         self.obj_signal.emit(self.ele)
#         #
#         #         time.sleep(0.05)
#
#         else:
#             self.signals.is_running_signal.emit(True)
#             # self.obj_signal.emit(self.ele)
#             # self.obj_signal.emit(self.ele)
#             # while int(self.ele.des) != int(self.ele.geometry().y()):
#             # while self.ele.des != self.ele.geometry().y():
#             # print('before loop, y in thread is {}, and the expected y should be {}'.format(self.ele.geometry().y(), self.ele.des))
#             # print(self.ele.direction)
#             while self.ele.des != self.ele.geometry().y():
#                 self.signals.obj_signal.emit(self.ele)
#                 # print('the signal is emitted')
#                 time.sleep(0.05)
#             if self.ele.direction == 'up':
#                 self.signals.obj_signal.emit(self.ele)
#             # self.obj_signal.emit(self.ele)
#             print('y in thread is {}, and the expected y should be {}'.format(self.ele.geometry().y(), self.ele.des))
#             self.signals.done_signal.emit()
#             return
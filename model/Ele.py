import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal


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
    phase1_signal = pyqtSignal()  # the signal after one move is done
    phase2_signal = pyqtSignal()  # the signal after one move is done

    # step1_1_signal = pyqtSignal()  # the signal after one step1_1 is done
    # step1_2_signal = pyqtSignal()  # the signal after one step1_2 is done,
    # the step1_2 is specificly to the ele in the latter place of a route that
    # needs ele exchange
    def __init__(self, order, location, parent=None, direction='stop', ele_name=None, des_exg_list=[], max_amount=13,
                 all_ele_status={},
                 **kwargs):
        super(ElevatorCar, self).__init__(parent)
        self.order = order
        self.ele_name = ele_name
        self.direction = direction
        self.max_amount = max_amount  # the maxium people a ele can hold
        self.des_exg_list = des_exg_list  # a list storing the destinations of passengers
        self.location = location  # the location would be sorted as 4
        self.current_amount = 0  # the amount of people in ele
        # self.exg_ele_list = []  # corresponding to the des list
        self.all_ele_status = all_ele_status
        self.kwargs = kwargs
        self.height = self.geometry().height()
        self.move_worker = EleWorker(self, speed=0.08, move_step=1,
                                     all_ele_status=self.all_ele_status)  # the moveing part that runs in the backthread
        self._init_appearance()

    def _init_appearance(self):
        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setText(self.ele_name)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.set_style()

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

    def set_style(self):
        qss = 'background-color:rgb(60, 60, 60); color:rgb(255, 255, 255)'
        self.setStyleSheet(qss)

    def get_current_amount(self):
        '''
        in reality this should be accessed by the sensor
        '''
        return self.current_amount

    def change_amount(self, amount=1):
        '''
        in reality this should be accessed by the sensor
        consider one person at a time by default
        '''
        self.current_amount += amount

    def update_des_exg_list(self):
        # make sure there is no duplicate des, the exg des would replace the normal one
        des_list = [a[0] for a in self.des_exg_list]
        seen = set()
        seen_add = seen.add
        dup_idx = [idx for idx, item in enumerate(des_list) if item in seen or seen_add(item)]
        for idx in dup_idx:
            if self.des_exg_list[idx][1] == 'N':
                self.des_exg_list.pop(idx)

    def _calculateFloor(self, fr_num, f_height, loc_y):
        # ############### this method should changed cause it is too dependent
        # the simple way, just one line
        # return sum(map(lambda j: (fr_num - j) if (50 + f_height / fr_num * j)
        # <= loc_y < (50 + f_height / fr_num * (j + 1)) else 0, range(fr_num)))

        for i in range(1, fr_num + 1):
            # if y is between (30 + (60-(i+1)*10), 30 + (60-i)*10], then it is
            # in ith floor
            L = 30 + f_height / (fr_num - 1) * (fr_num - (i + 1))
            R = 30 + f_height / (fr_num - 1) * (fr_num - i)
            if L < loc_y <= R:
                return i

    def ele_floor2y(self, floor):
        '''
        30 + 10 * (60 - i)
        '''
        # 30 + (60 -i) * (( 600 - 10) / (60 - 1))
        return 30 + (60 - floor) * ((600 - self.geometry().height()) / (60 - 1))


class EleWorker(QtCore.QObject):
    ele_info_sig = pyqtSignal(ElevatorCar, int, int)

    def __init__(self, ele, speed=0.08, move_step=1, all_ele_status={}):
        super(EleWorker, self).__init__()
        self.subject = ele
        self.speed = speed
        self.move_step = move_step
        self.all_ele_status = all_ele_status

    def ele_run(self):
        '''
        all_ele_status is a dict that contains the current floor of all eles, and would update as the ele moves,
        here it is passed to judge whether a ele should be stay for a longer time time exg ele comes
        :param all_ele_status:
        :return:
        '''
        while True:
            if len(self.subject.des_exg_list) == 0:
                self.subject.direction = 'stop'
                time.sleep(5)
                # print('the status of ele are {}'.format(self.all_ele_status))
            else:
                des_exg = self.subject.des_exg_list.pop()
                des = des_exg[0]
                exg_ele = des_exg[1]
                des_y = self.subject.ele_floor2y(des)
                # print('the des popped is {}'.format(des))
                # print('the exg_ele popped is {}'.format(exg_ele))
                current_loc = self.subject.geometry().y()
                x = self.subject.geometry().x()
                # print('current loc of {} is {}, that is {} floor, nearest des is {}'.format(self.subject.ele_name, current_loc, self.subject.getLocation(),des))
                if current_loc > des_y:
                    self.subject.direction = 'up'
                    step = -self.move_step
                elif current_loc < des_y:
                    step = self.move_step
                    self.subject.direction = 'down'
                # print('current step of {} is {}'.format(self.subject.ele_name, step))
                while current_loc != des_y:
                    current_loc += step
                    self.ele_info_sig.emit(self.subject, x, current_loc)
                    time.sleep(self.speed)
                    # print(current_loc)
                    self.subject.obj_signal.emit(self.subject)  # this signal connect the led and the all_ele_status
                # print('one des done, stay 1 seconds')
                if exg_ele != 'N':
                    # if there should change the ele, then wait until the exg ele has came
                    while self.all_ele_status[exg_ele] != des:
                        time.sleep(2)
                else:
                    time.sleep(1)
                self.subject.change_amount(-1)  # update the amount of people in the ele
                # time.sleep(1)

            if int(time.time()) % 100 == 0:
                print('movement of {} is done, no des in the list'.format(self.subject.ele_name))

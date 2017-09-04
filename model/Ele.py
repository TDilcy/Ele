import time
from collections import defaultdict

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
    # phase1_signal = pyqtSignal()  # the signal after one move is done
    # phase2_signal = pyqtSignal()  # the signal after one move is done
    amount_sig = pyqtSignal()
    execute_id_sig = pyqtSignal(str, str)

    # full_sig = pyqtSignal()
    # step1_1_signal = pyqtSignal()  # the signal after one step1_1 is done
    # step1_2_signal = pyqtSignal()  # the signal after one step1_2 is done,
    # the step1_2 is specificly to the ele in the latter place of a route that
    # needs ele exchange

    def __init__(self, order, location, parent=None, direction='stop', ele_name=None, des_exg_dict={}, max_amount=13,
                 all_ele_status={},
                 **kwargs):
        super(ElevatorCar, self).__init__(parent)
        self.order = order
        self.ele_name = ele_name
        self.direction = direction
        self.max_amount = max_amount  # the maxium people a ele can hold
        self.des_exg_dict = des_exg_dict  # a list storing the destinations of passengers
        self.des_exg_dict[
            'up'] = []  # the info inside is a tuple containing (des, exg_ele(if not then 'N'), is_terminal(to control the number of people in the ele), amount(how many people get in), route_finished(whether the end of a route), route_id(identify the route))
        self.des_exg_dict['down'] = []
        self.location = location  # the location would be sorted as 4
        self.current_amount = 0  # the amount of people in ele
        # self.exg_ele_list = []  # corresponding to the des list
        self.all_ele_status = all_ele_status
        self.is_first = 'None'
        self.running_set = ''
        self.des1_des2_diff = -1  # this variable indicates wheather the route should stay priority, if it is less than 0, then it is normal, otherwise it represents until which floor this can be broken
        self.kwargs = kwargs
        self.height = self.geometry().height()
        self.move_worker = EleWorker(self, speed=0.08, move_step=1,
                                     all_ele_status=self.all_ele_status)  # the moveing part that runs in the backthread
        self._init_appearance()

    def _init_appearance(self):
        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setText(self.ele_name + '  ' + str(self.current_amount))
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
        if self.current_amount + amount - 13 > 0:
            actual_in = self.max_amount - self.current_amount
            self.current_amount = 13
        else:
            self.current_amount += amount
            actual_in = -1
        self.amount_sig.emit()
        return actual_in  # the return value is ensure the src_des pair got the right amount of people(in and out)

    def show_amount(self):
        self.setText('{}  {}'.format(self.ele_name, self.current_amount))

    def full_alert(self):
        if self.max_amount * 0.8 <= self.current_amount < self.max_amount:
            self.setStyleSheet('background: #FFFF99')
        elif self.current_amount >= self.max_amount:
            self.setStyleSheet('background: #FF6666')
        elif 1 <= self.current_amount < self.max_amount * 0.8:
            self.setStyleSheet('background: #6699CC')
        else:
            self.set_style()

    def adjust_amount_des(self, route_id, adj_amount):
        # if only adj_mount people get in the ele due to no spare space, then change the amount of its another corresponding des to the actual number, if no one came in, then the latter corresponding des is dropped
        for dirc in ['up', 'down']:
            for des in self.des_exg_dict[dirc]:
                if des[4] == route_id:
                    des[3] = adj_amount
                    if adj_amount == 0:
                        self.des_exg_dict[dirc].remove(des)
                    break

    # def cancel_des(self):
    #     nearest_Y = [des[0] for des in self.des_exg_dict[self.direction] if des[2] == 'Y']
    #     nearest_des = self.des_exg_dict[self.direction][-1]
    #     if self.direction == 'up':
    #         if nearest_Y[-1] > nearest_des[0]:
    #             self.des_exg_dict[self.direction].pop()
    #     elif self.direction == 'down':
    #         if nearest_Y[-1] < nearest_des[0]:
    #             self.des_exg_dict[self.direction].pop()

    def sort_drop_des(self, des_exg_list, direction):
        if direction == 'down':
            des_exg_list = sorted(des_exg_list, key=lambda x: x[0])
        else:
            des_exg_list = sorted(des_exg_list, key=lambda x: x[0], reverse=True)
        # rule 1: if two routes own the same des, then the one that need to exchange would override another one
        des_list = [a[0] for a in des_exg_list]
        des_dup_idx = self.list_duplicates(des_list)

        for idxes in des_dup_idx.values():
            for idx in idxes[:-1]:
                if des_exg_list[idx][1] == 'N':
                    des_exg_list.pop(idx)
                    idxes.remove(idx)
            if len(idxes) != 1:
                # if not 1, then the correct one must have been left, so drop the last one
                des_exg_list.pop(idxes[-1])
        # # rule 2: if two route own the same route_id, then the one who need to exchange ele would override the another
        # route_id_list = [a[4] for a in des_exg_list]
        # route_dup_idx = self.list_duplicates(route_id_list)
        # for idxes in route_dup_idx.values():
        #     # exg_fin_pair = [(des_exg_list[idx][1], des_exg_list[idx][-1]) for idx in idxes]
        #     # if ('N', 'E') in exg_fin_pair:
        #     #     des_exg_list.pop(exg_fin_pair.index(('N', 'E')))
        #     for idx in idxes:
        #         if (des_exg_list[idx][1] == 'N') & (des_exg_list[idx][-1] == 'E'):
        #             des_exg_list.pop(idx)
        #             idxes.remove(idx)
        #     # if len(idxes) != 1:
        #     #     # if not 1, then the correct one must have been left, so drop the last one
        #     #     des_exg_list.pop(idxes[-1])
        return des_exg_list

    @staticmethod
    def list_duplicates(seq):
        '''
        obtain the indices of each duplicate element as a dict
        :param seq:
        :return:
        '''
        tally = defaultdict(list)
        for i, item in enumerate(seq):
            tally[item].append(i)
        return {key: locs for key, locs in tally.items() if len(locs) > 1}



    def update_des_exg_dict(self):
        # make sure there is no duplicate des, the exg des would replace the normal one(if both exsit), and sort the up and down set
        for direction in ['up', 'down']:
            self.des_exg_dict[direction] = self.sort_drop_des(self.des_exg_dict[direction], direction)

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
            if (len(self.subject.des_exg_dict['up']) == 0) & (len(self.subject.des_exg_dict['down']) == 0):
                # print('the running set of {} is {}'.format(self.subject.ele_name, self.subject.running_set))
                self.subject.direction = 'stop'
                self.subject.is_first = 'None'  # if both set are empty, reset the flag
                time.sleep(5)
                # print('the status of ele are {}'.format(self.all_ele_status))
            else:
                if self.subject.is_first != 'None':
                    self.subject.running_set = self.subject.is_first
                    self.subject.is_first = 'None'
                # print('the running set of {} is {}'.format(self.subject.ele_name, self.subject.running_set))
                des_exg = self.subject.des_exg_dict[self.subject.running_set][-1]
                des = des_exg[0]
                exg_ele = des_exg[1]
                is_terminal = des_exg[2]
                amount = des_exg[3]
                route_id = des_exg[4]
                route_finished = des_exg[5]
                # print('the route_finished of {} is {}, and the des is {}'.format(self.subject.ele_name, route_finished, des))
                des_y = self.subject.ele_floor2y(des)
                # print('the des popped is {}'.format(des))
                # print('the exg_ele popped is {}'.format(exg_ele))
                current_loc = self.subject.geometry().y()
                x = self.subject.geometry().x()
                if route_finished == 'S':
                    # if des_exg[5] == 'S':
                    # print('the des of ele {} is {}, and the route_finished sig {} is sent'.format(self.subject.ele_name, des, des_exg[5]))
                    self.subject.execute_id_sig.emit(route_id, 'started')
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
                # self.subject.direction = 'stop'

                if exg_ele != 'N':
                    # if there should change the ele, then wait until the exg ele has came
                    while self.all_ele_status[exg_ele] != des:
                        time.sleep(1.5)
                    time.sleep(1.5)  # # the wait here is important, making sure that one of the two while loop will end

                else:
                    time.sleep(1)

                # print('the des_exg_list of {} before popped is {}'.format(self.subject.ele_name, self.subject.des_exg_list))
                if is_terminal == 'Y':
                    # print('the amount of people in {} before is {}'.format(self.subject.ele_name, self.subject.current_amount))
                    actual_in = self.subject.change_amount(-amount)  # update the amount of people in the ele
                    # print('the amount of people in {} after is {}'.format(self.subject.ele_name, self.subject.current_amount))
                elif is_terminal == 'N':
                    # if not terminal, then some people get in
                    actual_in = self.subject.change_amount(amount)
                    if actual_in != -1:
                        # change the amount in the des_list with same route_id to the right number, drop the des if actual_in is 0.
                        print('the actual_in is {}'.format(actual_in))
                        self.subject.adjust_amount(route_id, actual_in)
                if route_finished == 'E':
                    # if des_exg[5] == 'E':
                    # print('the des of ele {} is {}, and the route_finished sig {} is sent'.format(self.subject.ele_name, des, des_exg[5]))
                    self.subject.execute_id_sig.emit(route_id, 'finished')

                self.subject.des_exg_dict[
                    self.subject.running_set].pop()  # delete the complete des until done, in case that Dcd won't be wrongly calculated
                # print('the des_exg_list of {} after popped is {}'.format(self.subject.ele_name, self.subject.des_exg_list))
                if len(self.subject.des_exg_dict[
                           self.subject.running_set]) == 0:  # when a direction set is completely done, switch to another one
                    # print('before switch the running_set of {} is {}'.format(self.subject.ele_name, self.subject.running_set))
                    self.subject.running_set = 'down' if self.subject.running_set == 'up' else 'up'
                    # print('the des_exg_dict of {} is {},\nafter switch the running_set is {}'.format(self.subject.ele_name, self.subject.des_exg_dict, self.subject.running_set))
                    # time.sleep(1)
                    # print('the amount of people in {} after moving is {}'.format(self.subject.ele_name, self.subject.current_amount))
                    # reset the des1_des2_diff if the des is arrived
                if des == self.subject.des1_des2_diff:
                    self.subject.des1_des2_diff = -1
                    # if int(time.time()) % 100 == 0:
                    #     print('movement of {} is done, no des in the list'.format(self.subject.ele_name))

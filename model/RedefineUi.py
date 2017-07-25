# -*- utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4.QtCore import QRect
from PyQt4.QtCore import pyqtSignal, pyqtSlot

from model.Ele import ElevatorCar
from model.ele_version7_7 import Ui_MainWindow

# import copy

class RedefineUi(QtGui.QMainWindow):
    Y_LOCS = {'A': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0, 'D1': 0, 'D2': 0}
    step1_signal = pyqtSignal() # the signal after one step is done
    end_waiting_signal = pyqtSignal()  # the signal indicating that two eles are all ready
    complete_signal = pyqtSignal()
    src_slider_signal = pyqtSignal()
    des_slider_signal = pyqtSignal()
    # phase1_signal = pyqtSignal() # the signal after one move is done
    def __init__(self):
        super(RedefineUi, self).__init__()
        self.ui = Ui_MainWindow()
        # use the QtGui.QMainWindow to initiate the UI
        self.ui.setupUi(self)
        # self.ui.horizontalLayout.setGeometry(QRect(-9, -9, 1200, 800))
        self.ele_height = 10
        self.margin = 30
        # self._initFrame1(90, self.margin, 100, 600 + self.ele_height)
        self._initFrame1(50, self.margin, 100, 590 + self.ele_height)
        self.WIDTH = self.ui.frame_1.geometry().width()
        self.HEIGHT = self.ui.frame_1.geometry().height()
        self.Y = self.ui.frame_1.geometry().y()
        self.X = self.ui.frame_1.geometry().x()

        self.fr_num = 60  # the total floor of the building
        self.lcds = [self.ui.lcd1, self.ui.lcd2, self.ui.lcd3, self.ui.lcd4, self.ui.lcd5, self.ui.lcd6, self.ui.lcd7]
        # the value in self.movin_range represents the upper and lower bound of elecar
        self.moving_range = {'B2': (self.floor2y(60), self.floor2y(16)),
                             'C2': (self.floor2y(60), self.floor2y(31)),
                             'D2': (self.floor2y(60), self.floor2y(46)),
                             'A': (self.floor2y(60), self.floor2y(1)),
                             'B1': (self.floor2y(15), self.floor2y(1)),
                             'C1': (self.floor2y(30), self.floor2y(1)),
                             'D1': (self.floor2y(45), self.floor2y(1))}

        self.setGeometry(0, 30, 1360, 750)
        self._initFrames()
        self._init_splitters()
        self.elecars, self.init_y_list = self._initEleCars()

        self._initLcds(self.init_y_list)
        self._initBounds()
        self.ui.src_slider.valueChanged.connect(self._read_floor_from_slider)
        self.ui.des_slider.valueChanged.connect(self._read_floor_from_slider)
        self.ui.src_floor_box.textChanged.connect(self._adjust_slider)
        self.ui.des_floor_box.textChanged.connect(self._adjust_slider)
        self._load_qss()
        # self.threadpool = QThreadPool()

    def _initFrame1(self, fX, fY, fWidth, fHeight):
        '''
        set the initial frame which is a standard one for others' position
        '''
        self.ui.frame_1.setGeometry(fX, fY, fWidth, fHeight)

    def _initFrames(self):
        self.ui.frame_2.setGeometry(self.frame_X(self.X, self.WIDTH, 2), self.Y,
                                    self.WIDTH, self.HEIGHT)
        self.ui.frame_3.setGeometry(self.frame_X(self.X, self.WIDTH, 3), self.Y,
                                    self.WIDTH, self.HEIGHT)
        self.ui.frame_4.setGeometry(self.frame_X(self.X, self.WIDTH, 4), self.Y,
                                    self.WIDTH, self.HEIGHT)
        # self.ui.frame_5.setGeometry(self.frame_X(5), self.Y, self.WIDTH, self.HEIGHT)
        # self.ui.frame_6.setGeometry(self.frame_X(6), self.Y, self.WIDTH, self.HEIGHT)
        # self.ui.frame_7.setGeometry(self.frame_X(7), self.Y, self.WIDTH, self.HEIGHT)

    def _init_splitters(self):
        S_WIDTH = self.WIDTH * 0.8
        S_HEIGHT = S_WIDTH
        S_Y = self.Y + self.HEIGHT

        # the lcds location,lcd1, splitter 12,13,14
        self.ui.splitter_2.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 1) + 20, S_Y + 20, S_WIDTH * 0.4, 20))
        self.ui.splitter_3.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 2), S_Y + 10, S_WIDTH, 60))
        self.ui.splitter_4.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 3), S_Y + 10, S_WIDTH, 60))
        self.ui.splitter_5.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 4), S_Y + 10, S_WIDTH, 60))

    @staticmethod
    def splitter_X(X, width, n):
        # this should be a staticmethod????
        return int(X + (2 * n - 1) * width * 0.1 + (n - 1) * width * 0.8)

    @staticmethod
    def frame_X(X, width, n):
        return X + (n - 1) * width

    def _initEleCars(self):
        '''
        initiate the ele_box in the gui, return a list contains all of them
        '''
        HEIGHT = self.ele_height
        WIDTH = self.ui.frame_1.width()
        elecar1 = ElevatorCar(1, 'L1', self, ele_name='A')
        elecar1.setGeometry(self.ui.frame_1.geometry().x(),
                            self.moving_range['A'][1],
                            WIDTH, HEIGHT)
        elecar2 = ElevatorCar(2, 'L2', self, ele_name='B1')
        elecar2.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['B1'][1],
                            WIDTH, HEIGHT)

        elecar3 = ElevatorCar(3, 'L3', self, ele_name='C1')
        elecar3.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['C1'][1],
                            WIDTH, HEIGHT)

# #############temp###############################################
        # elecar3 = Ele, selfvatorCar(3, 'L3')
        # elecar3.setGeometry(10,
        #                     10,
        #                     WIDTH, HEIGHT)
# #############temp###############################################
        elecar4 = ElevatorCar(4, 'L4', self, ele_name='D1')
        elecar4.setGeometry(self.ui.frame_4.geometry().x(),
                            self.moving_range['D1'][1],
                            WIDTH, HEIGHT)

        # frame5,6,7 are no longer exist, and frame 2,3,4 are holding two
        # elecars each
        elecar5 = ElevatorCar(5, 'U1', self, ele_name='B2')
        elecar5.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['B2'][1],
                            WIDTH, HEIGHT)
        elecar6 = ElevatorCar(6, 'U2', self, ele_name='C2')
        elecar6.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['C2'][1],
                            WIDTH, HEIGHT)
        elecar7 = ElevatorCar(7, 'U3', self, ele_name='D2')
        elecar7.setGeometry(self.ui.frame_4.geometry().x(),
                            self.moving_range['D2'][1],
                            WIDTH, HEIGHT)
        elecars = [elecar1, elecar2, elecar3, elecar4, elecar5, elecar6, elecar7]
        # this y_list is for move function
        init_y_list = [ele.geometry().y() for ele in elecars]
        return elecars, init_y_list

    def _initLcds(self, y_list):
        '''
        show the init_floor the elecar locates
        y_list stores the y_position of the elecars
        '''
        for ind, lcd in enumerate(self.lcds):
            lcd.display(self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y_list[ind]))

    def _initBounds(self):
        # the y_loc of B_bound is a relative distance not the absolute one
        self.ui.B_bound.setGeometry(0, self.floor2y(15) - self.margin,
                                    self.WIDTH, 1)
        self.ui.C_bound.setGeometry(0, self.floor2y(30) - self.margin,
                                    self.WIDTH, 1)
        self.ui.D_bound.setGeometry(0, self.floor2y(45) - self.margin,
                                    self.WIDTH, 1)

    def _read_floor_from_slider(self, floor):
        sender = self.sender()
        if sender.objectName() == 'src_slider':
            self.ui.src_floor_box.setHtml('<center><font color="#FFFFFF">{}</font></center>'.format(floor))
        elif sender.objectName() == 'des_slider':
            self.ui.des_floor_box.setHtml('<center><font color="#FFFFFF">{}</font></center>'.format(floor))

    def _adjust_slider(self):
        '''
        input a number would also trigger the _read_floor_from_slider function, so the cursor would be in a
        place, 34 would be 43 for instance, so we should alter the position of the cursor after one number is
        input
        :return:
        '''
        sender = self.sender()
        if sender.objectName() == 'src_floor_box':
            if self._check_input('a') == 1:
                self.ui.src_slider.setValue(int(self.ui.src_floor_box.toPlainText()))
                self.ui.src_floor_box.moveCursor(QtGui.QTextCursor.Right)
            elif self._check_input('a') == 2:
                self.ui.src_floor_box.clear()
            elif self._check_input('a') == 0:
                pass

        elif sender.objectName() == 'des_floor_box':
            if self._check_input('b') == 1:
                self.ui.des_slider.setValue(int(self.ui.des_floor_box.toPlainText()))
                self.ui.des_floor_box.moveCursor(QtGui.QTextCursor.Right)
            elif self._check_input('b') == 2:
                self.ui.des_floor_box.clear()
            elif self._check_input('b') == 0:
                pass

    def _load_qss(self):
        '''
        the path './style_7_8.qss' won't work, should use the following path,
        yet when packaging, the path above can't work, so use the absolute path
        '''
        cur_path = os.getcwd()
        # with open('model/style_7_8.qss', 'r') as f:
        #     qss = f.read()
        with open(cur_path + '\\model\\used_style.qss', 'r') as f:
            # with open('./used_style.qss', 'r') as f:
            qss = f.read()
        self.setStyleSheet(qss)

    def _check_input(self, floor_box):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        try:
            if floor_box == 'a':
                content = self.ui.src_floor_box.toPlainText()
                if len(content) == 0:
                    return 0

            elif floor_box == 'b':
                content = self.ui.des_floor_box.toPlainText()
                if len(content) == 0:
                    return 0
            if 0 < int(content) < 61:
                return 1
            else:
                msg.setText("输入超出范围[1，60]")
                msg.setWindowTitle("范围错误")
                # msg.buttonClicked.connect(msgbtn)
                msg.exec_()
                return 2

        except ValueError:
            msg.setText("非法字符输入，只接受整数输入")
            msg.setWindowTitle("非法输入")
            # msg.buttonClicked.connect(msgbtn)
            msg.exec_()
            return 2

    def clear_input(self):
        self.ui.src_floor_box.clear()
        self.ui.des_floor_box.clear()

    def reset_status(self):
        print('resetting in ui...')
        HEIGHT = self.ele_height
        WIDTH = self.ui.frame_1.width()
        self.elecars[0].setGeometry(self.ui.frame_1.geometry().x(),
                                    self.moving_range['A'][1],
                                    WIDTH, HEIGHT)
        self.elecars[1].setGeometry(self.ui.frame_2.geometry().x(),
                                    self.moving_range['B1'][1],
                                    WIDTH, HEIGHT)
        self.elecars[2].setGeometry(self.ui.frame_3.geometry().x(),
                                    self.moving_range['C1'][1],
                                    WIDTH, HEIGHT)
        self.elecars[3].setGeometry(self.ui.frame_4.geometry().x(),
                                    self.moving_range['D1'][1],
                                    WIDTH, HEIGHT)
        self.elecars[4].setGeometry(self.ui.frame_2.geometry().x(),
                                    self.moving_range['B2'][1],
                                    WIDTH, HEIGHT)
        self.elecars[5].setGeometry(self.ui.frame_3.geometry().x(),
                                    self.moving_range['C2'][1],
                                    WIDTH, HEIGHT)
        self.elecars[6].setGeometry(self.ui.frame_4.geometry().x(),
                                    self.moving_range['D2'][1],
                                    WIDTH, HEIGHT)

    @pyqtSlot()
    # def ele_move(self, name, des):
    def ele_move(self, ele, des):
        # ele = [i for i in self.elecars if i.ele_name == name][0]
        ori_floor = self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, ele.geometry().y())
        des_y = self.floor2y(des)
        # print('current floor in ele_move func is {}'.format(ori_floor))
        # print('des floor in ele_move is {}, and the y is {}'.format(des, self.floor2y(des)))
        print('ori_floor of {} is {}, the ele_des is {}，and the des in this move is {}'.format(ele.ele_name, ori_floor,
                                                                                               self._calculateFloor(
                                                                                                   self.fr_num,
                                                                                                   self.HEIGHT - self.ele_height,
                                                                                                   ele.des), des))
        if ori_floor < des:
            ele.moveUp()
            # self.threadpool.releaseThread()
            # ele.thread.setAutoDelete(False)
            # self.threadpool.start(ele.thread)

            ele.obj_signal.connect(lambda: self.move(ele, top_margin=des_y))
            # ele.thread.started.connect(lambda: self.move(ele, top_floor=des))
            # ele.thread.is_running_signal.connect(self.wait_a_while)

        elif ori_floor > des:
            ele.moveDown()
            # self.threadpool.releaseThread()
            # ele.thread.setAutoDelete(False)
            # self.threadpool.start(ele.thread)
            # self.threadpool.reserveThread()
            # ele.thread.started.connect(lambda: self.move(ele, buttom_floor=des))
            ele.obj_signal.connect(lambda: self.move(ele, buttom_margin=des_y))
            # ele.thread.is_running_signal.connect(self.wait_a_while)
        elif ori_floor == des:
            ele.moveStop()
            # ele.obj_signal.connect(lambda: self.move(ele))
            # ele.ele_thread.start()
            # ele.thread.setAutoDelete(False)
            # self.threadpool.start(ele.thread)
            # ele.thread.exit()
        # ele.thread.setAutoDelete(True)

            # ele.phase1_signal.disconnect(lambda: )






##############################################################################





######################### y_loc version##############################
    # def move(self, ele):
    #     '''
    #     important issue: the refresh operation should be put at the main thread rather than the sub-thread, otherwise, it will crash.
    #     '''
    #     # # the x, y position of the elebox
    #     x = ele.geometry().x()
    #     y = ele.geometry().y()
    #     # set the moving range for the upper elecars and the lowwer elecars
    #     # if top_margin is None:
    #     top_margin = self.moving_range[ele.ele_name][0]
    #     # if buttom_margin is None:
    #     buttom_margin = self.moving_range[ele.ele_name][1]
    #     if ele.direction == "up":
    #         step = -2
    #     elif ele.direction == "down":
    #         step = 2
    #     else:
    #         return
    #     y += step
    #     QtGui.QApplication.processEvents()
    #     # while (y <= buttom_margin) & (y >= top_margin):
    #     if (y <= buttom_margin) & (y >= top_margin):
    #         ele.new_move(x, y)
            # break

#################### floor version####################################
        # this version would cause some problems concerning to the floor display
    # def move(self, ele, top_floor = None, buttom_floor = None):
    def move(self, ele, top_margin = None, buttom_margin = None):
        '''
        important issue: the refresh operation should be put at the main thread rather than the sub-thread, otherwise, it will crash.
        '''
        # # the x, y position of the elebox
        x = ele.geometry().x()
        y = ele.geometry().y()
        # set the moving range for the upper elecars and the lowwer elecars
        if top_margin is None:
            # print('True')
            # top_floor = self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, self.moving_range[ele.ele_name][0])
            top_margin = self.moving_range[ele.ele_name][0]
        if buttom_margin is None:
            # print('False')
            # buttom_floor = self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, self.moving_range[ele.ele_name][1])
            buttom_margin = self.moving_range[ele.ele_name][1]

        if ele.direction == "up":
            step = -1
        elif ele.direction == "down":
            step = 1
        else:
            return
        y += step
        QtGui.QApplication.processEvents()
        if (y <= buttom_margin) & (y >= top_margin):
            # print('the location of y before movement is {}'.format(ele.geometry().y()))
            ele.new_move(x, y)
            # print('the y of ele after movement is {}, in {} floor'.format(ele.geometry().y(), ele.getLocation()))
    #         # break



    def showFloor(self, ele):
        '''
        show which flow does the elecar locate in the correspondant lcd
        '''
        y = ele.geometry().y()  # + ele.height  # add ele.height to avoid lcd displaying 0 when arrive at the top floor'
        # top_margin = 50
        lcd_selected = self.lcds[self.elecars.index(ele)]
        # calculate the floor
        lcd_selected.display(self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y))

    def floor2y(self, floor):
        '''
        30 + 10 * (60 - i)
        '''
        return self.margin + (self.fr_num - floor) * ((self.HEIGHT - self.ele_height) / (self.fr_num - 1))

    ################# executing one route at one function so as to get it done steply rather than simultaneously ######################
    def executeRoute(self, route):
        '''
        a whole movement to a given destination floor, first move to the floor where the passenger is, and then the destination floor
        :param des, ele
        :return: the elecar aminaiton
        '''
        if len(route) == 3:
            src = route[0]
            ele_name = route[1]
            des = route[2]

            ele = [i for i in self.elecars if i.ele_name == ele_name][0]
            print('the name of ele selected is {} and the its current floor is {}, its des is {}'.format(ele.ele_name, ele.getLocation(), ele.des))
            ele.des = self.floor2y(src)
            ele_des_list = [src, des]
            print("the des of {} is set as {}".format(ele.ele_name, ele.des))
            ele.reset_thread()
            # print('the id after the thread_reset is {}'.format(id(ele.ele_thread)))
            # ele.thread.setAutoDelete(False)
            self.ele_move(ele, src)
            # ele.thread.started.connect(self.show_thread_start)
            ##################################
            print('the des of this route is {}, and its corresponding y is {}'.format(des, self.floor2y(des)))
            # ele.thread.begin_signal.connect(lambda: self.show_thread_start(ele))
            ele.ele_thread.started.connect(lambda: self.show_thread_start(ele))

            ele.ele_thread.finished.connect(lambda: self.show_thread_finished(ele))

            ele.ele_thread.finished.connect(lambda: self.set_des(ele, ele_des_list))

            ele.phase1_signal.connect(lambda: self.ele_move(ele, des))
            ele.phase2_signal.connect(self.emit_over)
            self.complete_signal.connect(lambda: self.discon(ele1=ele))

        elif len(route) == 6:
            src = route[0]
            ele1_name = route[1]
            temp = route[2]
            ele2_name = route[3]
            des = route[4]

            ## step1_1: ele1 move to the temp floor
            ele1 = [i for i in self.elecars if i.ele_name == ele1_name][0]
            ele1.des = self.floor2y(src)
            ele1_des_list = [src, temp]
            # reset the thread and the ready_status
            ele1.reset_thread()
            ele1.ready = False
            self.ele_move(ele1, src)
            ele1.ele_thread.started.connect(lambda: self.show_thread_start(ele1))
            ele1.ele_thread.finished.connect(lambda: self.show_thread_finished(ele1))
            # ele1.ele_thread.finished.connect(lambda: self.set_2nd_des(ele1, temp))
            ele1.ele_thread.finished.connect(lambda: self.set_des(ele1, ele1_des_list))

            ele1.phase1_signal.connect(lambda: self.ele_move(ele1, temp))

            ele1.phase2_signal.connect(ele1.set_ready)
            ele1.phase2_signal.connect(lambda: self.step2(ele1, ele2))


            ## step1_2: ele2 move to the temp floor
            ele2 = [i for i in self.elecars if i.ele_name == ele2_name][0]
            ele2.des = self.floor2y(temp)
            ele2_des_list = [temp, des]
            # reset the thread and the ready_status
            ele2.reset_thread()
            ele2.ready = False
            self.ele_move(ele2, temp)
            ele2.ele_thread.started.connect(lambda: self.show_thread_start(ele2))
            ele2.ele_thread.finished.connect(lambda: self.show_thread_finished(ele2))
            # ele2.ele_thread.finished.connect(lambda: self.set_2nd_des(ele2, des))
            ele2.ele_thread.finished.connect(lambda: self.set_des(ele2, ele2_des_list))
            ele2.phase1_signal.connect(ele2.set_ready)
            ele2.phase1_signal.connect(lambda: self.step2(ele1, ele2))



            ## step2: ele2 move to the des floor after both ele1 and itself arriving at the temp floor
            self.end_waiting_signal.connect(lambda: self.ele_move(ele2, des))
            ## and the step1_1 signal of ele is no longer useful, so connect it to the null operation
            # ele2.phase2_signal.connect(lambda: self.cut(ele2, des))
            # ele2.phase2_signal.connect(lambda: self.cut_)
            ele2.phase2_signal.connect(self.emit_over)
            self.complete_signal.connect(lambda: self.discon(ele1, ele2))

    def null_operation(self):
        print('this is an operation doing nothing')
        pass


    def emit_over(self):
        print('emit_over sig is sent')
        self.complete_signal.emit()

    def discon(self, ele1, ele2=None):
        '''
        !!! important, cut all the connections of ele, including phase1_sig, phase2_sig, and the waiting_sig to ensure
        the latter operation won't be impacted by the previous one
        :param ele1:
        :param ele2:
        '''
        try:
            ele1.phase1_signal.disconnect()
            print('the p1_signal of {} are disconnected'.format(ele1.ele_name))
        except TypeError:
            print("fail to cut the connection of {}'s p1_signal".format(ele1.ele_name))
            pass
        try:
            ele1.phase2_signal.disconnect()
            print('the p2_signal of {} are disconnected'.format(ele1.ele_name))
        except TypeError:
            print("fail to cut the connection of {}'s p2_signal".format(ele1.ele_name))
            pass
        if ele2 is not None:
            try:
                ele2.phase1_signal.disconnect()
                print('the p1_signal of {} are disconnected'.format(ele2.ele_name))
            except TypeError:
                print("fail to cut the connection of {}'s p1_signal".format(ele2.ele_name))
                pass
            try:
                ele2.phase2_signal.disconnect()
                print('the p2_signal of {} are disconnected'.format(ele2.ele_name))
            except TypeError:
                print("fail to cut the connection of {}'s p2_signal".format(ele2.ele_name))
                pass
        try:
            self.end_waiting_signal.disconnect()
            print('the end_waiting_signal is disconnected')
        except TypeError:
            pass
            # try:
            #     ele1.phase2_signal.disconnect(ele1.set_ready)
            # except TypeError:
            #     pass
            # try:
            #     ele2.phase1_signal.disconnect(ele2.set_ready)
            # except TypeError:
            #     pass
            # self.end_waiting_signal.disconnect(lambda: self.discon(ele2, des))

    def step2(self, ele1, ele2):
        if ele1.ready & ele2.ready:
            # ele2.step1_2_signal.emit()
            self.end_waiting_signal.emit()
            print('the waiting signal is emitted')
            try:
                ele1.phase2_signal.disconnect(ele1.set_ready)
                ele1.ready = False
            except TypeError:
                pass
            try:
                ele2.phase1_signal.disconnect(ele2.set_ready)
                ele2.ready = False
            except TypeError:
                pass

    @pyqtSlot()
    def set_des(self, ele, des_list):
        # des_list: [temp, des]
        print('the ele_des of {} is {},and the des_list is {}'.format(ele.ele_name, self._calculateFloor(self.fr_num,
                                                                                                         self.HEIGHT - self.ele_height,
                                                                                                         ele.des),
                                                                      des_list))
        print('the geometry of ele is {}, and the first one in des_list is {}'.format(ele.geometry().y(),
                                                                                      self.floor2y(des_list[0])))
        # if ele.geometry().y() == self.floor2y(des_list[0]):
        # ## the floor version, different with the y_loc version
        if ele.getLocation() == des_list[0]:
            ele.phase1_signal.emit()
            ele.des = self.floor2y(des_list[1])
            print(
                'phase1 signal of {} is emitted...............the ele_des is set as {},'.format(ele.ele_name,
                                                                                                self._calculateFloor(
                                                                                                    self.fr_num,
                                                                                                    self.HEIGHT - self.ele_height,
                                                                                                    ele.des)))
        # elif ele.geometry().y() == self.floor2y(des_list[1]):
        if ele.getLocation() == des_list[1]:
            ele.phase2_signal.emit()
            print('phase2_signal of {} is emitted......'.format(ele.ele_name))
            # else:
            #     # if the des from last round is left, then set it as the new one
            #     ele.des = self.floor2y(des_list[0])



    def set_delete(self, ele):
        ele.thread.setAutoDelete(True)

    def show_thread_finished(self, ele):
        # print('the thread of {} is finished, and the thread_handle is {}'.format(ele.ele_name, ele.thread.currentThreadId()))
        print('the thread of {} is finished'.format(ele.ele_name))

    def show_thread_start(self, ele):
        # print('the thread of {} is started, and the thread_handle is {}'.format(ele.ele_name, ele.thread.currentThreadId()))
        print('the thread of {} is started'.format(ele.ele_name))

    def show_info(self, y, des):
        print(y, des)


    def demoMotion(self):
        # self.up(1, 30)
        self.down(1, 620)
        # self.up(2, )
        # self.up(3)
        # self.up(4)
        # self.up(5)
        # self.up(6)
        # self.up(7)



    # @staticmethod
    def _calculateFloor(self, fr_num, f_height, loc_y):
        # the simple way, just one line, not work now!
        # return sum(map(lambda j: (fr_num - j) if (50 + f_height / fr_num * j) <= loc_y < (50 + f_height / fr_num * (j + 1)) else 0, range(fr_num)))

        # a more concrete way；
        # for i in range(1, fr_num + 1):
        #     if i == 1:
        #         # make sure the 1st floor displayed properly
        #         L = self.margin + f_height / fr_num * (fr_num - i + 1) + 1
        #     U = self.margin + f_height / fr_num * (fr_num - (i + 1) + 1)
        #     if U <= loc_y < L:
        #         return i
        #     # else:
        #     #     return 999
        #####################
        # for i in range(1, fr_num + 1):
        #     L = self.margin + f_height / (fr_num - 1) * (fr_num - (i - 1))
        #     U = self.margin + f_height / (fr_num - 1) * (fr_num - i)
        #     if U <= loc_y < L:
        #         return i
        ############################
        for i in range(1, fr_num + 1):
            # if y is between (30 + (60-(i+1)*10), 30 + (60-i)*10], then it is in ith floor
            L = self.margin + f_height / (fr_num - 1) * (fr_num - (i + 1))
            R = self.margin + f_height / (fr_num - 1) * (fr_num - i)
            if L < loc_y <= R:
                return i
            # else:
            #     return 999

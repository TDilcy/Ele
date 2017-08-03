# -*- utf-8 -*-
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QRect
from PyQt4.QtCore import pyqtSignal

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
        self.all_ele_status = {'A': 1, 'B1': 1, 'C1': 1, 'D1': 1, 'B2': 16, 'C2': 31, 'D2': 46}
        self.elecars, self.init_y_list = self._initEleCars()

        self.threads = [QtCore.QThread() for i in range(len(self.elecars))]

        self._initLcds(self.init_y_list)
        self._initBounds()
        self.ui.src_slider.valueChanged.connect(self._read_floor_from_slider)
        self.ui.des_slider.valueChanged.connect(self._read_floor_from_slider)
        self.ui.src_floor_box.textChanged.connect(self._adjust_slider)
        self.ui.des_floor_box.textChanged.connect(self._adjust_slider)
        self._load_qss()
        #### following code control the movement ##############
        for i in self.elecars:
            i.move_worker.ele_info_sig.connect(self.move_one_step)
        self.start_ele_loop()




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
        elecar1 = ElevatorCar(1, 'L1', self, direction='stop', ele_name='A', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
        elecar1.setGeometry(self.ui.frame_1.geometry().x(),
                            self.moving_range['A'][1],
                            WIDTH, HEIGHT)
        elecar2 = ElevatorCar(2, 'L2', self, direction='stop', ele_name='B1', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
        elecar2.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['B1'][1],
                            WIDTH, HEIGHT)

        elecar3 = ElevatorCar(3, 'L3', self, direction='stop', ele_name='C1', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
        elecar3.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['C1'][1],
                            WIDTH, HEIGHT)
        elecar4 = ElevatorCar(4, 'L4', self, direction='stop', ele_name='D1', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
        elecar4.setGeometry(self.ui.frame_4.geometry().x(),
                            self.moving_range['D1'][1],
                            WIDTH, HEIGHT)
        elecar5 = ElevatorCar(5, 'U1', self, direction='stop', ele_name='B2', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
        elecar5.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['B2'][1],
                            WIDTH, HEIGHT)
        elecar6 = ElevatorCar(6, 'U2', self, direction='stop', ele_name='C2', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
        elecar6.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['C2'][1],
                            WIDTH, HEIGHT)
        elecar7 = ElevatorCar(7, 'U3', self, direction='stop', ele_name='D2', des_exg_list=[], max_mount=13,
                              all_ele_status=self.all_ele_status)
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

    # def show_info(self, y, des):
    #     print(y, des)

    def _calculateFloor(self, fr_num, f_height, loc_y):
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

    # ###### new way of simulating the ele-move ############
    @staticmethod
    def move_one_step(ele, x, y):
        ele.move(x, y)

    def start_ele_loop(self):
        for index, ele in enumerate(self.elecars):
            ele.move_worker.moveToThread(self.threads[index])
            # self.threads[index].started.connect(lambda: print('the {} is started'.format(self.threads[index].currentThreadId())))
            # self.threads[index].started.connect(lambda: ele.move_worker.ele_run(all_ele_status=self.all_ele_statu))
            self.threads[index].started.connect(ele.move_worker.ele_run)
            # pass
            self.threads[index].start()

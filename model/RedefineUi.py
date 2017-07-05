# -*- utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import QRect
from PyQt4.QtCore import pyqtSignal, pyqtSlot

from model.Ele import ElevatorCar
from model.ele_version5_3_2 import Ui_MainWindow


# import time
# import copy

class RedefineUi(QtGui.QMainWindow):
    Y_LOCS = {'A': 0, 'B1': 0, 'B2': 0, 'C1': 0, 'C2': 0, 'D1': 0, 'D2': 0}
    step1_signal = pyqtSignal() # the signal after one step is done
    # phase1_signal = pyqtSignal() # the signal after one move is done
    def __init__(self):
        super(RedefineUi, self).__init__()
        self.ui = Ui_MainWindow()
        # use the QtGui.QMainWindow to initiate the UI
        self.ui.setupUi(self)
        self.ele_height = 10
        self.margin = 30
        # self._initFrame1(90, self.margin, 100, 600 + self.ele_height)
        self._initFrame1(90, self.margin, 100, 590 + self.ele_height)
        self.WIDTH = self.ui.frame_1.geometry().width()
        self.HEIGHT = self.ui.frame_1.geometry().height()
        self.Y = self.ui.frame_1.geometry().y()
        self.X = self.ui.frame_1.geometry().x()

        self.fr_num = 60  # the total floor of the building
        self.lcds = [self.ui.lcd1, self.ui.lcd2, self.ui.lcd3, self.ui.lcd4, self.ui.lcd5, self.ui.lcd6, self.ui.lcd7]
        # the value in self.movin_range represents the upper and lower bound of elecar
        # self.moving_range = {'B2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.75),
        #                      'C2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.5),
        #                      'D2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.25),
        #                      'A': (self.Y, self.Y + (self.HEIGHT - self.ele_height)),
        #                      'B1': (self.Y + (self.HEIGHT - self.ele_height) * 0.75, self.Y + (self.HEIGHT - self.ele_height)),
        #                      'C1': (self.Y + (self.HEIGHT - self.ele_height) * 0.5, self.Y + (self.HEIGHT - self.ele_height)),
        #                      'D1': (self.Y + (self.HEIGHT - self.ele_height) * 0.25, self.Y + (self.HEIGHT - self.ele_height))}

        self.moving_range = {'B2': (self.floor2y(60), self.floor2y(16)),
                             'C2': (self.floor2y(60), self.floor2y(31)),
                             'D2': (self.floor2y(60), self.floor2y(46)),
                             'A': (self.floor2y(60), self.floor2y(1)),
                             'B1': (self.floor2y(15), self.floor2y(1)),
                             'C1': (self.floor2y(30), self.floor2y(1)),
                             'D1': (self.floor2y(45), self.floor2y(1))}

        self.setGeometry(500, 100, 1300, 750)
        self._initFrames()
        self._init_splitters()
        self.elecars, self.init_y_list = self._initEleCars()

        self._initLcds(self.init_y_list)
        self._initBounds()
        # self.threadpool = QThreadPool()

        # self._get_y_locs()
        # self.initScrollArea(self.elecars)

    # def initScrollArea(self, elecars_to_add):
    #     '''
    #     ref: http://stackoverflow.com/questions/32714656/pyqt-add-a-scrollbar-to-mainwindow
    #     '''
    #     self.layout = QtGui.QVBoxLayout(self.ui.centralwidget)  # create the layout
    #     self.ui.scroll_area = QtGui.QScrollArea(self.ui.centralwidget)  # create the scrollarea
    #     self.layout.addWidget(self.ui.scroll_area)  # add scroll area to the layout
    #     self.ui.scroll_area.setWidget(self.ui.frame_outer)  # add content in the scroll area
    #     self.ui.scroll_area.setAutoFillBackground(True)
    #     # self.layout = QtGui.QHBoxLayout(self.ui.widget_outer)
# ### test if we obtain the correct y_locs, that is, the changing y_loc rather than the static location#####
#     def test_y_locs(self):
#         for i in self.Y_LOCS.keys():
#             print(i + ':' + str(self.Y_LOCS[i]))
#
#     def _get_y_locs(self):
#         for i in self.elecars:
#             i.y_loc_signal.connect(self._set_y_locs)
#
#     def _set_y_locs(self, name, y_loc):
#         self.Y_LOCS[name] = y_loc

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

        # the buttons splitters location
        # self.ui.splitter_1.setGeometry(self.splitter_X(self.X, self.WIDTH, 1), S_Y, S_WIDTH, S_HEIGHT)
        # self.ui.splitter_15.setGeometry(self.splitter_X(self.X, self.WIDTH, 2), S_Y, S_WIDTH, S_HEIGHT)
        # self.ui.splitter_8.setGeometry(self.splitter_X(self.X, self.WIDTH, 3), S_Y, S_WIDTH, S_HEIGHT)
        # self.ui.splitter_9.setGeometry(self.splitter_X(self.X, self.WIDTH, 4), S_Y, S_WIDTH, S_HEIGHT)
        # The layout has changed, the splitters needed to be adjusted are spliter_15, spliter_8, and spliter_9, these are for buttons
        # ############ deprecated #############################################
        # self.ui.splitter_2.setGeometry(self.splitter_X(2), S_Y, S_WIDTH, S_HEIGHT)   #
        # self.ui.splitter_3.setGeometry(self.splitter_X(3), S_Y, S_WIDTH, S_HEIGHT)   #
        # self.ui.splitter_4.setGeometry(self.splitter_X(4), S_Y, S_WIDTH, S_HEIGHT)   #
        # self.ui.splitter_5.setGeometry(self.splitter_X(5), S_Y, S_WIDTH, S_HEIGHT)   #
        # self.ui.splitter_6.setGeometry(self.splitter_X(6), S_Y, S_WIDTH, S_HEIGHT)   #
        # self.ui.splitter_7.setGeometry(self.splitter_X(7), S_Y, S_WIDTH, S_HEIGHT)   #
        #######################################################################

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
        self.ui.B_bound.setGeometry(0, self.floor2y(16) - self.margin,
                                    self.WIDTH, 2)
        self.ui.C_bound.setGeometry(0, self.floor2y(31) - self.margin,
                                    self.WIDTH, 2)
        self.ui.D_bound.setGeometry(0, self.floor2y(46) - self.margin,
                                    self.WIDTH, 2)
######################## the following part will be repalced with another way#############
    # def up(self, order, top):
    #     ele = self.elecars[order - 1]
    #     ele.moveUp()
    #     self.threadpool.start(ele.thread)
    #     ele.thread.obj_signal.connect(lambda: self.move(ele, top_margin=top))
    #
    # def down(self, order, buttom):
    #     ele = self.elecars[order - 1]
    #     ele.moveDown()
    #     self.threadpool.start(ele.thread)
    #     ele.thread.obj_signal.connect(lambda: self.move(ele, buttom_margin=buttom))
    #
    # def stop(self, order):
    #     ele = self.elecars[order - 1]
    #     ele.moveStop()
    #     self.threadpool.start(ele.thread)
    #     ele.thread.obj_signal.connect(lambda: self.move(ele))
#############################################################################



# ######################## this part is correspondant to the global variable method#############
#     def up(self, order):
#         ele = self.elecars[order - 1]
#         ele.moveUp()
#         ele.thread.obj_signal.connect(self.move)
#
#     def down(self, order):
#         ele = self.elecars[order - 1]
#         ele.moveDown()
#         ele.thread.obj_signal.connect(self.move)
#
#     def stop(self, order):
#         ele = self.elecars[order - 1]
#         ele.moveStop()
#         ele.thread.obj_signal.connect(self.move)
#############################################################################
    @pyqtSlot()
    # def ele_move(self, name, des):
    def ele_move(self, ele, des):
        # ele = [i for i in self.elecars if i.ele_name == name][0]
        ori_floor = self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, ele.geometry().y())
        des_y = self.floor2y(des)
        # print('current floor in ele_move func is {}'.format(ori_floor))
        # print('des floor in ele_move is {}, and the y is {}'.format(des, self.floor2y(des)))
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
            # ele.ele_thread.start()
            # ele.thread.setAutoDelete(False)
            # self.threadpool.start(ele.thread)
            # ele.thread.exit()
        # ele.thread.setAutoDelete(True)





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
            print("the ele's des is set as {}".format(ele.des))
            # print('the ele_des after set ')
            # print('the first des is {}'.format(self.floor2y(src)))
            # self.ele_move(ele_name, src)
            # ele.ele_thread = ele
            # print('the id before the thread_reset is {}'.format(id(ele.ele_thread)))
            ele.reset_thread()
            # print('the id after the thread_reset is {}'.format(id(ele.ele_thread)))
            # ele.thread.setAutoDelete(False)
            self.ele_move(ele, src)
            # ele.thread.started.connect(self.show_thread_start)
            ##################################
            print('the des of this route is {}, and its cooresponding y is {}'.format(des, self.floor2y(des)))
            # ele.thread.begin_signal.connect(lambda: self.show_thread_start(ele))
            ele.ele_thread.started.connect(lambda: self.show_thread_start(ele))
            # ele.thread.finished.connect(self.show_thread_finished)
            # ele.thread.done_signal.connect(lambda: self.show_thread_finished(ele))
            ele.ele_thread.finished.connect(lambda: self.show_thread_finished(ele))
            # ele.thread.done_signal.connect(lambda: self.set_2nd_des(ele, des))
            ele.ele_thread.finished.connect(lambda: self.set_2nd_des(ele, des))
            # after 2nd des is set, the signal is emitted, and phase2 begins
            # ele.phase1_signal.connect(lambda: self.ele_move(ele_name, des))
            # ele.phase1_signal.connect(lambda: self.set_delete(ele))
            ele.phase1_signal.connect(lambda: self.ele_move(ele, des))

        elif len(route) == 6:
            src = route[0]
            ele1_name = route[1]
            temp = route[2]
            ele2_name = route[3]
            des = route[4]

            ## step1_1: ele1 move to the temp floor
            ele1 = [i for i in self.elecars if i.ele_name == ele1_name][0]
            ele1.des = self.floor2y(src)
            # reset the thread and the ready_status
            ele1.reset_thread()
            ele1.ready = False
            # ele1.reset_signal()
            self.ele_move(ele1, src)
            ele1.ele_thread.started.connect(lambda: self.show_thread_start(ele1))
            ele1.ele_thread.finished.connect(lambda: self.show_thread_finished(ele1))
            ele1.ele_thread.finished.connect(lambda: self.set_2nd_des(ele1, temp))
            ele1.phase1_signal.connect(lambda: self.ele_move(ele1, temp))
            ele1.step1_1_signal.connect(ele1.set_ready)
            ele1.step1_1_signal.connect(lambda: self.step2_signal(ele1, ele2))

            ## step1_2: ele2 move to the temp floor
            ele2 = [i for i in self.elecars if i.ele_name == ele2_name][0]
            ele2.des = self.floor2y(temp)
            # reset the thread and the ready_status
            ele2.reset_thread()
            ele2.ready = False
            # ele1.reset_signal()
            self.ele_move(ele2, temp)
            ele2.ele_thread.started.connect(lambda: self.show_thread_start(ele2))
            ele2.ele_thread.finished.connect(lambda: self.show_thread_finished(ele2))
            ele2.ele_thread.finished.connect(lambda: self.set_2nd_des(ele2, des))
            ele2.phase1_signal.connect(ele2.set_ready)
            ele2.phase1_signal.connect(lambda: self.step2_signal(ele1, ele2))

            ## step2: ele2 move to the des floor after both ele1 and itself arriving at the temp floor
            ele2.step1_2_signal.connect(lambda: self.ele_move(ele2, des))
            ## and the step1_1 signal of ele is no longer useful, so connect it to the null operation
            ele2.step1_1_signal.connect(self.null_operation)


asdfasdfsa
d  # def is_step1_1_over(self, ele, des):
#     print('the ele_des is {}, and the expected one is {}'.format(ele.des, des))
#     # if int(ele.des) == int(des):
#     if ele.des == des:
#         # time.sleep(0.2)
#         ele.step1_1_signal.emit()
#     else:
#         pass
# def exe_step2(self, ele1, ele2, src, des):
#     ele1.thread.finished.connect(lambda: self.ele_move(ele2, src))
#     # self.ele_move(ele2.ele_name, src)
#     ele2.thread.finished.connect(lambda: self.set_2nd_des(ele2, des))
#     ele2.phase1_signal.connect(lambda: self.ele_move(ele2, des))

def step2_signal(self, ele1, ele2):
    if ele1.ready & ele2.ready:
        ele2.step1_2_signal.emit()
        print('step1_2 signal of {} is emitted'.format(ele2.ele_name))


def null_operation(self):
    print('this is an operation doing nothing')
    pass

    # def is_step1_over(self, des_sig, des):
    #     if des_sig == des:
    #         self.step1_signal.emit()
    @pyqtSlot()
    def set_2nd_des(self, ele, des):
        # print('............ele_des is {}, target is {}'.format(ele.des, self.floor2y(des)))
        if ele.des != self.floor2y(des):
            ele.des = self.floor2y(des)
            ele.phase1_signal.emit()
            print('phase1 signal of {} is emitted...............the ele_des is set as {}'.format(ele.ele_name, ele.des))
        else:
            ele.step1_1_signal.emit()
            print('step1_1 signal of {} is emitted......'.format(ele.ele_name))

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

    # def executeRoute(self, route):
    #     '''
    #     execute the route given, simulate the movement of elecars
    #     :param route:a list containing which ele you should take and in which floor you should change ele
    #     :return: execute the whole route
    #     '''
    #     # route = [2, 'D1', 10] # just for debugging
    #     if len(route) == 3:
    #         src = route[0]
    #         picked_ele = route[1]
    #         des = route[2]
    #         ele = picked_ele #[i for i in self.elecars if i.ele_name == picked_ele][0]  # fetch the ele using the given name
    #         self._entireMove(ele, src, des)
    #     elif len(route) == 6:
    #         src = route[0]
    #         picked_ele1 = route[1]
    #         temp = route[2]
    #         picked_ele2 = route[3]
    #         des = route[4]
    #         ele1 = picked_ele1 #[i for i in self.elecars if i.ele_name == picked_ele1][0]  # fetch the ele using the given name
    #         ele2 = picked_ele2 #[i for i in self.elecars if i.ele_name == picked_ele2][0]  # fetch the ele using the given name
    #         self._entireMove(ele1, src, temp)
    #         self._entireMove(ele2, temp, des)
    #     # else:
    #     #     pass


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

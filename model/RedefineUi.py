# -*- utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import QRect
from PyQt4.QtCore import pyqtSignal
# from model.ele import Ui_MainWindow
# from model.ele_version5_3 import Ui_MainWindow
from model.ele_version5_3_2 import Ui_MainWindow
# from model.ele_3_27 import Ui_MainWindow
# from model.ele_bak import Ui_MainWindow
from model.ElevatorCar import ElevatorCar
import time


class RedefineUi(QtGui.QMainWindow):

    def __init__(self):
        super(RedefineUi, self).__init__()
        self.ui = Ui_MainWindow()
        # use the QtGui.QMainWindow to initiate the UI
        self.ui.setupUi(self)
        self.ele_height = 15
        self.margin = 30
        self._initFrame1(90, self.margin, 100, 600 + self.ele_height)
        self.WIDTH = self.ui.frame_1.geometry().width()
        self.HEIGHT = self.ui.frame_1.geometry().height()
        self.Y = self.ui.frame_1.geometry().y()
        self.X = self.ui.frame_1.geometry().x()

        self.fr_num = 60  # the total floor of the building
        self.lcds = [self.ui.lcd1, self.ui.lcd2, self.ui.lcd3, self.ui.lcd4, self.ui.lcd5, self.ui.lcd6, self.ui.lcd7]
        # the value in self.movin_range represents the upper and lower bound of elecar
        self.moving_range = {'B2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.75),
                             'C2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.5),
                             'D2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.25),
                             'A': (self.Y, self.Y + (self.HEIGHT - self.ele_height)),
                             'B1': (self.Y + (self.HEIGHT - self.ele_height) * 0.75, self.Y + (self.HEIGHT - self.ele_height)),
                             'C1': (self.Y + (self.HEIGHT - self.ele_height) * 0.5, self.Y + (self.HEIGHT - self.ele_height)),
                             'D1': (self.Y + (self.HEIGHT - self.ele_height) * 0.25, self.Y + (self.HEIGHT - self.ele_height))}

        self.setGeometry(500, 100, 1300, 750)
        self._initFrames()
        self._init_splitters()
        self.elecars, self.init_y_list = self._initEleCars()

        self._initLcds(self.init_y_list)
        self._initBounds()
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
        self.ui.B_bound.setGeometry(0, (self.HEIGHT - self.ele_height) * 0.75,
                                    self.WIDTH, 2)
        self.ui.C_bound.setGeometry(0, (self.HEIGHT - self.ele_height) * 0.5,
                                    self.WIDTH, 2)
        self.ui.D_bound.setGeometry(0, (self.HEIGHT - self.ele_height) * 0.25,
                                    self.WIDTH, 2)

    def up(self, order):
        self.elecars[order].moveUp()
        self.elecars[order].thread.obj_signal.connect(self.move)

    def down(self, order):
        self.elecars[order].moveDown()
        self.elecars[order].thread.obj_signal.connect(self.move)

    def stop(self, order):
        self.elecars[order].moveStop()
        self.elecars[order].thread.obj_signal.connect(self.move)

    def move(self, ele):
        '''
        important issue: the refresh operation should be put at the main thread rather than the sub-thread, otherwise, it will crash.
        '''
        # # the x, y position of the elebox
        x = ele.geometry().x()
        y = ele.geometry().y()
        # set the moving range for the upper elecars and the lowwer elecars
        top_margin = self.moving_range[ele.ele_name][0]
        buttom_margin = self.moving_range[ele.ele_name][1]
        if ele.direction == "up":
            step = -2
        elif ele.direction == "down":
            step = 2
        else:
            return
        y += step
        QtGui.QApplication.processEvents()
        while (y <= buttom_margin) & (y >= top_margin):
            ele.move(x, y)
            break

    def showFloor(self, ele):
        '''
        show which flow does the elecar locate in the correspondant lcd
        '''
        y = ele.geometry().y()  # + ele.height  # add ele.height to avoid lcd displaying 0 when arrive at the top floor'
        # top_margin = 50
        lcd_selected = self.lcds[self.elecars.index(ele)]
        # calculate the floor
        lcd_selected.display(self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y))

    # def signal2Floor(self, ele):
    #     y_loc = ele.geometry().y()
    #     return self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y_loc)

    def getEleFloor(self, name):
        '''
        obtain the current floor of each ele
        '''
        y_loc = [i for i in self.elecars if i.ele_name == name][0].geometry().y()
        floor = self._calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y_loc)
        print(floor)
        return floor


    def _moveToOne(self, name, target):
        '''
        to one place
        :param name:
        :param target:
        :return:
        '''
        ele = [i for i in self.elecars if i.ele_name == name][0]
        cur_floor = self.getEleFloor(name)
        if cur_floor < target:
            while cur_floor < target:
                self.up(ele.order)
                time.sleep(0.05)
                cur_floor = self.getEleFloor(name)
            self.stop(ele.order)
        elif cur_floor > target:
            while cur_floor > target:
                self.down(ele.order)
                time.sleep(0.05)
                cur_floor = self.getEleFloor(ele)
            self.stop(ele.order)
        else:
            pass

    def _entireMove(self, name, src, des):
        '''
        a whole movement to a given destination floor, first move to the floor where the passenger is, and then the destination floor
        :param des, ele
        :return: the elecar aminaiton
        '''
        # first step: to src
        self._moveToOne(name, src)
        # second step: to des
        self._moveToOne(name, des)


    def executeRoute(self, route):
        '''
        execute the route given, simulate the movement of elecars
        :param route:a list containing which ele you should take and in which floor you should change ele
        :return: execute the whole route
        '''
        if len(route) == 3:
            src = route[0]
            picked_ele = route[1]
            des = route[2]
            ele = picked_ele #[i for i in self.elecars if i.ele_name == picked_ele][0]  # fetch the ele using the given name
            self._entireMove(ele, src, des)
        elif len(route) == 6:
            src = route[0]
            picked_ele1 = route[1]
            temp = route[2]
            picked_ele2 = route[3]
            des = route[4]
            ele1 = picked_ele1 #[i for i in self.elecars if i.ele_name == picked_ele1][0]  # fetch the ele using the given name
            ele2 = picked_ele2 #[i for i in self.elecars if i.ele_name == picked_ele2][0]  # fetch the ele using the given name
            self._entireMove(ele1, src, temp)
            self._entireMove(ele2, temp, des)
        else:
            pass


    def demoMotion(self):
        self.up(3)
        self.down(5)
        self.up(6)
        self.down(4)



    # @staticmethod
    def _calculateFloor(self, fr_num, f_height, loc_y):
        # the simple way, just one line, not work now!
        # return sum(map(lambda j: (fr_num - j) if (50 + f_height / fr_num * j) <= loc_y < (50 + f_height / fr_num * (j + 1)) else 0, range(fr_num)))

        # a more concrete way；
        for i in range(1, fr_num + 1):
            if i == 1:
                # make sure the 1st floor displayed properly
                L = self.margin + f_height / fr_num * (fr_num - i + 1) + 1
            U = self.margin + f_height / fr_num * (fr_num - (i + 1) + 1)
            if U <= loc_y < L:
                return i
            # else:
            #     return 999

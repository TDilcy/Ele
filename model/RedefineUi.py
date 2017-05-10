# -*- utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtCore import QRect
# from model.ele import Ui_MainWindow
# from model.ele_version5_3 import Ui_MainWindow
from model.ele_version5_3_2 import Ui_MainWindow
# from model.ele_3_27 import Ui_MainWindow
# from model.ele_bak import Ui_MainWindow
from model.ElevatorCar import ElevatorCar


class RedefineUi(QtGui.QMainWindow):

    def __init__(self):
        super(RedefineUi, self).__init__()
        self.ui = Ui_MainWindow()
        # use the QtGui.QMainWindow to initiate the UI
        self.ui.setupUi(self)
        # self.initScrollArea()
        self.WIDTH = self.ui.frame_1.geometry().width()
        self.HEIGHT = self.ui.frame_1.geometry().height()
        self.Y = self.ui.frame_1.geometry().y()
        self.X = self.ui.frame_1.geometry().x()
        self.ele_height = 30
        self.fr_num = 60
        self.lcds = [self.ui.lcd1, self.ui.lcd2, self.ui.lcd3, self.ui.lcd4, self.ui.lcd5, self.ui.lcd6, self.ui.lcd7]
        # the value in self.movin_range represents the upper and lower bound of elecar
        self.moving_range = {'U1': (self.Y, self.Y + self.HEIGHT * 0.75 - self.ele_height),
                             'U2': (self.Y, self.Y + self.HEIGHT * 0.5 - self.ele_height),
                             'U3': (self.Y, self.Y + self.HEIGHT * 0.25 - self.ele_height),
                             'L1': (self.Y, self.Y + self.HEIGHT - self.ele_height),
                             'L2': (self.Y + self.HEIGHT * 0.75, self.Y + self.HEIGHT - self.ele_height),
                             'L3': (self.Y + self.HEIGHT * 0.5, self.Y + self.HEIGHT - self.ele_height),
                             'L4': (self.Y + self.HEIGHT * 0.25, self.Y + self.HEIGHT - self.ele_height)}

        self.setGeometry(500, 100, 600, 700)
        self.initFrames()
        self.init_splitters()
        self.elecars, self.init_y_list = self.initEleCars()

        self.initLcds(self.init_y_list)
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

    def initFrames(self):
        self.ui.frame_2.setGeometry(self.frame_X(self.X, self.WIDTH, 2), self.Y,
                                    self.WIDTH, self.HEIGHT)
        self.ui.frame_3.setGeometry(self.frame_X(self.X, self.WIDTH, 3), self.Y,
                                    self.WIDTH, self.HEIGHT)
        self.ui.frame_4.setGeometry(self.frame_X(self.X, self.WIDTH, 4), self.Y,
                                    self.WIDTH, self.HEIGHT)
        # self.ui.frame_5.setGeometry(self.frame_X(5), self.Y, self.WIDTH, self.HEIGHT)
        # self.ui.frame_6.setGeometry(self.frame_X(6), self.Y, self.WIDTH, self.HEIGHT)
        # self.ui.frame_7.setGeometry(self.frame_X(7), self.Y, self.WIDTH, self.HEIGHT)

    def init_splitters(self):
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
        self.ui.splitter_2.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 1) + 20, S_Y + 30, S_WIDTH * 0.6, 30))
        self.ui.splitter_3.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 2), S_Y + 20, S_WIDTH, 60))
        self.ui.splitter_4.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 3), S_Y + 20, S_WIDTH, 60))
        self.ui.splitter_5.setGeometry(QRect(self.splitter_X(self.X, self.WIDTH, 4), S_Y + 20, S_WIDTH, 60))

    @staticmethod
    def splitter_X(X, width, n):
        # this should be a staticmethod????
        return int(X + (2 * n - 1) * width * 0.1 + (n - 1) * width * 0.8)

    @staticmethod
    def frame_X(X, width, n):
        return X + (n - 1) * width

    def initEleCars(self):
        '''
        initiate the ele_box in the gui, return a list contains all of them
        '''
        HEIGHT = 30
        WIDTH = self.ui.frame_1.width()
        elecar1 = ElevatorCar(1, 'L1', self)
        elecar1.setGeometry(self.ui.frame_1.geometry().x(),
                            self.moving_range['L1'][1],
                            WIDTH, HEIGHT)
        elecar2 = ElevatorCar(2, 'L2', self)
        elecar2.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['L2'][1],
                            WIDTH, HEIGHT)

        # elecar3 = ElevatorCar(3, 'L3', self)
        # elecar3.setGeometry(self.ui.frame_3.geometry().x(),
        #                     self.moving_range['L3'][1],
        #                     WIDTH, HEIGHT)
# #############temp###############################################
        elecar3 = ElevatorCar(3, 'L3', self)
        elecar3.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['L3'][1] - 200,
                            WIDTH, HEIGHT)
# #############temp###############################################
        elecar4 = ElevatorCar(4, 'L4', self)
        elecar4.setGeometry(self.ui.frame_4.geometry().x(),
                            self.moving_range['L4'][1],
                            WIDTH, HEIGHT)

        # frame5,6,7 are no longer exist, and frame 2,3,4 are holding two
        # elecars each
        elecar5 = ElevatorCar(5, 'U1', self)
        elecar5.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['U1'][1],
                            WIDTH, HEIGHT)
        elecar6 = ElevatorCar(6, 'U2', self)
        elecar6.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['U2'][1],
                            WIDTH, HEIGHT)
        elecar7 = ElevatorCar(7, 'U3', self)
        elecar7.setGeometry(self.ui.frame_4.geometry().x(),
                            self.moving_range['U3'][1],
                            WIDTH, HEIGHT)
        elecars = [elecar1, elecar2, elecar3, elecar4, elecar5, elecar6, elecar7]
        # this y_list is for move function
        init_y_list = [ele.geometry().y() for ele in elecars]
        return elecars, init_y_list

    def initLcds(self, y_list):
        '''
        show the init_floor the elecar locates
        y_list stores the y_position of the elecars
        '''
        for ind, lcd in enumerate(self.lcds):
            lcd.display(self.calculateFloor(self.fr_num, self.HEIGHT, y_list[ind] + self.ele_height))

    def up(self, order):
        self.elecars[order].moveUp()
        self.elecars[order].thread.obj_signal.connect(self.move)

    def down(self, order):
        self.elecars[order].moveDown()
        self.elecars[order].thread.obj_signal.connect(self.move)

    # def stop(self, order):
    #     self.elecars[order].moveStop()
    #     self.elecars[order].thread.obj_signal.connect(self.move)

    def move(self, ele):
        '''
        important issue: the refresh operation should be put at the main thread rather than the sub-thread, otherwise, it will crash.
        '''
        # # the x, y position of the elebox
        x = ele.geometry().x()
        y = ele.geometry().y()
        # set the moving range for the upper elecars and the lowwer elecars
        top_margin = self.moving_range[ele.location][0]
        buttom_margin = self.moving_range[ele.location][1]
        if ele.direction == "up":
            step = -2
        elif ele.direction == "down":
            step = 2
        y += step
        QtGui.QApplication.processEvents()
        while (y <= buttom_margin) & (y >= top_margin):
            ele.move(x, y)
            break

    def showFloor(self, ele):
        '''
        show which flow does the elecar locate in the correspondant lcd
        '''
        y = ele.geometry().y() + ele.height  # add ele.height to avoid lcd displaying 0 when arrive at the top floor'
        # top_margin = 50
        lcd_selected = self.lcds[self.elecars.index(ele)]
        # calculate the floor
        lcd_selected.display(self.calculateFloor(self.fr_num, self.HEIGHT, y))

    def demo_motion(self):
        '''
        show which flow does the elecar locate in the correspondant lcd
        '''
        import time
        self.up(1)
        time.sleep(10)
        self.down(2)
        # time.sleep(4)
        # self.up(2)


        # pass

    @staticmethod
    def calculateFloor(fr_num, f_height, loc_y):
        # the simple way, just one line
        return sum(map(lambda j: (fr_num - j) if (50 + f_height / fr_num * j) <= loc_y < (50 + f_height / fr_num * (j + 1)) else 0, range(fr_num)))

        # a more concrete way；
        # for i in range(fr_num):
        #     L = 50 + f_height / fr_num * i
        #     U = 50 + f_height / fr_num * (i + 1)
        #     if L <= loc_y <= U:
        #         flr = fr_num - i
        # return flr

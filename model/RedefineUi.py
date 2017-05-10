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
        self.ele_height = 15
        self.margin = 30
        self.initFrame1(90, self.margin, 100, 600 + self.ele_height)
        self.WIDTH = self.ui.frame_1.geometry().width()
        self.HEIGHT = self.ui.frame_1.geometry().height()
        self.Y = self.ui.frame_1.geometry().y()
        self.X = self.ui.frame_1.geometry().x()

        self.fr_num = 60  # the total floor of the building
        self.lcds = [self.ui.lcd1, self.ui.lcd2, self.ui.lcd3, self.ui.lcd4, self.ui.lcd5, self.ui.lcd6, self.ui.lcd7]
        # the value in self.movin_range represents the upper and lower bound of elecar
        self.moving_range = {'U1': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.75),
                             'U2': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.5),
                             'U3': (self.Y, self.Y + (self.HEIGHT - self.ele_height) * 0.25),
                             'L1': (self.Y, self.Y + (self.HEIGHT - self.ele_height)),
                             'L2': (self.Y + (self.HEIGHT - self.ele_height) * 0.75, self.Y + (self.HEIGHT - self.ele_height)),
                             'L3': (self.Y + (self.HEIGHT - self.ele_height) * 0.5, self.Y + (self.HEIGHT - self.ele_height)),
                             'L4': (self.Y + (self.HEIGHT - self.ele_height) * 0.25, self.Y + (self.HEIGHT - self.ele_height))}

        self.setGeometry(500, 100, 600, 700)
        self.initFrames()
        self.init_splitters()
        self.elecars, self.init_y_list = self.initEleCars()

        self.initLcds(self.init_y_list)
        # self.initBounds()
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
    def initFrame1(self, fX, fY, fWidth, fHeight):
        '''
        set the initial frame which is a standard one for others' position
        '''
        self.ui.frame_1.setGeometry(fX, fY, fWidth, fHeight)

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

    def initEleCars(self):
        '''
        initiate the ele_box in the gui, return a list contains all of them
        '''
        HEIGHT = self.ele_height
        WIDTH = self.ui.frame_1.width()
        elecar1 = ElevatorCar(1, 'L1', self)
        elecar1.setGeometry(self.ui.frame_1.geometry().x(),
                            self.moving_range['L1'][1],
                            WIDTH, HEIGHT)
        elecar2 = ElevatorCar(2, 'L2', self)
        elecar2.setGeometry(self.ui.frame_2.geometry().x(),
                            self.moving_range['L2'][1],
                            WIDTH, HEIGHT)

        # elecar2 = ElevatorCar(2, 'L2', self)
        # elecar2.setGeometry(self.ui.frame_2.geometry().x(),
        #                     self.moving_range['U1'][1],
        #                     WIDTH, HEIGHT)

        elecar3 = ElevatorCar(3, 'L3', self)
        elecar3.setGeometry(self.ui.frame_3.geometry().x(),
                            self.moving_range['L3'][1],
                            WIDTH, HEIGHT)

# #############temp###############################################
        # elecar3 = ElevatorCar(3, 'L3', self)
        # elecar3.setGeometry(10,
        #                     10,
        #                     WIDTH, HEIGHT)
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
            lcd.display(self.calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y_list[ind]))

    def initBounds(self):
        # the y_loc of B_bound is a relative distance not the absolute one
        self.ui.B_bound.setGeometry(0, 10,
                                    self.WIDTH, 2)
        self.ui.C_bound.setGeometry(0, (self.HEIGHT - self.ele_height) * 0.5,
                                    self.WIDTH, 2)
        self.ui.D_bound.setGeometry(0, (self.HEIGHT - self.ele_height) * 0.25,
                                    self.WIDTH, 2)
        pass

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
        y = ele.geometry().y() #  + ele.height  # add ele.height to avoid lcd displaying 0 when arrive at the top floor'
        # top_margin = 50
        lcd_selected = self.lcds[self.elecars.index(ele)]
        # calculate the floor
        lcd_selected.display(self.calculateFloor(self.fr_num, self.HEIGHT - self.ele_height, y))

    def demo_motion(self):
        '''
        show which flow does the elecar locate in the correspondant lcd
        '''
        import time
        self.up(0)
        self.up(1)
        self.up(2)
        self.up(3)
        # self.up(4)
        # self.up(5)
        # self.up(6)
        # time.sleep(2)
        # self.down(2)
        # time.sleep(4)
        # self.up(2)
        # pass

    # @staticmethod
    def calculateFloor(self, fr_num, f_height, loc_y):
        # the simple way, just one line
        # return sum(map(lambda j: (fr_num - j) if (50 + f_height / fr_num * j) <= loc_y < (50 + f_height / fr_num * (j + 1)) else 0, range(fr_num)))

        # a more concrete way；
        for i in range(1, fr_num + 1):
            if i == 1:
                # make sure the 1st floor displayed properly
                L = self.margin + f_height / fr_num * (fr_num - i + 1) + 1
            U = self.margin + f_height / fr_num * (fr_num - (i + 1) + 1)
            # print(L)
            # print(U)
            if U <= loc_y < L:
                return i
            # else:
            #     return 999

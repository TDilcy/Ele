import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from move_test import Ui_MainWindow
import time


class myWindow(QtGui.QMainWindow):
    """example of get the y_loc of a moving label"""
    # y_sig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(myWindow, self).__init__()
        # self.resize(300, 500)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.ele_car.connect(lambda: self.ui.ele_y_broswer.setText(self.ui.ele_car.geometry().y()))
        # self.ui.info_button.clicked.connect(self.show_y)
        self.ui.ele_car.y_loc_signal.connect(self.ui.ele_y_broswer.setText)

        self.ui.run_button.clicked.connect(self.move_ele)
        # self.ui.run_button.clicked.connect(self.show_y)
        self.ui.reset_button.clicked.connect(self.reset_ele)

    def move_ele(self):
        ele = self.ui.ele_car
        y = ele.geometry().y()
        # print(ele.geometry().y())
        step = 1
        for i in range(300):
            y += step
            self.ui.ele_car.new_move(ele.geometry().x(), y)
            QtGui.QApplication.processEvents()
            # print(ele.geometry().y())
            # self.y_sig.emit(str(self.ui.ele_car.geometry().y()))
            # self.ui.ele_y_broswer.setText(str(self.ui.ele_car.geometry().y()))
            time.sleep(0.05)
        # print('final_loc: {}'.format(ele.geometry().y()))

    def reset_ele(self):
        self.ui.setupUi(self)

    def show_y(self, text):
        self.y_sig.connect(self.ui.ele_y_broswer.setText)
        # self.y_sig.connect(lambda: self.ui.ele_y_broswer.setText())

    # def print_y(self):
    #     y = self.ui.ele_car.y_loc_signal.
    #     print(y)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())

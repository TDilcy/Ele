# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'move_test.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.run_button = QtGui.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(450, 200, 75, 23))
        self.run_button.setObjectName(_fromUtf8("run_button"))
        # self.ele_car = QtGui.QLabel(self.centralwidget)
        # self.ele_car.setGeometry(QtCore.QRect(200, 200, 71, 21))
        # self.ele_car.setFrameShape(QtGui.QFrame.Panel)
        # self.ele_car.setFrameShadow(QtGui.QFrame.Raised)
        # self.ele_car.setObjectName(_fromUtf8("ele_car"))

        self.ele_car = new_label(self.centralwidget)
        self.ele_car.setGeometry(QtCore.QRect(100, 200, 71, 21))
        self.ele_car.setFrameShape(QtGui.QFrame.Panel)
        self.ele_car.setFrameShadow(QtGui.QFrame.Raised)
        self.ele_car.setObjectName(_fromUtf8("new_ele_car"))

        self.ele_y_broswer = QtGui.QTextBrowser(self.centralwidget)
        self.ele_y_broswer.setGeometry(QtCore.QRect(440, 40, 101, 71))
        self.ele_y_broswer.setObjectName(_fromUtf8("ele_y_broswer"))
        self.reset_button = QtGui.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(450, 250, 75, 23))
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.info_button = QtGui.QPushButton(self.centralwidget)
        self.info_button.setGeometry(QtCore.QRect(450, 310, 75, 23))
        self.info_button.setObjectName(_fromUtf8("info_button"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.run_button.setText(_translate("MainWindow", "run", None))
        # self.ele_car.setText(_translate("MainWindow", "ele_sample", None))
        self.ele_car.setText(_translate("MainWindow", "ele_sample", None))
        self.reset_button.setText(_translate("MainWindow", "reset", None))
        self.info_button.setText(_translate("MainWindow", "print_info", None))


class new_label(QtGui.QLabel):
    """docstring for new_label"""
    y_loc_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(new_label, self).__init__(parent)

    def new_move(self, x, y):
        self.move(x, y)
        self.y_loc_signal.emit(str(self.geometry().y()))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

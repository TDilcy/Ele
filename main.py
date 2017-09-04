# -*- coding: utf-8 -*-
# date: 2017-05-03
import sys

from PyQt4 import QtGui

from model.MainWindow import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    # print('the main thread loaded in main is\n{}'.format(QThread.currentThread()))
    window.show()
    sys.exit(app.exec_())

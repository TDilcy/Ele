# -*- coding: utf-8 -*-
# date: 2017-05-03
import sys

from PyQt4 import QtGui

from model.MainWindow import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
'''
TODO:
标题： 一井道七轿厢超级电梯调度模拟系统
语言： 中文
布局： 去掉无关按键
'''

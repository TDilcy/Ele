# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ele_version5_3_2.ui'
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
        MainWindow.setEnabled(True)
        MainWindow.resize(1536, 1089)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame_1 = QtGui.QFrame(self.centralwidget)
        self.frame_1.setGeometry(QtCore.QRect(90, 30, 100, 600))
        self.frame_1.setFrameShape(QtGui.QFrame.Box)
        self.frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_1.setLineWidth(1)
        self.frame_1.setMidLineWidth(0)
        self.frame_1.setObjectName(_fromUtf8("frame_1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(190, 30, 100, 591))
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(0)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.B_bound = QtGui.QFrame(self.frame_2)
        self.B_bound.setEnabled(True)
        self.B_bound.setGeometry(QtCore.QRect(0, 380, 80, 16))
        self.B_bound.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.B_bound.setFrameShadow(QtGui.QFrame.Raised)
        self.B_bound.setLineWidth(2)
        self.B_bound.setFrameShape(QtGui.QFrame.HLine)
        self.B_bound.setObjectName(_fromUtf8("B_bound"))
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(310, 30, 100, 601))
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.frame_3.setMidLineWidth(0)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.C_bound = QtGui.QFrame(self.frame_3)
        self.C_bound.setGeometry(QtCore.QRect(10, 230, 74, 6))
        self.C_bound.setFrameShadow(QtGui.QFrame.Raised)
        self.C_bound.setLineWidth(2)
        self.C_bound.setFrameShape(QtGui.QFrame.HLine)
        self.C_bound.setObjectName(_fromUtf8("C_bound"))
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(430, 60, 100, 591))
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setLineWidth(1)
        self.frame_4.setMidLineWidth(0)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.D_bound = QtGui.QFrame(self.frame_4)
        self.D_bound.setGeometry(QtCore.QRect(10, 100, 80, 16))
        self.D_bound.setFrameShadow(QtGui.QFrame.Raised)
        self.D_bound.setLineWidth(2)
        self.D_bound.setFrameShape(QtGui.QFrame.HLine)
        self.D_bound.setObjectName(_fromUtf8("D_bound"))
        self.splitter_10 = QtGui.QSplitter(self.centralwidget)
        self.splitter_10.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.splitter_10.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_10.setObjectName(_fromUtf8("splitter_10"))
        self.confirm_button = QtGui.QPushButton(self.centralwidget)
        self.confirm_button.setEnabled(True)
        self.confirm_button.setGeometry(QtCore.QRect(950, 180, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm_button.setFont(font)
        self.confirm_button.setObjectName(_fromUtf8("confirm_button"))
        self.splitter_3 = QtGui.QSplitter(self.centralwidget)
        self.splitter_3.setGeometry(QtCore.QRect(190, 640, 81, 61))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.layoutWidget = QtGui.QWidget(self.splitter_3)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.lcd5 = QtGui.QLCDNumber(self.layoutWidget)
        self.lcd5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd5.setAutoFillBackground(True)
        self.lcd5.setSmallDecimalPoint(False)
        self.lcd5.setNumDigits(2)
        self.lcd5.setDigitCount(2)
        self.lcd5.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd5.setProperty("value", 3.0)
        self.lcd5.setProperty("intValue", 3)
        self.lcd5.setObjectName(_fromUtf8("lcd5"))
        self.verticalLayout_8.addWidget(self.lcd5)
        self.lcd2 = QtGui.QLCDNumber(self.layoutWidget)
        self.lcd2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd2.setAutoFillBackground(True)
        self.lcd2.setSmallDecimalPoint(False)
        self.lcd2.setNumDigits(2)
        self.lcd2.setDigitCount(2)
        self.lcd2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd2.setProperty("value", 3.0)
        self.lcd2.setProperty("intValue", 3)
        self.lcd2.setObjectName(_fromUtf8("lcd2"))
        self.verticalLayout_8.addWidget(self.lcd2)
        self.layoutWidget1 = QtGui.QWidget(self.splitter_3)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_7.addWidget(self.label_4)
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_7.addWidget(self.label_5)
        self.splitter_4 = QtGui.QSplitter(self.centralwidget)
        self.splitter_4.setGeometry(QtCore.QRect(310, 650, 71, 61))
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName(_fromUtf8("splitter_4"))
        self.layoutWidget2 = QtGui.QWidget(self.splitter_4)
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.lcd6 = QtGui.QLCDNumber(self.layoutWidget2)
        self.lcd6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd6.setAutoFillBackground(True)
        self.lcd6.setSmallDecimalPoint(False)
        self.lcd6.setNumDigits(2)
        self.lcd6.setDigitCount(2)
        self.lcd6.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd6.setProperty("value", 3.0)
        self.lcd6.setProperty("intValue", 3)
        self.lcd6.setObjectName(_fromUtf8("lcd6"))
        self.verticalLayout_9.addWidget(self.lcd6)
        self.lcd3 = QtGui.QLCDNumber(self.layoutWidget2)
        self.lcd3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd3.setAutoFillBackground(True)
        self.lcd3.setSmallDecimalPoint(False)
        self.lcd3.setNumDigits(2)
        self.lcd3.setDigitCount(2)
        self.lcd3.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd3.setProperty("value", 3.0)
        self.lcd3.setProperty("intValue", 3)
        self.lcd3.setObjectName(_fromUtf8("lcd3"))
        self.verticalLayout_9.addWidget(self.lcd3)
        self.layoutWidget3 = QtGui.QWidget(self.splitter_4)
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.label_8 = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_10.addWidget(self.label_8)
        self.label_7 = QtGui.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_10.addWidget(self.label_7)
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(60, 680, 51, 41))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.lcd1 = QtGui.QLCDNumber(self.splitter_2)
        self.lcd1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd1.setAutoFillBackground(True)
        self.lcd1.setSmallDecimalPoint(False)
        self.lcd1.setNumDigits(2)
        self.lcd1.setDigitCount(2)
        self.lcd1.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd1.setProperty("value", 3.0)
        self.lcd1.setProperty("intValue", 3)
        self.lcd1.setObjectName(_fromUtf8("lcd1"))
        self.label_6 = QtGui.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.splitter_5 = QtGui.QSplitter(self.centralwidget)
        self.splitter_5.setGeometry(QtCore.QRect(441, 651, 55, 54))
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName(_fromUtf8("splitter_5"))
        self.layoutWidget4 = QtGui.QWidget(self.splitter_5)
        self.layoutWidget4.setObjectName(_fromUtf8("layoutWidget4"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.lcd7 = QtGui.QLCDNumber(self.layoutWidget4)
        self.lcd7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd7.setAutoFillBackground(True)
        self.lcd7.setSmallDecimalPoint(False)
        self.lcd7.setNumDigits(2)
        self.lcd7.setDigitCount(2)
        self.lcd7.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd7.setProperty("value", 3.0)
        self.lcd7.setProperty("intValue", 3)
        self.lcd7.setObjectName(_fromUtf8("lcd7"))
        self.verticalLayout_12.addWidget(self.lcd7)
        self.lcd4 = QtGui.QLCDNumber(self.layoutWidget4)
        self.lcd4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd4.setAutoFillBackground(True)
        self.lcd4.setSmallDecimalPoint(False)
        self.lcd4.setNumDigits(2)
        self.lcd4.setDigitCount(2)
        self.lcd4.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd4.setProperty("value", 3.0)
        self.lcd4.setProperty("intValue", 3)
        self.lcd4.setObjectName(_fromUtf8("lcd4"))
        self.verticalLayout_12.addWidget(self.lcd4)
        self.layoutWidget5 = QtGui.QWidget(self.splitter_5)
        self.layoutWidget5.setObjectName(_fromUtf8("layoutWidget5"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.label_10 = QtGui.QLabel(self.layoutWidget5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_13.addWidget(self.label_10)
        self.label_9 = QtGui.QLabel(self.layoutWidget5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_13.addWidget(self.label_9)
        self.layoutWidget6 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget6.setGeometry(QtCore.QRect(721, 151, 198, 73))
        self.layoutWidget6.setObjectName(_fromUtf8("layoutWidget6"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.layoutWidget6)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.src_floor_box = QtGui.QSpinBox(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.src_floor_box.setFont(font)
        self.src_floor_box.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.src_floor_box.setMinimum(1)
        self.src_floor_box.setMaximum(60)
        self.src_floor_box.setObjectName(_fromUtf8("src_floor_box"))
        self.horizontalLayout_2.addWidget(self.src_floor_box)
        self.des_floor_box = QtGui.QSpinBox(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.des_floor_box.setFont(font)
        self.des_floor_box.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.des_floor_box.setMinimum(1)
        self.des_floor_box.setMaximum(60)
        self.des_floor_box.setObjectName(_fromUtf8("des_floor_box"))
        self.horizontalLayout_2.addWidget(self.des_floor_box)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(670, 240, 541, 231))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(1)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget7 = QtGui.QWidget(self.splitter)
        self.layoutWidget7.setObjectName(_fromUtf8("layoutWidget7"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget7)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_3 = QtGui.QLabel(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_6.addWidget(self.label_3)
        self.pass_info_broswer = QtGui.QTextBrowser(self.layoutWidget7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pass_info_broswer.setFont(font)
        self.pass_info_broswer.setObjectName(_fromUtf8("pass_info_broswer"))
        self.verticalLayout_6.addWidget(self.pass_info_broswer)
        self.layoutWidget_2 = QtGui.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.label_11 = QtGui.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.verticalLayout_11.addWidget(self.label_11)
        self.sch_info_broswer = QtGui.QTextBrowser(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sch_info_broswer.setFont(font)
        self.sch_info_broswer.setObjectName(_fromUtf8("sch_info_broswer"))
        self.verticalLayout_11.addWidget(self.sch_info_broswer)
        self.layoutWidget8 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget8.setGeometry(QtCore.QRect(670, 470, 541, 141))
        self.layoutWidget8.setObjectName(_fromUtf8("layoutWidget8"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget8)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_12 = QtGui.QLabel(self.layoutWidget8)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.verticalLayout_2.addWidget(self.label_12)
        self.chg_info_broswer = QtGui.QTextBrowser(self.layoutWidget8)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chg_info_broswer.setFont(font)
        self.chg_info_broswer.setObjectName(_fromUtf8("chg_info_broswer"))
        self.verticalLayout_2.addWidget(self.chg_info_broswer)
        self.layoutWidget9 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget9.setGeometry(QtCore.QRect(1090, 160, 81, 71))
        self.layoutWidget9.setObjectName(_fromUtf8("layoutWidget9"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget9)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.clear_button = QtGui.QPushButton(self.layoutWidget9)
        self.clear_button.setObjectName(_fromUtf8("clear_button"))
        self.verticalLayout_3.addWidget(self.clear_button)
        self.shuffle_button = QtGui.QPushButton(self.layoutWidget9)
        self.shuffle_button.setObjectName(_fromUtf8("shuffle_button"))
        self.verticalLayout_3.addWidget(self.shuffle_button)
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(640, 40, 631, 61))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("黑体"))
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.splitter_3.raise_()
        self.splitter_4.raise_()
        self.splitter_2.raise_()
        self.splitter_5.raise_()
        self.splitter.raise_()
        self.confirm_button.raise_()
        self.frame_1.raise_()
        self.frame_2.raise_()
        self.frame_3.raise_()
        self.frame_4.raise_()
        self.splitter_10.raise_()
        self.layoutWidget.raise_()
        self.label_13.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1536, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Elevator", None))
        self.confirm_button.setText(_translate("MainWindow", "确认", None))
        self.label_4.setText(_translate("MainWindow", "B2", None))
        self.label_5.setText(_translate("MainWindow", "B1", None))
        self.label_8.setText(_translate("MainWindow", "C2", None))
        self.label_7.setText(_translate("MainWindow", "C1", None))
        self.label_6.setText(_translate("MainWindow", "A", None))
        self.label_10.setText(_translate("MainWindow", "D2", None))
        self.label_9.setText(_translate("MainWindow", "D1", None))
        self.label.setText(_translate("MainWindow", "呼梯楼层", None))
        self.label_2.setText(_translate("MainWindow", "目的楼层", None))
        self.label_3.setText(_translate("MainWindow", "乘客信息", None))
        self.pass_info_broswer.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_11.setText(_translate("MainWindow", "调度信息", None))
        self.sch_info_broswer.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_12.setText(_translate("MainWindow", "换乘信息", None))
        self.chg_info_broswer.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.clear_button.setText(_translate("MainWindow", "重置", None))
        self.shuffle_button.setText(_translate("MainWindow", "随机", None))
        self.label_13.setText(_translate("MainWindow", "一井道七轿厢超级电梯调度模拟系统", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# import sys
# from PyQt4 import QtCore, QtGui
# # import classblock
#
#
# class MainWindow(QtGui.QMainWindow):
#     def __init__(self, parent=None):
#         QtGui.QMainWindow.__init__(self, parent)
#         w = QtGui.QWidget()
#         self.setCentralWidget(w)
#
#         topFiller = QtGui.QWidget()
#         topFiller.setMinimumSize(1200, 1200)
#         for i in range(1, 40):
#             label = QtGui.QLabel("<--------->", topFiller)
#             label.move(i * 10, i * 10)
#
#         scroll = QtGui.QScrollArea()
#         scroll.setWidget(topFiller)
#         scroll.setAutoFillBackground(True)
#         scroll.setWidgetResizable(True)
#
#         vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(scroll)
#         w.setLayout(vbox)
#
#         self.statusBar().showMessage(self.tr("A context menu is available by right-clicking"))
#         self.setWindowTitle(self.tr("Menus"))
#         self.resize(480, 320)
#
#
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     mainwindow = MainWindow()
#     mainwindow.show()
#     sys.exit(app.exec_())

class A():
    def __init__(self, pa1):
        self.pa = pa1
        self.b = B(6)

class B():
    b1 = 'static_b1'
    def __init__(self, pb1):
        self.pb1 = pb1

a1 = A(4)
a2 = a1
a2.b = B(7)
# a2.b.pb1 = 10
a2.b.b1 = 'hhhhe'
# print(a.p1)
print(a1.b.b1)
print(a2.b.b1)
# print(id(a1))
# print(id(a2))


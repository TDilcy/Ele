import sys
from PyQt4 import QtCore, QtGui
# import classblock


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        w = QtGui.QWidget()
        self.setCentralWidget(w)

        topFiller = QtGui.QWidget()
        topFiller.setMinimumSize(1200, 1200)
        for i in range(1, 40):
            label = QtGui.QLabel("<--------->", topFiller)
            label.move(i * 10, i * 10)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(topFiller)
        scroll.setAutoFillBackground(True)
        scroll.setWidgetResizable(True)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(scroll)
        w.setLayout(vbox)

        self.statusBar().showMessage(self.tr("A context menu is available by right-clicking"))
        self.setWindowTitle(self.tr("Menus"))
        self.resize(480, 320)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
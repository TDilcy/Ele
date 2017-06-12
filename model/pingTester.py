# -*- coding: utf-8 -*-
 
import sys
import time
import subprocess
from threading import Thread
import re
from PyQt4.QtGui import QMainWindow, QApplication, QStandardItemModel, QStandardItem, QWidget, QVBoxLayout, QTableView
from PyQt4.QtCore import pyqtSignature, Qt, QTimer, SIGNAL, QString, QMetaObject
from Queue import Queue
 
#from Ui_main import Ui_MainWindow
 
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(500, 435)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QTableView(self.centralWidget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralWidget)
 
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
 
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Ping Tester", None, QApplication.UnicodeUTF8))
 
if sys.platform.startswith('linux'):
    getdata = re.compile(r"icmp_req=(\d+) ttl=(\d+) time=([\d\.]+)\sms")
    pingstr = ["ping", "-n", "-i 0.2"]
    filtered = "Packet filtered"
    delaytime = 200
else:
    getdata = re.compile(r"=([\d\.]+)ms TTL=(\d+)")
    pingstr = ["ping.exe", "-t"]
    timeout = "Request timed out."
    delaytime = 500
 
try:
    with open("ips.conf", "r") as f:
        t_node = f.read().decode('utf-8')
        if not t_node:
            raise IOError
except IOError:
    with open("ips.conf", "w") as f:
        t_node = u"""
        210.51.176.182-北京联通BGP
        202.97.224.68-黑龙江网通
        202.99.96.68-天津网通
        202.99.160.68-河北网通
        202.96.69.38-大连网通
        221.208.172.1-哈尔滨网通
        202.99.192.68-山西网通
        202.99.160.68-河北网通
        210.52.149.2-湖北网通
        218.30.64.121-湖南电信
        202.100.4.15-陕西电信 
        202.96.199.133-上海电信 
        219.150.150.150-河南电信 
        219.146.0.130-黑龙江电信
        202.98.96.68-四川电信
        59.66.4.50-北京教育网
        202.112.26.246-上海教育网
        202.114.0.254-武汉教育网
        211.161.159.9-武汉长城宽带
        143.90.12.170-日本东京odn
        202.160.123.5-新加坡Host1Plus
        60.199.17.138-台湾固网
        220.128.152.1-台湾HINET
        168.95.1.1-台湾中华电信
        202.65.207.1-香港DYX
        202.181.171.1-香港HKCIX
        203.169.186.1-香港NTT.HKNET
        59.148.193.38-香港HKCTI
        220.232.214.1-香港Supernet
        59.152.208.1-香港WTT
        210.56.48.1-香港HKSUN
        202.76.56.1-香港CPCNET
        218.213.250.130-香港SNL
        69.162.132.1-美国芝加哥Level3
        205.185.112.131-美国佛里蒙特HE
        204.152.221.1-美国洛杉矶nLayer
        178.63.62.208-德国Nuremburg
        94.23.202.83-法国OVH
        69.163.43.73-美国波特兰HE
        216.189.1.14-美国RockHill
        69.172.231.1-美国洛杉矶Peer1
        184.22.112.34-美国迈阿密HE
        199.48.146.37-美国圣琼斯
        216.245.208.1-美国达拉斯
        109.74.207.9-英国伦敦
        """
        f.write(t_node.encode('utf-8'))
 
node = []
for line in t_node.split('\n'):
    try:
        ip, desc = line.strip().split("-")
        node.append((ip, desc))
    except ValueError:
        pass
nodecount = len(node)
 
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.model = QStandardItemModel()
        self.model.setColumnCount(6)
        self.model.setRowCount(nodecount)
        self.model.setHorizontalHeaderLabels(["IP", "Description", "Loss%", "CurPing", "AvgPing", "TTL"])
        for i, (ip, desc) in enumerate(node):
            self.setitem(i, 0, ip)
            self.setitem(i, 1, desc)
            self.setitem(i, 2, "")
            self.setitem(i, 3, "")
            self.setitem(i, 4, "")
            self.setitem(i, 5, "")
        self.tableView.setModel(self.model)
        for i in range(len(node)):
            self.tableView.setRowHeight(i, 18)
        self.resizetable()
        self.timer = QTimer(self)
        self.connect(self.timer,
                     SIGNAL("timeout()"),
                     self.checkitems)
        self.timer.start(delaytime)
    
    def checkitems(self):
        while not q.empty():
            item = q.get()
            self.chgtxt(*item)
            q.task_done()
        self.resizetable()
    
    def resizetable(self):
        self.tableView.resizeColumnsToContents()
        
    def chgtxt(self, x, y, value):
        self.model.item(x, y).setText(value)
    
    def setitem(self, x, y, value):
        self.model.setItem(x, y, QStandardItem(value))
        
app = QApplication(sys.argv)
ui = MainWindow()
ui.show()
q = Queue()
 
def pinger(i, ip, desc):
    s = ""
    avgping = 0
    count = 0
    timeoutcount = 0
    ret = subprocess.Popen(pingstr + [ip],
                            stdout=subprocess.PIPE)
    while True:
        try:
            s += ret.stdout.read(1)
            
            tryfind = getdata.findall(s)
            if sys.platform.startswith('linux'):
                if len(tryfind) > 0:
                    req, ttl, crtping = tryfind[-1]
                    avgping += float(crtping)
                    count += 1
                    q.put((i, 3, crtping + "ms"))
                    q.put((i, 4, "%.2f" % (avgping * 1.0 / count) + "ms"))
                    q.put((i, 5, ttl))
                    q.put((i, 2, "%.2f" % ((int(req) - count) * 100.0 / int(req))))
                    s = ""
                elif filtered in s:
                    q.put((i, 2, "Failed"))
                    q.put((i, 3, "Failed"))
                    q.put((i, 4, "Failed"))
                    q.put((i, 5, "Failed"))
                    ret.kill()
                    s = ""
            else:
                if len(tryfind) > 0:
                    crtping, ttl = tryfind[-1]
                    avgping += float(crtping)
                    count += 1
                    q.put((i, 3, crtping + "ms"))
                    q.put((i, 4, "%.2f" % (avgping * 1.0 / count) + "ms"))
                    q.put((i, 5, ttl))
                    q.put((i, 2, "%.2f" % (timeoutcount * 100.0 / (count + timeoutcount))))
                elif timeout in s:
                    timeoutcount += 1
                    q.put((i, 2, "-"))
                    q.put((i, 3, "-"))
                    if count:
                        q.put((i, 5, "%.2f" % (timeoutcount * 100.0 / (count + timeoutcount))))
                    else:
                        q.put((i, 5, "-"))
                    s = ""
        except IOError:
            print(s)
            break
            
def startworkers():
    for i, (ip, desc) in enumerate(node):
        worker = Thread(target=pinger, args=(i, ip, desc))
        worker.setDaemon(True)
        worker.start()
        time.sleep(delaytime / 10000.0)
 
startthread = Thread(target=startworkers)
startthread.setDaemon(True)
startthread.start()
 
sys.exit(app.exec_())
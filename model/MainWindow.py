# -*- coding: utf-8 -*-
from model.RedefineUi import RedefineUi
from model.schedule import Schedule
import random


class MainWindow(RedefineUi):

    def __init__(self):
        super(MainWindow, self).__init__()
        # the demo of the schedule
        # the init_variables
        self.src = []
        self.des = []
        self.base_passager_info = ''
        self.pass_info = ''
        self.base_sch_info = ''
        self.sch_info = ''
        self.route = []
        self.scheduler = Schedule(self.elecars)

        # fetch the input and show the info in the textbroswer
        self.ui.confirm_button.clicked.connect(self._getSrcDes)
        self.ui.confirm_button.clicked.connect(lambda: self._setPassText(
            len(self.src), self.src[-1], '乘客呼梯'))
        self.ui.confirm_button.clicked.connect(
            lambda: self.ui.pass_info_broswer.setHtml(self.pass_info))

        # use different strategy
        self.ui.confirm_button.clicked.connect(self._chooseSchStrategy)
        # show the route being calculated
        self.ui.confirm_button.clicked.connect(lambda: self._setSchText(
            len(self.src), self.src[-1], self.des[-1], self.route))
        self.ui.confirm_button.clicked.connect(
            lambda: self.ui.sch_info_broswer.setHtml(self.sch_info))
        self.ui.confirm_button.clicked.connect(self.showChgText)
        # start the amitation
        self.ui.confirm_button.clicked.connect(lambda: self.executeRoute(self.route))
        # self.ui.confirm_button.clicked.connect(self.demoMotion)
########################        ##################################################
        # show the floor of the elevator
        self.elecars[0].obj_signal.connect(self.showFloor)
        self.elecars[1].obj_signal.connect(self.showFloor)
        self.elecars[2].obj_signal.connect(self.showFloor)
        self.elecars[3].obj_signal.connect(self.showFloor)
        self.elecars[4].obj_signal.connect(self.showFloor)
        self.elecars[5].obj_signal.connect(self.showFloor)
        self.elecars[6].obj_signal.connect(self.showFloor)

        # clear the des and route just for testing
        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.shuffle_button.clicked.connect(self.shuffle)

        self.ui.run_button.clicked.connect(self.demoMotion)
        # self.ui.run_button.clicked.connect(self.test_y_locs)
        self.ui.stop_button.clicked.connect(lambda: self.getEleFloor(3))







    def _getSrcDes(self):
        self.src.append(self.ui.src_floor_box.value())
        self.des.append(self.ui.des_floor_box.value())

    def _setPassText(self, record, src, info):
        self.base_passager_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{info_kind}</td>   </tr>'.format(
            rec=record, src=src, info_kind=info)
        # self.pass_info = '<table><tr>    <th>Record</th> <th>Floor</th> <th>Info</th>    </tr>{show_info}</table>'.format(
        #     show_info=self.base_passager_info)
        self.pass_info = '<table><tr>    <th>记录</th> <th>楼层</th> <th>信息</th>    </tr>{show_info}</table>'.format(
            show_info=self.base_passager_info)

    def _setSchText(self, record, src, des, route_info):
        '''
        two condition are considered: with or without elevator exchanged
        '''
        if len(route_info) == 3:
            self.base_sch_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{des}</td>  <td><b>{r1}</b>(<font color="#009933">{r2}</font>)</td>    </tr>'.format(rec=record, src=src, des=des, r1=route_info[-1], r2=route_info[1])
        elif len(route_info) == 6:
            self.base_sch_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{des}</td>  <td><b>{r1}</b>(<font color="#009933">{r2}</font>)——><b>{r3}</b>(<font color="#009933">{r4}</font>)</td>    </tr>'.format(rec=record, src=src, des=des, r1=route_info[2], r2=route_info[1], r3=route_info[4], r4=route_info[3])
        # self.sch_info = '<table><tr><th>Record</th>   <th>src</th>    <th>des</th>    <th>Route</th></tr>{show_info}</table>'.format(
        #     show_info=self.base_sch_info)
        self.sch_info = '<table><tr><th>记录</th>   <th>当前楼层</th>    <th>目的楼层</th>    <th>线路</th></tr>{show_info}</table>'.format(
            show_info=self.base_sch_info)

    def showChgText(self):
        if len(self.route) == 6:
            self.ui.chg_info_broswer.setHtml('<font color="#FF6666">{}</font>'.format(self.route[-1]))

    def _chooseSchStrategy(self):
        if len(self.des) <= 1:
            self.route = self.scheduler.one_command(self.src[-1], self.des[-1])
        else:
            self.route = self.scheduler.commands(self.src[-1], self.des[-1])
        print(self.route)

    def clear(self):
        self.des = []
        self.src = []
        self.route = []
        self.ui.pass_info_broswer.clear()
        self.ui.sch_info_broswer.clear()
        self.ui.chg_info_broswer.clear()
        # self.__init__()

    def shuffle(self):
        '''
        generate a random position for each elecar and update the corresponding lcd
        # TODO: ~~transform the result randomly generated into the floor num rather than just the y_loc~~
        '''
        for i in self.elecars:
            random.seed(666)
            # make the number generated transformed to the multiple of 10, so as to adapt the following condition:
            # the ele start at the floor where the passenger calls
            random_y = random.randint(self.moving_range[i.ele_name][0], self.moving_range[i.ele_name][1]) // 10 * 10
            # print('the y generated after ceiling is {}'.format(random_y))
            i.setGeometry(i.geometry().x(), random_y, i.geometry().width(), i.geometry().height())
            self.showFloor(i)

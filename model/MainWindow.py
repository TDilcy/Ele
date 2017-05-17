# -*- coding: utf-8 -*-
from model.RedefineUi import RedefineUi
from model.schedule import one_command, commands


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
        # fetch the input and show the info in the textbroswer
        self.ui.confirm_button.clicked.connect(self._getSrcDes)
        self.ui.confirm_button.clicked.connect(lambda: self._setPassText(
            len(self.src), self.src[-1], 'passager calls'))
        self.ui.confirm_button.clicked.connect(
            lambda: self.ui.pass_info_broswer.setHtml(self.pass_info))

        self.ui.confirm_button.clicked.connect(self._chooseSchStrategy)

        self.ui.confirm_button.clicked.connect(lambda: self._setSchText(
            len(self.src), self.src[-1], self.des[-1], self.route))
        self.ui.confirm_button.clicked.connect(
            lambda: self.ui.sch_info_broswer.setHtml(self.sch_info))
        # self.ui.confirm_button.clicked.connect(lambda: self.ui.sch_info_broswer.setHtml(html_demo_sch_info))
        # self.ui.confirm_button.clicked.connect(self.demo_motion)
        # self.ui.stop_button.clicked.connect(lambda: self.stop(4))
##########################################################################
        # show the floor of the elevator
        self.elecars[0].thread.obj_signal.connect(self.showFloor)
        self.elecars[1].thread.obj_signal.connect(self.showFloor)
        self.elecars[2].thread.obj_signal.connect(self.showFloor)
        self.elecars[3].thread.obj_signal.connect(self.showFloor)
        self.elecars[4].thread.obj_signal.connect(self.showFloor)
        self.elecars[5].thread.obj_signal.connect(self.showFloor)
        self.elecars[6].thread.obj_signal.connect(self.showFloor)

    def _getSrcDes(self):
        self.src.append(self.ui.src_floor_box.value())
        self.des.append(self.ui.des_floor_box.value())

    def _setPassText(self, record, src, info):
        self.base_passager_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{info_kind}</td>   </tr>'.format(
            rec=record, src=src, info_kind=info)
        self.pass_info = '<table><tr>    <th>Record</th> <th>Floor</th> <th>Info</th>    </tr>{show_info}</table>'.format(
            show_info=self.base_passager_info)

    def _setSchText(self, record, src, des, route_info):
        '''
        two condition are considered: with or without elevator exchanged
        '''

        self.base_sch_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{des}</td>  <td><b>{r1}</b>(<font color="#009933">{r2}</font>)——><b>{r3}</b>(<font color="#009933">{r4}</font>)</td>    </tr>'.format(rec=record, src=src, des=des, r1=route_info[0], r2=route_info[1], r3=route_info[2], r4=route_info[3])
        self.sch_info = '<table><tr><th>Record</th>   <th>src</th>    <th>des</th>    <th>Route</th></tr>{show_info}</table>'.format(
            show_info=self.base_sch_info)

    def _chooseSchStrategy(self):
        if len(self.des) == 0:
            self.route = one_command(self.src[-1], self.des[-1])
        else:
            self.route = commands(self.src[-1], self.des[-1])

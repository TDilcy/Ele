# -*- coding: utf-8 -*-
import random

from PyQt4.QtCore import pyqtSignal, QObject, QThread

from model.RedefineUi import RedefineUi
from model.schedule import Schedule


class MainWindow(RedefineUi):
    # schedule_res_sig = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        # the demo of the schedule
        # the init_variables
        self.base_passager_info = ''
        self.pass_info = ''
        self.base_sch_info = ''
        self.sch_info = ''
        self.pass_count = 0
        self.sche_count = 0
        self.scheduler = Schedule(self.elecars)
        self.schedule_thread = QThread()
        # ##################### what need to be done here ################################################################################
        # 1. once the confirm is pressed, the src and des should be fetched and the corresponding infomation should be showed in the board
        # 2. The exchange infomation should be kept
        # ################################################################################################################################
        # 0. Shuffle the ele status to simulating the status that all eles have been working for a while
        self.ui.shuffle_button.clicked.connect(self.shuffle)
        # 1. Reset all thing to be the initial status
        self.ui.clear_button.clicked.connect(self.clear)
        # 2. The LEDs show the floor information, and update the ele_status
        for ele in self.elecars:
            ele.obj_signal.connect(self.showFloor)
            ele.obj_signal.connect(self.update_ele_status)
        # 3. Once confirm button is pressed, fetch the src and des, put it into schedule module to get the result,
        #    and emit it out so that to trigger updating eles' des_list. This should be done in the background thread, because the schedule result are not
        #    to be given inmediately, it contains the loop
        # self.ui.confirm_button.clicked.connect(self.clear_input)  # clear the text-broswer after inputing
        self.ui.confirm_button.clicked.connect(self.get_schedule_result)
        # 4. Show the passenger info, this should be shown as the confirm button is pressed
        self.ui.confirm_button.clicked.connect(self.show_passenger_info)
        # 5. Show the schedule info(exchange info are contained), the info should be displayed as soon as the schedule is calculate
        # self.schedule_res_sig.connect(self.show_schedule_info)
        # self.schedule_res_sig.connect(self.show_schedule_info)
        # self.scheduler.result_sig.connect(self.show_schedule_info)
        # 6. Updating eles' des_list as the schedule result come out
        # self.schedule_res_sig.connect(self.update_ele_des)
        # self.scheduler.result_sig.connect(self.update_ele_des)

    def get_schedule_result(self):
        '''
        fetch the src, des, and use schedule module to calculate the route, then emit the result when calculating is done
        '''
        print('start getting result')
        src = int(self.ui.src_floor_box.toPlainText())
        des = int(self.ui.des_floor_box.toPlainText())
        print('src is {} des is {}'.format(src, des))
        worker = ScheduleWorker(self.scheduler)
        worker.moveToThread(self.schedule_thread)
        self.schedule_thread.start()
        # schedule_thread = QThread()
        self.schedule_thread.started.connect(lambda: print('the schedule thread starts'))
        self.schedule_thread.finished.connect(lambda: print('the schedule thread done'))
        self.schedule_thread.started.connect(lambda: worker.run_schedule(src, des))
        worker.result_sig.connect(self.show_schedule_info)
        worker.result_sig.connect(self.update_ele_des)

    def show_passenger_info(self):
        self.pass_count += 1
        src = int(self.ui.src_floor_box.toPlainText())
        self._setPassText(self.pass_count, src, '乘客呼梯')

    def show_schedule_info(self, route):
        # if len(route)==3: then it is [src, ele_picked, des]
        # if len(route)==6: then it is [notice, src, cur_ele, temp_flr, chg_ele, des]
        self.sche_count += 1
        self._setSchText(self.sche_count, route)
        self._showChgText(route)

    def update_ele_des(self, route):
        '''
        update the ele des_list and the exg_list of chosen ele
        :param route:
        :return:
        '''
        print('updating ele status')
        if len(route) == 3:
            ele = [ele for ele in self.elecars if ele.ele_name == route[1]][0]
            ele.des_list.append(route[-1])
            ele.update_des_list()
            print('the ele_list of {} is updated to {}'.format(ele.ele_name, ele.des_list))
        elif len(route) == 6:
            ele1 = [ele for ele in self.elecars if ele.ele_name == route[2]][0]
            ele2 = [ele for ele in self.elecars if ele.ele_name == route[-2]][0]
            print('des list of {} before are {}'.format(ele1.ele_name, ele1.des_list))
            print('des list of {} before are {}'.format(ele2.ele_name, ele2.des_list))
            ele1.des_list.append(route[3])
            ele1.des_list.append(route[1])
            ele1.exg_ele_list.append(route[-2])
            ele1.exg_ele_list.append('N')
            # ele1.update_des_list()

            ele2.des_list.append(route[5])
            ele2.des_list.append(route[3])
            ele2.exg_ele_list.append(route[2])
            ele2.exg_ele_list.append('N')
            # ele2.update_des_list()
            print('the des_list of {} is updated to {}, exg_list is {}'.format(ele1.ele_name, ele1.des_list,
                                                                               ele1.exg_ele_list))
            print('the des_list of {} is updated to {}, exg_list is {}'.format(ele2.ele_name, ele2.des_list,
                                                                               ele2.exg_ele_list))

    def _setPassText(self, order, src, info):
        self.base_passager_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{info_kind}</td>   </tr>'.format(
            rec=order, src=src, info_kind=info)
        # self.pass_info = '<table><tr>    <th>Record</th> <th>Floor</th> <th>Info</th>    </tr>{show_info}</table>'.format(
        #     show_info=self.base_passager_info)
        self.pass_info = '<table><tr>    <th>记录</th> <th>楼层</th> <th>信息</th>    </tr>{show_info}</table>'.format(
            show_info=self.base_passager_info)
        self.ui.pass_info_broswer.setHtml(self.pass_info)

    def _setSchText(self, order, route):
        '''
        two condition are considered: with or without elevator exchanged
        '''
        if len(route) == 3:
            self.base_sch_info += '<tr>    <td>{ord}</td>  <td>{src}</td>  <td>{des}</td>  <td><b>{des}</b>(<font color="#FFFFFF">{ele}</font>)</td>    </tr>'.format(
                ord=order, src=route[0], ele=route[1], des=route[-1])
        elif len(route) == 6:
            self.base_sch_info += '<tr>    <td>{ord}</td>  <td>{src}</td>  <td>{des}</td>  <td><b>{chg_flr}</b>(<font color="#FFFFFF">{cur_ele}</font>)——><b>{des}</b>(<font color="#FFFFFF">{chg_ele}</font>)</td>    </tr>'.format(
                ord=order, src=route[1], des=route[-1], chg_flr=route[3], cur_ele=route[2], chg_ele=route[4])
        # self.sch_info = '<table><tr><th>Record</th>   <th>src</th>    <th>des</th>    <th>Route</th></tr>{show_info}</table>'.format(
        #     show_info=self.base_sch_info)
        self.sch_info = '<table><tr><th>记录</th>   <th>当前楼层</th>    <th>目的楼层</th>    <th>线路</th></tr>{show_info}</table>'.format(
            show_info=self.base_sch_info)
        self.ui.sch_info_broswer.setHtml(self.sch_info)

    def _showChgText(self, route):
        if len(route) == 6:
            self.ui.chg_info_broswer.setHtml('<font color="#FFFFFF">{chg_info}</font>'.format(chg_info=route[0]))

    def update_ele_status(self, ele):
        self.all_ele_status[ele.ele_name] = ele.getLocation

    def clear(self):
        '''
        clear  all the infomation showed in the boxes
        '''
        # self.des = []
        # self.src = []
        # self.route = []
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


class ScheduleWorker(QObject):
    result_sig = pyqtSignal(list)

    def __init__(self, scheduler):
        super(ScheduleWorker, self).__init__()
        self.scheduler = scheduler

    def run_schedule(self, src, des):
        schedule_result = self.scheduler.commands(src, des)
        print('the result calculated is \n{}'.format(schedule_result))
        self.result_sig.emit(schedule_result)

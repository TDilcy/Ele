# -*- coding: utf-8 -*-
import copy
import random
import re
import time

from PyQt4.QtCore import QObject

from model.RedefineUi import RedefineUi
from model.schedule import Schedule


class MainWindow(RedefineUi):
    # schedule_res_sig = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        # the demo of the schedule
        # the init_variables

        # print('the main thread in MainWindow is\n{}'.format(QThread.currentThread()))
        self.pass_info = ''
        self.pass_info_dict = {}
        self.pass_count = 0

        self.sch_info = ''
        self.sche_info_dict = {}
        self.sche_count = 0

        self.base_request_info = ''
        self.request_count = 0
        self.request_list = []
        self.schedulers = [ScheduleWorker(self.elecars) for i in range(4)]
        # self.scheduler = Schedule(self.elecars)
        # self.schedule_threads = [QThread() for i in range(4)]
        # print('all thread are \n{}\n{}\n{}\n{}'.format(self.schedule_threads[0], self.schedule_threads[1], self.schedule_threads[2], self.schedule_threads[3]))
        # ##################### what need to be done here ################################################################################
        # 1. once the confirm is pressed, the src and des should be fetched and the corresponding infomation should be showed in the board
        # 2. The exchange information should be kept
        # ################################################################################################################################
        # 0. Shuffle the ele status to simulating the status that all eles have been working for a while
        self.ui.shuffle_button.clicked.connect(self.shuffle)
        # 1. Reset all thing to be the initial status
        self.ui.clear_button.clicked.connect(self.clear)
        # 2. The LEDs show the floor information, the amount of people is shown in the elevator, and update the ele_status,
        #    the input_browser show the input information
        for ele in self.elecars:
            ele.obj_signal.connect(self.showFloor)
            ele.amount_sig.connect(ele.show_amount)
            ele.obj_signal.connect(self.update_ele_status)
            ele.amount_sig.connect(ele.full_alert)
            ele.execute_id_sig.connect(self.change_info_color)
        self.ui.add_button.clicked.connect(self.display_input)
        # 5. Once confirm button is pressed, fetch the src and des, put it into schedule module to get the result,
        #    and emit it out so that to trigger updating eles' des_exg_dict. This should be done in the background thread, because the schedule result are not
        #    to be given inmediately, it contains the loop
        # self.ui.confirm_button.clicked.connect(self.clear_input)  # clear the text-browser after inputing
        self.ui.confirm_button.clicked.connect(self.get_schedule_results)
        # 6. Show the passenger info, this should be shown as the confirm button is pressed
        self.ui.confirm_button.clicked.connect(self.show_passenger_info)
        # 7. Show the schedule info(exchange info are contained), the info should be displayed as soon as the schedule is calculate
        # self.schedule_res_sig.connect(self.show_schedule_info)
        # self.schedule_res_sig.connect(self.show_schedule_info)
        # self.scheduler.result_sig.connect(self.show_schedule_info)
        # 8. Updating eles' des_exg_dict as the schedule result come out
        # self.schedule_res_sig.connect(self.update_ele_des)
        # self.scheduler.result_sig.connect(self.update_ele_des)

    def get_schedule_results(self):
        request_bro_content = self.ui.request_broswer.toPlainText()
        if len(request_bro_content) == 0:
            # if only one des, then no need to add to the request_browser
            src = int(self.ui.src_floor_box.toPlainText())
            des = int(self.ui.des_floor_box.toPlainText())
            amount = int(self.ui.amount_box.toPlainText()) if len(self.ui.amount_box.toPlainText()) != 0 else 1
            route_id = self.hash_route_id(src, des, amount)
            self.request_list.append((src, des, amount, route_id))
        temp_request_list = copy.deepcopy(self.request_list)
        # reset for next calling
        # self.request_list = []
        self.ui.request_broswer.clear()
        self.base_request_info = ''

        for request in temp_request_list:
            src = request[0]
            des = request[1]
            amount = request[2]
            route_id = request[3]
            # print('request is {}'.format(request))
            self.get_single_result(src, des, amount, route_id)

    def get_single_result(self, src, des, amount, route_id):
        '''
        fetch the src, des, and use schedule module to calculate the route, then emit the result when calculating is done
        '''
        # print('start getting result')
        # def update_ele_in_func(route):
        #     self.update_ele_des(route, amount)
        # idle_thread_idx = [idx for idx, thread in enumerate(self.schedule_threads) if not thread.isRunning()]

        # print('the idle threads are {}'.format(idle_thread_idx))
        # idx = random.choice(idle_thread_idx)
        # # while idx == 0:
        # #     idx = random.choice(idle_thread_idx)
        # worker = ScheduleWorker(self.scheduler)
        # worker.moveToThread(self.schedule_threads[idx])
        # print('thread[{}] is {}'.format(idx, self.schedule_threads[idx]))
        # # self.schedule_threads[idx] = QThread()
        # self.schedule_threads[idx].started.connect(lambda: print('the schedule thread starts'))
        # self.schedule_threads[idx].finished.connect(lambda: print('the schedule thread done'))

        # self.schedule_threads[idx].started.connect(lambda: worker.run_schedule(src, des))
        # self.schedule_threads[idx].start()
        # # print('the worker is {}'.format(worker))
        # worker.result_sig.connect(self.show_schedule_info)
        # worker.result_sig.connect(update_ele_in_func)
        # worker.result_sig.connect(self.schedule_threads[idx].exit)

        # #===========================another way======================
        print('start getting result')

        def update_ele_in_func(route):
            self.update_ele_des(route, route_id, amount)

        def show_schedule_info_in_func(route):
            self.show_schedule_info(route, route_id)
        idle_thread_idx = [idx for idx, thread in enumerate(self.schedule_threads) if not thread.isRunning()]

        # print('the idle threads are {}'.format(idle_thread_idx))
        idx = random.choice(idle_thread_idx)
        # while idx == 0:
        #     idx = random.choice(idle_thread_idx)
        scheduler = self.schedulers[random.choice([0, 1, 2, 3])]
        scheduler.worker.moveToThread(self.schedule_threads[idx])
        # print('thread[{}] is {}'.format(idx, self.schedule_threads[idx]))
        # self.schedule_threads[idx] = QThread()
        self.schedule_threads[idx].started.connect(lambda: print('the schedule thread starts'))
        self.schedule_threads[idx].finished.connect(lambda: print('the schedule thread done'))

        self.schedule_threads[idx].started.connect(lambda: scheduler.worker.run_schedule(src, des))
        self.schedule_threads[idx].start()
        # print('the worker is {}'.format(worker))
        scheduler.worker.result_sig.connect(show_schedule_info_in_func)
        scheduler.worker.result_sig.connect(update_ele_in_func)
        scheduler.worker.result_sig.connect(self.schedule_threads[idx].exit)

    def show_passenger_info(self):
        for request in self.request_list:
            self.pass_count += 1
            src = request[0]
            route_id = request[3]
            self._setPassinfo_dict(self.pass_count, src, route_id, '乘客呼梯')
        # print(self.pass_info)
        self._setPassText()
        self.ui.pass_info_broswer.setHtml(self.pass_info)
        self.request_list = []  # reset the request info here to ensure pass info shown properly

    def _setPassinfo_dict(self, order, src, route_id, info):
        self.pass_info_dict[route_id] = [order,
                                         '<tr>    <td><font color={color}>{rec}</font></td>  <td><font color={color}>{src}</font></td>  <td><font color={color}>{info_kind}</font></td>   </tr>'.format(
                                             rec=order, src=src, info_kind=info, color="#000000")]

    def _setPassText(self):
        sorted_route_info = sorted(self.pass_info_dict.values(), key=lambda x: x[0])
        base_pass_info = ''
        for route_info in sorted_route_info:
            base_pass_info += route_info[1]
        self.pass_info = '<table><tr>    <th>记录</th> <th>楼层</th> <th>信息</th>    </tr>{show_info}</table>'.format(
            show_info=base_pass_info)

    def show_schedule_info(self, route, route_id):
        # if len(route)==3: then it is [src, ele_picked, des]
        # if len(route)==6: then it is [notice, src, cur_ele, temp_flr, chg_ele, des]
        self.sche_count += 1
        self._setSchText_dict(self.sche_count, route, route_id)
        self._setScheText()
        self.ui.sch_info_broswer.setHtml(self.sche_info)
        self._showChgText(route)

    def _setSchText_dict(self, order, route, route_id):
        '''
        two condition are considered: with or without elevator exchanged
        '''
        if len(route) == 3:
            self.sche_info_dict[route_id] = [order,
                                             '<tr>    <td><font color={color}>{ord}</font></td>  <td><font color={color}>{src}</font></td>  <td><font color={color}><b>{des}</b>({ele})</font></td>   </tr>'.format(
                                                 ord=order, src=route[0], des=route[-1], ele=route[1], color='#000000')]
        elif len(route) == 6:
            self.sche_info_dict[route_id] = [order,
                                             '<tr>    <td><font color={color}>{ord}</font></td>  <td><font color={color}>{src}</font></td>  <td><font color={color}>{des}</font></td>  <td><font color={color}><b>{chg_flr}</b>({cur_ele})——><b>{des}</b>({chg_ele})</font></td>    </tr>'.format(
                                                 ord=order, src=route[1], des=route[-1], chg_flr=route[3],
                                                 cur_ele=route[2], chg_ele=route[4], color='#000000')]

    def _setScheText(self):
        sorted_route_info = sorted(self.sche_info_dict.values(), key=lambda x: x[0])
        base_sche_info = ''
        for route_info in sorted_route_info:
            base_sche_info += route_info[1]
        self.sche_info = '<table><tr>    <th>记录</th> <th>楼层</th> <th>信息</th>    </tr>{show_info}</table>'.format(
            show_info=base_sche_info)

    def change_info_color(self, route_id, status, exc='#FF9900',
                          not_exc='#000000'):  # # another pair('#FF0033', '#333333')
        '''
        find the pass_info which owns the specific route_id, then change the font color
        :param route_id:
        :param status:
        :return:
        '''
        print('changing font color, route_id is {} status is {}'.format(route_id, status))
        if status == 'started':
            self.pass_info_dict[route_id][1] = re.sub('#.{6}', exc, self.pass_info_dict[route_id][1])
            self.sche_info_dict[route_id][1] = re.sub('#.{6}', exc, self.sche_info_dict[route_id][1])
        if status == 'finished':
            self.pass_info_dict[route_id][1] = re.sub('#.{6}', not_exc, self.pass_info_dict[route_id][1])
            self.sche_info_dict[route_id][1] = re.sub('#.{6}', not_exc, self.sche_info_dict[route_id][1])
        self._setPassText()
        self.ui.pass_info_broswer.setHtml(self.pass_info)
        self._setScheText()
        self.ui.sch_info_broswer.setHtml(self.sche_info)

    def _showChgText(self, route):
        if len(route) == 6:
            self.ui.chg_info_broswer.setHtml('<font color="#FFFFFF">{chg_info}</font>'.format(chg_info=route[0]))

    def update_ele_status(self, ele):
        self.all_ele_status[ele.ele_name] = ele.getLocation()

    def display_input(self):
        self.request_count += 1
        src = int(self.ui.src_floor_box.toPlainText())
        des = int(self.ui.des_floor_box.toPlainText())
        amount = int(self.ui.amount_box.toPlainText())
        route_id = self.hash_route_id(src, des, amount)
        self.request_list.append((src, des, amount, route_id))

        self.base_request_info += '<tr>    <td>{rec}</td>  <td>{src}</td>  <td>{des}</td> <td>{amount}</td>  </tr>'.format(
            rec=self.request_count, src=src, des=des, amount=amount)
        request_info = '<table><tr>    <th>记录</th> <th>呼梯楼层</th> <th>目的楼层</th> <th>呼梯人数</th>   </tr>{show_info}</table>'.format(
            show_info=self.base_request_info)
        self.ui.request_broswer.setHtml(request_info)

    def update_ele_des(self, route, route_id, amount=1):
        '''
        update the ele des_exg_dict and the exg_list of chosen ele
        '''
        # print('updating ele status')
        if len(route) == 3:
            # route is like: [src, ele, des]
            # this condition contains the insert situation

            ele = [ele for ele in self.elecars if ele.ele_name == route[1]][0]
            self.assign_des(ele, des1=route[0], des2=route[2], exg_info=['N', 'N'], route_id=route_id,
                            route_finished=['S', 'E'])
            # print('the ele_list of {} is updated to \n{}\nfirst stat is {}'.format(ele.ele_name, ele.des_exg_dict, ele.is_first))
        elif len(route) == 6:
            print(route)
            # route is like: [notice, src, cur_ele, temp_flr, chg_ele, des]
            ele1 = [ele for ele in self.elecars if ele.ele_name == route[2]][0]
            # ele1's des list here is straight, yet ele2's is a turn back
            ele2 = [ele for ele in self.elecars if ele.ele_name == route[-2]][0]
            self.assign_des(ele1, des1=route[1], des2=route[3], exg_info=['N', route[4]], amount=amount,
                            route_id=route_id, route_finished=['S', 'N'])
            self.assign_des(ele2, des1=route[3], des2=route[5], exg_info=[route[2], 'N'], amount=amount,
                            route_id=route_id, route_finished=['N', 'E'])
            # print('the amount of people in {} before moving is {}'.format(ele1.ele_name, ele1.current_amount))
            # print('the amount of people in {} before moving is {}'.format(ele2.ele_name, ele2.current_amount))
            # print('the des_exg_dict of {} is updated to \n{},\nthe is_first_stat is {}'.format(ele1.ele_name, ele1.des_exg_dict, ele1.is_first))
            # print('the des_exg_dict of {} is updated to \n{},\nthe is_first_stat is {}'.format(ele2.ele_name, ele2.des_exg_dict, ele2.is_first))

    # #################################################################

    def assign_des(self, ele, des1, des2, exg_info, route_id, route_finished, amount=1):
        '''
        exg_info contains the exg_info of des1 and des2 in the form of [exg1, exg2]
        '''
        ele_cur_flr = ele.getLocation()
        if len(ele.des_exg_dict['up']) == 0 & len(ele.des_exg_dict['down']) == 0:
            # if first time, then we should confirm which set should be executed first
            if ele_cur_flr >= des1:  # the equal situation is included in this
                ele.is_first = 'down'
            elif ele_cur_flr < des1:
                ele.is_first = 'up'
        if ele_cur_flr >= des1:
            ele.des_exg_dict['down'].append([des1, exg_info[0], 'N', amount, route_id, route_finished[0]])
        elif ele_cur_flr < des1:
            ele.des_exg_dict['up'].append([des1, exg_info[0], 'N', amount, route_id, route_finished[0]])
        if des1 >= des2:
            ele.des_exg_dict['down'].append([des2, exg_info[1], 'Y', amount, route_id, route_finished[1]])
        elif des1 < des2:
            ele.des_exg_dict['up'].append([des2, exg_info[1], 'Y', amount, route_id, route_finished[1]])
        # set the des1_des2_diff value
        if (des1 - ele_cur_flr) * (des2 - des1) < 0:
            ele.des1_des2_diff = des1
        ele.update_des_exg_dict()

    @staticmethod
    def hash_route_id(src, des, amount):
        route_id = (''.join(str(time.time()).split('.')) + str(src) + str(des) + str(amount))[-12:]
        print(src, des, amount, route_id)
        return route_id

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
    # result_sig = pyqtSignal(list)

    # def __init__(self, scheduler):
    #     super(ScheduleWorker, self).__init__()
    #     self.scheduler = scheduler
    def __init__(self, elecars):
        super(ScheduleWorker, self).__init__()
        self.elecars = elecars
        self.worker = Schedule(self.elecars)

        # def run_schedule(self, src, des):
        #     print('seeking result..........from {} to {}'.format(src, des))
        #     schedule_result = self.scheduler.commands(src, des)
        #     # print('the result calculated is \n{}'.format(schedule_result))
        #     self.result_sig.emit(schedule_result)

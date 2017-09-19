# coding: utf-8
# Date: 2017-05-10
# Author: cyL
import random
import time

from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal


class Schedule(QObject):
    '''A class that implements two schedule strategies'''
    # the route should be stored in a dict rather than list..., this is a big mistake
    # global constant:
    result_sig = pyqtSignal(list)
    finished_sig = pyqtSignal()

    def __init__(self, eles):
        super(Schedule, self).__init__()
        self.eles = eles
        self.src = 0
        self.des = 0
        self.amount = 0
        self.route_id = ''
        self.test_src = 0
        self.isRunning = False
        # should the AVAI_MATRIX be changed
        # self.AVAI_MATRIX = [[('A', 'B1', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1')],
        #                     [('A', 'C1', 'D1'), ('A', 'B2', 'C1', 'D1'), ('A', 'B2', 'D1'), ('A', 'B2', 'D1')],
        #                     [('A', 'B2', 'D1'), ('A', 'B2', 'D1'), ('A', 'B2', 'C2', 'D1'), ('A', 'B2', 'C2')],
        #                     [('A', 'B2', 'C2', 'D2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2', 'D2')]]

        self.AVAI_MATRIX = [['A', 'B1', 'C1', 'D1'],
                            ['A', 'B2', 'C1', 'D1'],
                            ['A', 'B2', 'C2', 'D1'],
                            ['A', 'B2', 'C2', 'D2']]

        self.ELE_DICT = {'A': 0, 'B1': 1, 'C1': 2,
                         'D1': 3, 'B2': 4, 'C2': 5, 'D2': 6}

    def set_src(self, src):
        self.src = src
        # print('the src of this worker is set as {}'.format(self.src))

    def set_des(self, des):
        self.des = des

    def set_amount(self, amount):
        self.amount = amount

    def set_route_id(self, route_id):
        self.route_id = route_id

    def set_test_src(self, test_src):
        self.test_src = test_src

    def map_index(self, x):
        if 1 <= x < 16:
            return 0
        elif 16 <= x < 31:
            return 1
        elif 31 <= x < 46:
            return 2
        elif 46 <= x < 61:
            return 3
        else:
            print('input floor number out of range')
            raise IndexError

    def _select_avai_ele(self, src):
        '''
        1. map the src and des to the matrix index.
        2. select available ele_cars from a matrix using the src and des as index, return ele_id set
        '''
        # src, des = self.map_index(src), self.map_index(des)
        src = self.map_index(src)
        # avai_eles = self.AVAI_MATRIX[src][des]
        avai_eles = self.AVAI_MATRIX[src]
        return avai_eles

    def _nearest_ele(self, ele_cur_floor, src):
        '''
        ele_cur_floor: a dict that contains each ele's current floor
        obtain the current floor of the ele_cur_floor, and then calculate the distance between passager and each ele_car,
        and picked the nearest one. return picked ele_id, if there are more than one being picked, then choose one randomly
        '''
        min_distance = min([abs(i - src) for i in ele_cur_floor.values()])
        picked_eles = [i for i in ele_cur_floor.keys() if abs(ele_cur_floor[i] - src) == min_distance]
        # print('picked_eles are {}'.format(picked_eles))
        random.seed(111)
        return random.choice(picked_eles)

    def _notice(self, chg_ele, temp_flr, des):
        # message = "The final destination of current elecar is {}, the people who go to {} should change to elecar {} at {}".format(temp_flr, des, chg_ele, temp_flr)
        if isinstance(chg_ele, list):
            if len(chg_ele) != 0:
                message = "电梯到达楼层为{}层, 当前无可用换乘轿厢，将在{}层之前逐层检查轿厢是否可用".format(temp_flr, temp_flr)
            else:
                message = "电梯到达楼层为{}层, 未寻找到可用换乘轿厢".format(temp_flr)
        else:
            message = "电梯到达楼层为{}层, 去往{}层的乘客请在{}层换乘{}".format(temp_flr, des, temp_flr, chg_ele)
        return message

    def _get_y_status(self, picked_name):
        '''
        get the y_position of picked eles, return a dict that contains the name of ele and its corresponding y_location
        '''
        picked_ele = [self.eles[self.ELE_DICT[i]] for i in picked_name]
        return {i.ele_name: i.getLocation() for i in picked_ele}

    # ###################### function used in commands ##########
    def adjust_set(self, cand_set, src, des):
        '''
        actually here only need des, src would be filtered in the previous step, and it is guaranteed to be eligible.
        '''
        for ele in cand_set:
            ele_car = self.eles[self.ELE_DICT[ele]]
            # print('the des_diff of {} is {}'.format(ele_car.ele_name, ele_car.des1_des2_diff))
            if (des - src) > 0:
                if (ele_car.des1_des2_diff != -1) & (ele_car.des1_des2_diff < max(src, des)):
                    cand_set.remove(ele)
            elif (des - src) < 0:
                if (ele_car.des1_des2_diff != -1) & (ele_car.des1_des2_diff > min(src, des)):
                    cand_set.remove(ele)
        return cand_set

    def _disc_status(self, ele_names):
        '''
        divide the available eles into different sets
        :param ele_names:
        :return: up_set, down_set, static_set, list containing the name of the eles
        '''
        eles = [self.eles[self.ELE_DICT[i]] for i in ele_names]
        ele_sets = {direc: [ele.ele_name for ele in eles if ele.direction == direc] for direc in ['up', 'down', 'stop']}
        return ele_sets['up'], ele_sets['down'], ele_sets['stop']

    def _cal_distance(self, name_set, floor):
        '''
        Calculate the distance between the floor and the chosen eles, which is assigned to Dcc.
        Calculate the distance between the nearest target and the current floor of each eles, which is taken as Dcd
        :param set:
        :param floor:
        :return: Dcd, Dcd, dict type
        '''
        # print('calculating Dcc, Dcd among {}'.format(name_set))
        eles = {i: self.eles[self.ELE_DICT[i]] for i in name_set}
        Dcc = {i: eles[i].getLocation() - floor for i in eles.keys()}
        Dcd = {i: eles[i].getLocation() - eles[i].des_exg_dict[eles[i].running_set][-1][0] for i in eles.keys()}
        return Dcc, Dcd

    def _is_full(self, ele_name, floor):
        '''
        judge if the ele would be full when arriving at specific floor, the index may be the number of people or the total weight
        :param ele:
        :param floor:
        :return: Boolean
        '''
        ele = [e for e in self.eles if e.ele_name == ele_name][0]
        try:
            increment = sum([des_floor[3] for des_floor in ele.des_exg_dict[ele.running_set] if des_floor[0] < floor])
        except KeyError:
            # if ele not running, then it neither 'up' nor 'down'
            increment = 0
        total_amount = ele.get_current_amount() + increment
        if total_amount >= ele.max_amount:
            return True
        else:
            return False

    def _choose_from_static(self, static_set, src):
        '''
        Choose ele from static set
        :param static_set:
        :param src:
        :return:
        '''
        # print('choosing from static set :{}'.format(static_set))
        ele_status = self._get_y_status(static_set)
        ele_picked = self._nearest_ele({key: ele_status[key] for key in static_set}, src)
        return ele_picked

    def check_one_way(self, one_way_route):
        '''
        check if the route is valid, the route is straight, with no turn-back
        :param one_way_route: [src, ele, des]
        :return:
        '''
        ele = [e for e in self.eles if e.ele_name == one_way_route[1]][0]
        direction = 'up' if one_way_route[-1] - one_way_route[0] > 0 else 'down'
        ele_des_range = [i[0] for i in ele.des_exg_dict[direction]]
        if len(ele_des_range) == 0:
            # this indicates that there is no previous route generated
            print('return due to 0 length，current route is {}, no previous route'.format(one_way_route))
            return 0
        route_min = min([one_way_route[0], one_way_route[-1]])
        route_max = max([one_way_route[0], one_way_route[-1]])
        ele_min = min(ele_des_range)
        ele_max = max(ele_des_range)
        if direction == 'up':
            if ele.running_set == 'up':
                if (route_max <= ele_max) & (route_min >= ele.getLocation() + 1):
                    print('return 0, current route is {}'.format(one_way_route))
                    return 0
                else:
                    print('return 1, current route is {}'.format(one_way_route))
                    return 1
            else:
                if (route_max <= ele_max) & (route_min >= ele_min):
                    print('return 0, current route is {}'.format(one_way_route))
                    return 0
                else:
                    print('return 1, current route is {}'.format(one_way_route))
                    return 1
        else:
            if ele.running_set == 'down':
                if (route_max <= ele.getLocation() - 1) & (route_min >= ele_min):
                    print('return 0, current route is {}'.format(one_way_route))
                    return 0
                else:
                    print('return 1, current route is {}'.format(one_way_route))
                    return 1
            else:
                if (route_max <= ele_max) & (route_min >= ele_min):
                    print('return 0, current route is {}'.format(one_way_route))
                    return 0
                else:
                    print('return 1, current route is {}'.format(one_way_route))
                    return 1

    def check_validity(self, result):
        # check if the result obtained is valid
        if len(result) == 3:
            # [src, ele, des]
            print('len(route) is 3, and the ele is {}'.format(result[1]))
            ele = [e for e in self.eles if e.ele_name == result[1]][0]
            route_1 = [ele.getLocation(), result[1], result[0]]
            route_2 = [result[0], result[1], result[2]]
            if self.check_one_way(route_1) + self.check_one_way(route_2) > 0:
                return 1
            else:
                return 0
        else:
            print('the result in validity is {}'.format(result))
            # [notice, src, cur_ele, temp_flr, chg_ele, des]
            ele1 = [e for e in self.eles if e.ele_name == result[2]][0]
            if isinstance(result[4], list):
                # if result[4] has more than one candidate, then only check the first half
                first_way_1 = [ele1.getLocation(), result[2], result[1]]
                first_way_2 = [result[1], result[2], result[3]]
                if self.check_one_way(first_way_1) + self.check_one_way(first_way_2) > 0:
                    print('result[4] is a list, and here returns 1')
                    return 1
                else:
                    if len(result[4]) == 0:
                        print('result[4] is a list, and here returns 0')
                        # if first half is ok, and the candidate set is empty, then the route_result should be sent,
                        # but we need to return another number other than 0 to distinguish from normal situation
                        return 5
                    else:
                        return 0
            else:
                ele2 = [e for e in self.eles if e.ele_name == result[4]][0]
                first_way_1 = [ele1.getLocation(), result[2], result[1]]
                first_way_2 = [result[1], result[2], result[3]]
                second_way_1 = [ele2.getLocation(), result[4], result[3]]
                second_way_2 = [result[3], result[4], result[5]]
            # if first way is not valid
            if self.check_one_way(first_way_1) + self.check_one_way(first_way_2) > 0:
                return 1
            else:
                # if second way is not valid
                if self.check_one_way(second_way_1) + self.check_one_way(second_way_2) > 0:
                    return 2
                # if both is valid
                else:
                    return 0

    def _get_chg(self, cur_ele, src, des, candidate, temp_flr, direction=None, solo=False, exclude='None'):
        '''
        recurrently find the available elecar  from candidates, if failed at the destination, use a different flag to indicate the failing info
        :param cur_ele:
        :param candidate:
        :param temp_flr:
        :return:
        '''
        if direction is not None:
            # print('exchange direction is {}'.format(direction))
            # ====debug code===========
            # print('candidate is {}'.format(candidate))
            ori_candidate = candidate
            candidate = self.adjust_set(candidate, src, des)
            if exclude != 'None':
                candidate.remove(exclude)
            candidate_eles = [self.eles[self.ELE_DICT[i]] for i in candidate]

            # print('candidate_eles are {}'.format(candidate))
            available_eles = []
            for ele in candidate_eles:
                if ele.is_first != "None":
                    if (ele.is_first == direction) & (not self._is_full(ele.ele_name, temp_flr)):
                        available_eles.append(ele)
                else:
                    if (ele.direction == 'stop') | (
                        (ele.direction == direction) & (not self._is_full(ele.ele_name, temp_flr))):
                        available_eles.append(ele)
            # available_eles = [ele for ele in candidate_eles if ((ele.direction == 'stop') | ((ele.direction == direction) & (not self._is_full(ele.ele_name, temp_flr))))]
            # print('available eles for exg are {}'.format([ele.ele_name for ele in available_eles]))
            if len(available_eles) == 0:
                # print('there is no available eles for now')
                if not solo:
                    # print('the solo status is {}'.format(solo))
                    return [cur_ele, temp_flr, ori_candidate, des]
                else:
                    if self.eles[self.ELE_DICT[cur_ele]].getLocation() == temp_flr:
                        # print('waiting 3s due to the y_loc == temp_flr')
                        time.sleep(5)
                    # while self.eles[self.ELE_DICT[cur_ele]].getLocation() == temp_flr:
                    #         time.sleep(0.2)
                    while self.eles[self.ELE_DICT[cur_ele]].getLocation() != temp_flr:
                        time.sleep(0.5)
                        print('inside the loop of seeking exg ele...')
                        # print('the status of all the ele is {}'.format([e.getLocation() for e in self.eles]))
                        return self._get_chg(cur_ele, src, des, ori_candidate, temp_flr, direction=direction, solo=True)
                    # if no result, then return a empty list
                    return [cur_ele, temp_flr, [], des]
            else:
                temp_status = self._get_y_status([ele.ele_name for ele in available_eles])
                chg_ele = self._nearest_ele(temp_status, temp_flr)
                # print('exchange ele is {}'.format(chg_ele))
                return [cur_ele, temp_flr, chg_ele, des]

        else:
            temp_status = self._get_y_status(candidate)
            chg_ele = self._nearest_ele(temp_status, temp_flr)
            return [cur_ele, temp_flr, chg_ele, des]

    @staticmethod
    def get_candidate(src, des, ele_picked):
        result = []
        if src == 0:
            if des == 1:
                if ele_picked == 'B1':
                    result.extend([['A', 'C1', 'D1'], 15])
            elif des == 2:
                if ele_picked == 'C1':
                    result.extend([['A', 'B2', 'D1'], 30])
                elif ele_picked == 'B1':
                    result.extend([['A', 'D1'], 15])
            elif des == 3:
                if ele_picked == 'B1':
                    result.extend([['A'], 15])
                elif ele_picked == 'C1':
                    result.extend([['A', 'B2'], 30])
                elif ele_picked == 'D1':
                    result.extend([['A', 'B2', 'C2'], 45])

        elif src == 1:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend([['A', 'C1', 'D1'], 16])
            elif des == 2:
                if ele_picked == 'C1':
                    result.extend([['A', 'B2', 'D1'], 30])
            elif des == 3:
                if ele_picked == 'C1':
                    result.extend([['A'], 30])
                elif ele_picked == 'D1':
                    result.extend([['A', 'B2', 'C2'], 45])

        elif src == 2:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend([['A', 'C1', 'D1'], 16])
                elif ele_picked == 'C2':
                    result.extend([['A', 'D1'], 31])
            elif des == 1:
                if ele_picked == 'C2':
                    result.extend([['A', 'B2', 'D1'], 31])
            elif des == 3:
                if ele_picked == 'D1':
                    result.extend([['A', 'B2', 'C2'], 45])

        elif src == 3:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend([['A', 'C1', 'D1'], 16])
                elif ele_picked == 'C2':
                    result.extend([['A', 'D1'], 31])
                elif ele_picked == 'D2':
                    result.extend([['A'], 46])
            elif des == 1:
                if ele_picked == 'C2':
                    result.extend([['A', 'B2', 'D1'], 31])
                elif ele_picked == 'D2':
                    result.extend([['A', 'B2'], 46])
            elif des == 2:
                if ele_picked == 'D2':
                    result.extend([['A', 'B2', 'C2'], 46])
        return result

    def _step_one(self, src, des, exclude='None'):
        '''
        got the ele in first step
        '''
        # select available ele_cars. return ele_id list
        ava_eles = self._select_avai_ele(src)
        if exclude != 'None':
            ava_eles.remove(exclude)
        # divide the eles into up, down, static set
        up_set, down_set, static_set = self._disc_status(ava_eles)

        # ===============debug code==========
        # print('up_set is {}, down_set is {}, static_set is {}'.format(up_set, down_set, static_set))
        # get ele status
        if src < des:  # which means that the passenger expects to go upstairs
            # print('the up_set before is {}'.format(up_set))
            up_set = self.adjust_set(up_set, src, des)
            # print('the up_set is {}'.format(up_set))

            # print('the static_set before is {}'.format(static_set))
            static_set = self.adjust_set(static_set, src, des)
            # print('the static_set is {}'.format(static_set))
            if len(up_set) == 0:
                # whether should consider that the ele is full when it arrive at the floor of the first caller, because other people may also call during the process
                # for instance: A: 1 ————> 25, another is A: 3————>22, and the latter may make the ele be fully occupied
                # for now, we think that the first command would gain higher
                # priority, and won't be broken
                if len(static_set) != 0:
                    ele_picked = self._choose_from_static(static_set, src)
                    print('the ele returned is {}'.format(ele_picked))
                    return ele_picked
                else:
                    print('up_set and static set are both empty, restarting...')
                    # time.sleep(1)
                    # return self.commands(src, des)
                    return self._step_one(src, des)
            else:
                # print('the up_set is {}'.format(up_set))
                Dcc, Dcd = self._cal_distance(up_set, src)
                Dcc_Dcd = {key: abs(Dcc[key]) - abs(Dcd[key]) for key in Dcc.keys() if Dcc[key] <= 0}
        elif src > des:
            # print('the down_set bofore is {}'.format(down_set))
            down_set = self.adjust_set(down_set, src, des)
            # print('the down_set after is {}'.format(down_set))

            # print('the static_set before is {}'.format(static_set))
            static_set = self.adjust_set(static_set, src, des)
            # print('the static_set is {}'.format(static_set))
            if len(down_set) == 0:
                if len(static_set) != 0:
                    ele_picked = self._choose_from_static(static_set, src)
                    # print('the ele returned is {}'.format(ele_picked))
                    return ele_picked
                else:
                    print('down_set and static set are both empty, restarting...')
                    time.sleep(0.5)
                    # return self.commands(src, des)
                    return self._step_one(src, des)
            else:
                # print('the down_set is {}'.format(down_set))
                Dcc, Dcd = self._cal_distance(up_set, src)
                Dcc_Dcd = {key: abs(Dcc[key]) - abs(Dcd[key]) for key in Dcc.keys() if Dcc[key] >= 0}
        elif src == des:
            print('The destination is the current floor, no need for elevator!')
            return 'X'
        # get the min(Dcc_Dcd.values>0), or choose from (Dcc_Dcd.values>0) randomly

        # # if Dcc_Dcd is empty, then check static set
        print('Dcc_Dcd is {}'.format(Dcc_Dcd))
        if len(Dcc_Dcd) == 0:

            if len(static_set) != 0:
                print('Dcc_Dcd is empty, choosing from static set')
                ele_picked = self._choose_from_static(static_set, src)
                return ele_picked
            else:
                print('Dcc_Dcd and static set are both empty, restarting...')
                time.sleep(1)
                # return self.commands(src, des)
                return self._step_one(src, des)
        else:
            above_0 = [value for value in Dcc_Dcd.values() if value > 0]
            below_0 = [i for i in Dcc_Dcd.keys() if Dcc_Dcd[i] < 0]
            # ========================== debug code=============
            # print('Dcc is {}, Dcd is {}'.format(Dcc, Dcd))
            # print('Dcc_Dcd is {}'.format(Dcc_Dcd))
            # print('the ele set above 0 are {}'.format(above_0))
            # print('the ele set below 0 are {}'.format(below_0))
            # ======================================================
            if len(above_0) != 0:
                ele_picked = random.choice([i for i in Dcc_Dcd.keys() if Dcc_Dcd[i] == min(above_0)])
            else:
                ele_picked = random.choice([i for i in Dcc_Dcd.keys() if Dcc_Dcd[i] <= 0])
            print('ele picked is in step_one final part is {}'.format(ele_picked))
            if not self._is_full(ele_picked, src):
                return ele_picked
            else:
                time.sleep(1)
                print('no proper result, restarting')
                # return self.commands(src, des)
                return self._step_one(src, des)

    def _whether_change_coms(self, ele_picked, src, des, exclude='None'):
        '''
        determine wheather changing the ele or not. return changed ele_id if needed, else return original input, list.
        '''
        ele_direction = 'up' if (des - src) > 0 else 'down'  # up if direction > 0 else down
        ori_des = des
        ori_src = src
        result = [src]
        src, des = self.map_index(src), self.map_index(des)
        candidate_res = self.get_candidate(src, des, ele_picked)
        if len(candidate_res) != 0:
            candidate = candidate_res[0]
            exg_flr = candidate_res[1]
            result.extend(self._get_chg(ele_picked, ori_src, ori_des, candidate, exg_flr, direction=ele_direction,
                                        exclude=exclude))
        return result

    def execute_result(self, route, route_id, amount=1):
        '''
        modify the des_exg_dict in the eles involved in the result, rather than do it in the MainWindow
        :param route, route_id, amount:
        :return: no return, just modify the ele
        '''
        # print('updating ele status')
        print('the route obtained is {}, it is being executed'.format(route))
        if len(route) == 3:
            # route is like: [src, ele, des]
            # this condition contains the insert situation

            ele = [ele for ele in self.eles if ele.ele_name == route[1]][0]
            self.assign_des(ele, des1=route[0], des2=route[2], exg_info=['N', 'N'], amount=amount, route_id=route_id,
                            route_finished=['S', 'E'])
            print('the ele_list of {} is updated to \n{}\nfirst stat is {}'.format(ele.ele_name, ele.des_exg_dict,
                                                                                   ele.is_first))
        elif len(route) == 6:
            # # to be rewrite to handle the new situation
            ele1 = [ele for ele in self.eles if ele.ele_name == route[2]][0]
            if isinstance(route[4], list):
                # ## ALERT!!!!!!!!!!!!!!!
                if len(route[4]) != 0:
                    # if in searching for exg ele
                    self.assign_des(ele1, des1=route[1], des2=route[3], exg_info=['N', 'N'], amount=amount,
                                    route_id=route_id, route_finished=['S', 'E'])
                    # print('the des_exg_dict of {} is updated to \n{},\nthe is_first_stat is {}'.format(ele1.ele_name,
                    #                                                                                    ele1.des_exg_dict,
                    #                                                                                    ele1.is_first))

            else:
                # route is like: [notice, src, cur_ele, temp_flr, chg_ele, des]
                # if the route is already in the ele1's des list, then just update the info

                # #####################################################
                ele1_route_ids = [i[4] for direc in ['up', 'down'] for i in ele1.des_exg_dict[direc]]
                if route_id in ele1_route_ids:
                    self.update_des(ele1, route_id, route[-2])
                else:
                    self.assign_des(ele1, des1=route[1], des2=route[3], exg_info=['N', route[4]], amount=amount,
                                    route_id=route_id, route_finished=['S', 'N'])
                ele2 = [ele for ele in self.eles if ele.ele_name == route[-2]][0]
                self.assign_des(ele2, des1=route[3], des2=route[5], exg_info=[route[2], 'N'], amount=amount,
                                route_id=route_id, route_finished=['N', 'E'])
                # print('the amount of people in {} before moving is {}'.format(ele1.ele_name, ele1.current_amount))
                # print('the amount of people in {} before moving is {}'.format(ele2.ele_name, ele2.current_amount))
            print('the des_exg_dict of {} is updated to \n{},\nthe is_first_stat is {}'.format(ele1.ele_name,
                                                                                               ele1.des_exg_dict,
                                                                                               ele1.is_first))
            try:
                print('the des_exg_dict of {} is updated to \n{},\nthe is_first_stat is {}'.format(ele2.ele_name,
                                                                                                   ele2.des_exg_dict,
                                                                                                   ele2.is_first))
            except:
                pass

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
        # print('the des_exg_dict of {} updated before is \n{}'.format(ele.ele_name, ele.des_exg_dict))
        ele.update_des_exg_dict()

    def update_des(self, ele, route_id, exg_ele):
        # update the exg and is_finished status to the right one
        print('the route_id already exists, updating it')
        for direc in ['up', 'down']:
            for index, des_set in enumerate(ele.des_exg_dict[direc]):
                if (route_id in des_set) & ('E' in des_set):
                    ele.des_exg_dict[direc][index][1] = exg_ele
                    ele.des_exg_dict[direc][index][-1] = 'N'

    # ############ Two main function ##############

    def commands(self, src, des, skip=0, ele_last=None, exclude_1='None', exclude_2='None'):
        if skip == 1:
            ele_picked = ele_last
        else:
            ele_picked = self._step_one(src, des, exclude=exclude_1)
        print('ele_picked after step one is  {}, and des is {}'.format(ele_picked, des))
        change_result = self._whether_change_coms(ele_picked, src, des, exclude=exclude_2)
        if len(change_result) == 5:
            # output the notice if change needed. string
            change_notice = self._notice(chg_ele=change_result[3], temp_flr=change_result[2], des=des)
            # print(change_notice)
            change_result.insert(0, change_notice)
        else:
            change_result = [src, ele_picked, des]
        validity = self.check_validity(change_result)
        if validity == 0:
            print('the validity is 0')
            return change_result
        if validity == 5:
            print('the validity is 5')
            mapped_src, mapped_des = self.map_index(src), self.map_index(des)
            candidate_ele = self.get_candidate(mapped_src, mapped_des, ele_picked)
            change_result[-2] = candidate_ele[0]
            return change_result
        elif validity == 1:
            # the first ele is dropped, so change both two eles
            print('the validity is 1, back to get result')
            time.sleep(0.5)
            return self.commands(src, des, exclude_1=ele_picked)
        elif validity == 2:
            # the first ele is kept, just change the second ele
            print('the validity is 2, back to get result')
            time.sleep(0.5)
            return self.commands(src, des, skip=1, ele_last=ele_picked, exclude_2=change_result[-2])

    # def run_schedule(self, src, des):
    #     route = self.commands(src, des)
    #     self.result_sig.emit(route)

    def run_commands(self):
        # self.isRunning = True
        # time.sleep(5)
        print('seeking result..........from {} to {}'.format(self.src, self.des))
        schedule_result = self.commands(self.src, self.des)
        print('the result calculated is {}'.format(schedule_result))
        # ## the notice is like: [notice, src, cur_ele, temp_flr, chg_ele, des] or [src, ele, des]
        self.result_sig.emit(schedule_result)
        print('the amount of people is {}'.format(self.amount))
        self.execute_result(schedule_result, self.route_id, self.amount)
        # print('the result_sig is emitted out.................')
        # if the exg_ele is not confirmed, then go back to search for a ele if possible
        # print('length of schedule result is {} and type of schedule_result[3] is {}'.format(len(schedule_result), type(schedule_result[3])))
        if len(schedule_result) == 6:
            if isinstance(schedule_result[4], list):
                # print('len of schedule_result[3] is {}'.format(len(schedule_result[4])))
                if len(schedule_result[4]) != 0:
                    print('in the progress of loop searching')
                    ele_direction = 'up' if (schedule_result[-1] - schedule_result[1]) > 0 else 'down'
                    change_result = self._get_chg(schedule_result[2], schedule_result[1], schedule_result[-1],
                                                  schedule_result[4], schedule_result[3], direction=ele_direction,
                                                  solo=True)
                    change_result.insert(0, schedule_result[1])
                    change_notice = self._notice(chg_ele=change_result[3], temp_flr=change_result[2],
                                                 des=change_result[-1])
                    change_result.insert(0, change_notice)
                    schedule_result = change_result
                    self.result_sig.emit(schedule_result)
                    self.execute_result(schedule_result, self.route_id, self.amount)
        print('the schedule is done, finished_sig is to be sent')
        self.isRunning = False
        self.finished_sig.emit()

    def test(self):
        while True:
            time.sleep(3)
            print('inside infinite loop of scheduler...{}'.format(self.test_src))

# coding: utf-8
# Date: 2017-05-10
# Author: cyL
import random
import time

from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal


class Schedule(QObject):
    """A class that implements two schedule strategy"""
    # global constant:
    result_sig = pyqtSignal(list)
    def __init__(self, eles):
        super(Schedule, self).__init__()
        self.eles = eles
        # should the AVAI_MATRIX be changed
        # self.AVAI_MATRIX = [[('A', 'B1', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1')],
        #                     [('A', 'C1', 'D1'), ('A', 'B2', 'C1', 'D1'), ('A', 'B2', 'D1'), ('A', 'B2', 'D1')],
        #                     [('A', 'B2', 'D1'), ('A', 'B2', 'D1'), ('A', 'B2', 'C2', 'D1'), ('A', 'B2', 'C2')],
        #                     [('A', 'B2', 'C2', 'D2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2', 'D2')]]

        self.AVAI_MATRIX = [('A', 'B1', 'C1', 'D1'),
                            ('A', 'B2', 'C1', 'D1'),
                            ('A', 'B2', 'C2', 'D1'),
                            ('A', 'B2', 'C2', 'D2')]

        self.ELE_DICT = {'A': 0, 'B1': 1, 'C1': 2,
                         'D1': 3, 'B2': 4, 'C2': 5, 'D2': 6}

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
        random.seed = 111
        return random.choice(picked_eles)

    def _notice(self, chg_ele, temp_flr, des):
        # message = "The final destination of current elecar is {}, the people who go to {} should change to elecar {} at {}".format(temp_flr, des, chg_ele, temp_flr)
        message = "电梯到达楼层为{}层, 去往{}层的乘客请在{}层换乘{}".format(
            temp_flr, des, temp_flr, chg_ele)
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
        print('calculating Dcc, Dcd among {}'.format(name_set))
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
        current_amount = ele.get_current_amount()
        midway_floors = [des_floor[0] for des_floor in ele.des_exg_dict[ele.running_set] if des_floor[0] < floor]
        increasement = len(
            midway_floors) * 1  # this number is reserved to be changed to simulate the real situation that more than one person would get in at one time
        total_amount = current_amount + increasement
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
        print('choosing from static set :{}'.format(static_set))
        ele_status = self._get_y_status(static_set)
        ele_picked = self._nearest_ele({key: ele_status[key] for key in static_set}, src)
        return ele_picked

    def _get_chg(self, cur_ele, src, des, candidate, temp_flr, direction=None):
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
            candidate = self.adjust_set(candidate, src, des)
            candidate_eles = [self.eles[self.ELE_DICT[i]] for i in candidate]

            print('candidate_eles are {}'.format(candidate_eles))
            available_eles = [ele for ele in candidate_eles if (ele.direction == direction) | (ele.direction == 'stop')]
            print('available eles for exg are {}'.format([ele.ele_name for ele in available_eles]))
            if len(available_eles) == 0:
                if self.eles[self.ELE_DICT[cur_ele]] == temp_flr:
                    print(
                        'There arrives at the {} floor, there is no available eles for {}, please go out call the ele again'.format(
                            temp_flr, des))
                else:
                    # for i in range(100000000):
                    #     print('infinite loop')
                    time.sleep(0.01)
                    # QtGui.QApplication.processEvents()
                    # print('in the loop of searching available eles')
                    # # whether the location obtained could be the updated?
                    # # here is found to slow down the main UI, should to be handled......
                    # # ==========debug code=============
                    # # print('candidates are {}'.format(candidate))
                    # # =================================
                    self._get_chg(cur_ele, src, des, candidate, temp_flr, direction=direction)
            else:
                temp_status = self._get_y_status([ele.ele_name for ele in available_eles])
                chg_ele = self._nearest_ele(temp_status, temp_flr)
                print('change ele is {}'.format(chg_ele))
                return [cur_ele, temp_flr, chg_ele, des]
        else:
            temp_status = self._get_y_status(candidate)
            chg_ele = self._nearest_ele(temp_status, temp_flr)
            return [cur_ele, temp_flr, chg_ele, des]

    def _step_one(self, src, des):
        '''
        got the ele in first step
        '''
        # select available ele_cars. return ele_id list
        ava_eles = self._select_avai_ele(src)
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
                    time.sleep(1)
                    self.commands(src, des)
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
                    time.sleep(1)
                    self.commands(src, des)
            else:
                # print('the down_set is {}'.format(down_set))
                Dcc, Dcd = self._cal_distance(up_set, src)
                Dcc_Dcd = {key: abs(Dcc[key]) - abs(Dcd[key]) for key in Dcc.keys() if Dcc[key] >= 0}
        elif src == des:
            print('The destination is the current floor, no need for elevator!')
            return 'X'
        # get the min(Dcc_Dcd.values>0), or choose from (Dcc_Dcd.values>0) randomly

        # # if Dcc_Dcd is empty, then check static set
        if len(Dcc_Dcd) == 0:
            if len(static_set) != 0:
                ele_picked = self._choose_from_static(static_set, src)
                return ele_picked
            else:
                time.sleep(1)
                self.commands(src, des)
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
                ele_picked = random.choice([i for i in Dcc_Dcd.keys() if Dcc_Dcd[i] < 0])
            if not self._is_full(ele_picked, src):
                return ele_picked
            else:
                time.sleep(1)
                print('no proper result, back to the beginning')
                self.commands(src, des)

    def _whether_change_coms(self, ele_picked, src, des):
        '''
        determine wheather changing the ele or not. return changed ele_id if needed, else return original input, list.
        '''
        ele_direction = 'up' if (des - src) > 0 else 'down'  # up if direction > 0 else down
        ori_des = des
        ori_src = src
        result = [src]
        src, des = self.map_index(src), self.map_index(des)

        if src == 0:
            if des == 1:
                if ele_picked == 'B1':
                    result.extend(self._get_chg('B1', ori_src, ori_des, ['A', 'C', 'D1'], 15, direction=ele_direction))
            elif des == 2:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_src, ori_des, ['A', 'B2', 'D1'], 30, direction=ele_direction))
                elif ele_picked == 'B1':
                    result.extend(self._get_chg('B1', ori_src, ori_des, ['A', 'D1'], 15, direction=ele_direction))
            elif des == 3:
                if ele_picked == 'B1':
                    result.extend(self._get_chg('B1', ori_src, ori_des, ['A'], 15, direction=ele_direction))
                elif ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_src, ori_des, ['A', 'B2'], 30, direction=ele_direction))
                elif ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_src, ori_des, ['A', 'B2', 'C2'], 45, direction=ele_direction))

        elif src == 1:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_src, ori_des, ['A', 'C1', 'D1'], 16, direction=ele_direction))
            elif des == 2:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_src, ori_des, ['A', 'B2', 'D1'], 30, direction=ele_direction))
            elif des == 3:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_src, ori_des, ['A'], 30, direction=ele_direction))
                elif ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_src, ori_des, ['A', 'B2', 'C2'], 45, direction=ele_direction))

        elif src == 2:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_src, ori_des, ['A', 'C1', 'D1'], 16, direction=ele_direction))
                elif ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_src, ori_des, ['A', 'D1'], 31, direction=ele_direction))
            elif des == 1:
                if ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_src, ori_des, ['A', 'B2', 'D1'], 31, direction=ele_direction))
            elif des == 3:
                if ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_src, ori_des, ['A', 'B2', 'C2'], 45, direction=ele_direction))

        elif src == 3:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_src, ori_des, ['A', 'C1', 'D1'], 16, direction=ele_direction))
                elif ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_src, ori_des, ['A', 'D1'], 31, direction=ele_direction))
                elif ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_src, ori_des, ['A'], 46, direction=ele_direction))
            elif des == 1:
                if ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_src, ori_des, ['A', 'B2', 'D1'], 31, direction=ele_direction))
                elif ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_src, ori_des, ['A', 'B2'], 46, direction=ele_direction))
            elif des == 2:
                if ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_src, ori_des, ['A', 'B2', 'C2'], 46, direction=ele_direction))
        return result

    # ############ Two main function ##############

    def commands(self, src, des):
        ele_picked = self._step_one(src, des)
        # =================debug code=============
        print('ele_picked after step one is  {}, and des is {}'.format(ele_picked, des))
        change_result = self._whether_change_coms(ele_picked, src, des)
        if len(change_result) == 5:
            # output the notice if change needed. string
            change_notice = self._notice(
                chg_ele=change_result[3], temp_flr=change_result[2], des=des)
            # print(change_notice)
            change_result.insert(0, change_notice)
            return change_result
        else:
            return [src, ele_picked, des]

    def run_schedule(self, src, des):
        route = self.commands(src, des)
        self.result_sig.emit(route)


if __name__ == '__main__':
    pass

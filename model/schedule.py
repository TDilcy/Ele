# coding: utf-8
# Date: 2017-05-10
# Author: cyL
import random
import time


class Schedule(object):
    """A class that implements two schedule strategy"""
    # global constant:

    def __init__(self, eles):
        super(Schedule, self).__init__()
        self.eles = eles
        # should the AVAI_MATRIX be changed
        self.AVAI_MATRIX = [[('A', 'B1', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1')],
                            [('A', 'C1', 'D1'), ('A', 'B2', 'C1', 'D1'),
                             ('A', 'B2', 'D1'), ('A', 'B2', 'D1')],
                            [('A', 'B2', 'D1'), ('A', 'B2', 'D1'),
                             ('A', 'B2', 'C2', 'D1'), ('A', 'B2', 'C2')],
                            [('A', 'B2', 'C2', 'D2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2', 'D2')]]

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

    def _select_avai_ele(self, src, des):
        '''
        1. map the src and des to the matrix index.
        2. select available ele_cars from a matrix using the src and des as index, return ele_id set
        '''
        src, des = self.map_index(src), self.map_index(des)
        avai_eles = self.AVAI_MATRIX[src][des]
        return avai_eles

    def _nearest_ele(self, ele_cur_floor, src):
        '''
        ele_cur_floor: a dict that contains each ele's current floor
        obtain the current floor of the ele_cur_floor, and then calculate the distance between passager and each ele_car,
        and picked the nearest one. return picked ele_id, if there are more than one being picked, then choose one randomly
        '''
        min_distance = min([abs(i - src) for i in ele_cur_floor.values()])
        picked_eles = [i for i in ele_cur_floor.keys() if abs(
            ele_cur_floor[i] - src) == min_distance]
        return random.choice(picked_eles)

    def _whether_change(self, ele_picked, src, des):
        '''
        determine wheather changing the ele or not. return changed ele_id if needed, else return original input, tuple.
        '''
        ori_des = des
        result = [src]
        src, des = self.map_index(src), self.map_index(des)

        # def get_chg(cur_ele, candidate, temp_flr):
        #     temp_status = self._get_y_status(candidate)
        #     chg_ele = self._nearest_ele(temp_status, temp_flr)
        #     return [cur_ele, temp_flr, chg_ele, ori_des]

        if src == 0:
            if des == 2:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_des, ['A', 'B2', 'D1'], 30))
            elif des == 3:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_des, ['A', 'B2'], 30))
                elif ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_des, ['A', 'B2', 'C2'], 45))

        elif src == 1:
            if des == 3:
                if ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_des, ['A', 'B2', 'C2'], 45))
        elif src == 2:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_des, ['A', 'C1', 'D1'], 16))

        elif src == 3:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_des, ['A', 'C1', 'D1'], 16))
                elif ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_des, ['A', 'D1'], 31))
                elif ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_des, ['A'], 46))
            elif des == 1:
                if ele_picked == 'C2':
                    # do something
                    result.extend(self._get_chg('C2', ori_des, ['A', 'B2', 'D1'], 31))
        return result

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

    ####################### function used in commands ##########

    def _step_one(self, src, des):
        '''
        got the ele in first step
        '''
        # select available ele_cars. return ele_id list
        ava_eles = self._select_avai_ele(src, des)
        # divide the eles into up, down, static set
        up_set, down_set, static_set = self._disc_status(ava_eles)
        # get ele status
        if src < des:  # which means that the passenger expects to go upstairs
            if len(up_set) == 0:
                # whether should consider that the ele is full when it arrive at the floor of the first caller, because other people may also call during the process
                # for instance: A: 1 ————> 25, another is A: 3————>22, and the latter may make the ele be fully occupied
                # for now, we think that the first command would gain higher
                # priority, and won't be broken
                if len(static_set) != 0:
                    ele_picked = self._choose_from_static(static_set, src)
                    return ele_picked
                else:
                    time.sleep(1)
                    self.commands(src, des)
            else:
                Dcc, Dcd = self._cal_distance(up_set.keys(), src)
                Dcc_Dcd = {key: abs(Dcc[key]) - abs(Dcd[key])
                           for key in Dcc.keys() if Dcc[key] <= 0}
        elif src > des:
            if len(down_set) == 0:
                ele_picked = self._choose_from_static(static_set, src)
                return ele_picked
            else:
                Dcc, Dcd = self._cal_distance(up_set.keys(), src)
                Dcc_Dcd = {key: abs(Dcc[key]) - abs(Dcd[key])
                           for key in Dcc.keys() if Dcc[key] >= 0}
        elif src == des:
            print('The destination is the current floor, no need for elevator!')
            return 'X'
        # get the min(Dcc_Dcd.values>0), or choose from (Dcc_Dcd.values>0)
        # randomly
        above_0 = [value for value in Dcc_Dcd.values() if value > 0]
        if len(above_0) != 0:
            ele_picked = random.choice(
                [i for i in Dcc_Dcd.keys() if Dcc_Dcd[i] == min(above_0)])
        else:
            ele_picked = random.choice(
                [i for i in Dcc_Dcd.keys() if Dcc_Dcd[i] < 0])
        if not self._is_full(ele_picked, src):
            return ele_picked
        else:
            time.sleep(1)
            self.commands(src, des)

    def _disc_status(self, ele_names):
        '''
        divide the available eles into different sets
        :param elenames:
        :return: up_set, down_set, static_set, list containing the name of the eles
        '''
        eles = [self.eles[self.ELE_DICT[i]] for i in ele_names]
        ele_sets = {direc: [ele for ele in eles if ele.direction == direc] for direc in ['up', 'down', 'stop']}
        return ele_sets['up'], ele_sets['down'], ele_sets['stop']

    def _cal_distance(self, name_set, floor):
        '''
        Calculate the distance between the floor and the chosen eles, which is assigned to Dcc.
        Calculate the distance between the nearest target and the current floor of each eles, which is taken as Dcd
        :param set:
        :param floor:
        :return: Dcd, Dcd, dict type
        '''
        eles = {i: self.eles[self.ELE_DICT[i]] for i in name_set}
        Dcc = {i: eles[i].getLocation() - floor for i in eles.keys()}
        Dcd = {i: eles[i].getLocation() - min(eles[i].des_list) for i in eles.keys()}
        return Dcc, Dcd

    def _is_full(self, ele, floor):
        '''
        judge if the ele would be full when arriving at specific floor, the index may be the number of people or the total weight
        :param ele:
        :param floor:
        :return: Boolean
        '''
        current_amount = ele.get_current_amount()
        midway_floors = [des_floor for des_floor in ele.des_list if des_floor < floor]
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
        ele_status = self._get_y_status(static_set)
        ele_picked = self._nearest_ele(
            {key: ele_status[key] for key in static_set}, src)
        return ele_picked

    def _get_chg(self, cur_ele, des, candidate, temp_flr, direction=None):
        '''
        recurrently find the available elecar  from candidates, if failed at the destination, use a different flag to indicate the failing info
        :param cur_ele:
        :param candidate:
        :param temp_flr:
        :return:
        '''
        if direction is not None:
            candidate_eles = [self.eles[self.ELE_DICT[i]] for i in candidate]
            available_eles = [ele for ele in candidate_eles if ele.direction == direction]
            if len(available_eles) == 0:
                if self.eles[self.ELE_DICT[cur_ele]] == temp_flr:
                    print(
                        'There arrives at the {} floor, there is no available eles for {}, please go out call the ele again'.format(
                            temp_flr, des))
                else:
                    time.sleep(1)
                    print('in the loop of searching available eles')
                    # whether the location obtained could be the updated?
                    self._get_chg(cur_ele, des, direction, candidate, temp_flr)
            else:
                temp_status = self._get_y_status([ele.ele_name for ele in available_eles])
                chg_ele = self._nearest_ele(temp_status, temp_flr)
                return [cur_ele, temp_flr, chg_ele, des]
        else:
            temp_status = self._get_y_status(candidate)
            chg_ele = self._nearest_ele(temp_status, temp_flr)
            return [cur_ele, temp_flr, chg_ele, des]

    def _whether_change_coms(self, ele_picked, src, des):
        '''
        determine wheather changing the ele or not. return changed ele_id if needed, else return original input, list.
        '''
        ele_direction = 'up' if (des - src) > 0 else 'down'  # up if direction > 0 else down
        ori_des = des
        result = [src]
        src, des = self.map_index(src), self.map_index(des)

        if src == 0:
            if des == 1:
                if ele_picked == 'B1':
                    result.extend(self._get_chg('B1', ori_des, ['A', 'C', 'D1'], 15, direction=ele_direction))
            elif des == 2:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_des, ['A', 'B2', 'D1'], 30, direction=ele_direction))
            elif des == 3:
                if ele_picked == 'B1':
                    result.extend(self._get_chg('B1', ori_des, ['A'], 15, direction=ele_direction))
                elif ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_des, ['A', 'B2'], 30, direction=ele_direction))
                elif ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_des, ['A', 'B2', 'C2'], 45, direction=ele_direction))

        elif src == 1:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_des, ['A', 'C1', 'D1'], 16, direction=ele_direction))
            elif des == 2:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_des, ['A', 'B2', 'D1'], 30, direction=ele_direction))
            elif des == 3:
                if ele_picked == 'C1':
                    result.extend(self._get_chg('C1', ori_des, ['A'], 30, direction=ele_direction))
                elif ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_des, ['A', 'B2', 'C2'], 45, direction=ele_direction))

        elif src == 2:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_des, ['A', 'C1', 'D1'], 16, direction=ele_direction))
                elif ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_des, ['A', 'D1'], 31, direction=ele_direction))
            elif des == 1:
                if ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_des, ['A', 'B2', 'D1'], 31, direction=ele_direction))
            elif des == 3:
                if ele_picked == 'D1':
                    result.extend(self._get_chg('D1', ori_des, ['A', 'B2', 'C2'], 45, direction=ele_direction))

        elif src == 3:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(self._get_chg('B2', ori_des, ['A', 'C1', 'D1'], 16, direction=ele_direction))
                elif ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_des, ['A', 'D1'], 31, direction=ele_direction))
                elif ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_des, ['A'], 46, direction=ele_direction))
            elif des == 1:
                if ele_picked == 'C2':
                    result.extend(self._get_chg('C2', ori_des, ['A', 'B2', 'D1'], 31, direction=ele_direction))
                elif ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_des, ['A', 'B2'], 46, direction=ele_direction))
            elif des == 2:
                if ele_picked == 'D2':
                    result.extend(self._get_chg('D2', ori_des, ['A', 'B2', 'C2'], 46, direction=ele_direction))
        return result

    # ############ Two main function ##############

    def one_command(self, src, des):
        '''
        input: the current and the destination floor
        output: the scheduling scheme: the route passagers should follow and the notice.
        '''

        # select available ele_cars. return ele_id list
        ava_eles = self._select_avai_ele(src, des)
        # ##TODO: get the current status of each eles
        ele_status = self._get_y_status(ava_eles)
        # calculate the distance between passager and each ele_car, and picked the
        # nearest one. return picked ele_id
        ele_picked = self._nearest_ele(ele_status, src)
        # determine wheather changing the ele or not. return changed ele_id if
        # needed, else return original input. dict
        change_result = self._whether_change(ele_picked, src, des)
        if len(change_result) == 5:
            # output the notice if change needed. string
            change_notice = self._notice(
                chg_ele=change_result[3], temp_flr=change_result[2], des=des)
            # print(change_notice)
            change_result.insert(0, change_notice)  # add the info at the first place of the route
            return change_result
        else:
            return [src, ele_picked, des]

    def commands(self, src, des):
        ele_picked = self._step_one(src, des)
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


if __name__ == '__main__':
    pass

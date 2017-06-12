# coding: utf-8
# Date: 2017-05-10
# Author: cyL
import random


class Schedule(object):
    """A class that implements two shedule strategy"""
    # global constant:

    def __init__(self, eles):
        super(Schedule, self).__init__()
        self.eles = eles
        self.AVAI_MATRIX = [[('A', 'B1', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1'), ('A', 'C1', 'D1')],
                            [('A', 'C1', 'D1'), ('A', 'B2', 'C1', 'D1'),
                             ('A', 'B2', 'D1'), ('A', 'B2', 'D1')],
                            [('A', 'B2', 'D1'), ('A', 'B2', 'D1'),
                             ('A', 'B2', 'C2', 'D1'), ('A', 'B2', 'C2')],
                            [('A', 'B2', 'C2', 'D1'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2'), ('A', 'B2', 'C2', 'D2')]]

        self.ELE_DICT = {'A': 0, 'B1': 1, 'C1': 2,
                         'D1': 3, 'B2': 4, 'C2': 5, 'D2': 6}

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
        change_result = self._wheather_change(ele_picked, src, des)
        if len(change_result) == 5:
            # output the notice if change needed. string
            change_notice = self._notice(
                chg_ele=change_result[3], temp_flr=change_result[2], des=des)
            # print(change_notice)
            change_result.append(change_notice)
            return change_result
        else:
            return [src, ele_picked, des]

    def commands(self, src, des):
        pass

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
        if len(picked_eles) != 1:
            return random.choice(picked_eles)
            # return 'D1'
        else:
            return picked_eles[0]

    def _wheather_change(self, ele_picked, src, des):
        '''
        determine wheather changing the ele or not. return changed ele_id if needed, else return original input, tuple.
        '''
        ori_des = des
        result = [src]
        src, des = self.map_index(src), self.map_index(des)
        def get_chg(cur_ele, candidate, temp_flr):
            temp_status = self._get_y_status(candidate)
            chg_ele = self._nearest_ele(temp_status, temp_flr)
            return [cur_ele, temp_flr, chg_ele, ori_des]

        if src == 0:
            if des == 2:
                if ele_picked == 'C1':
                    result.extend(get_chg('C1', ['A', 'B2', 'D1'], 30))
            elif des == 3:
                if ele_picked == 'C1':
                    result.extend(get_chg('C1', ['A', 'B2'], 30))
                elif ele_picked == 'D1':
                    result.extend(get_chg('D1', ['A', 'B2', 'C2'], 45))

        elif src == 1:
            if des == 3:
                if ele_picked == 'D1':
                    result.extend(get_chg('D1', ['A', 'B2', 'C2'], 45))
        elif src == 2:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(get_chg('B2', ['A', 'C1', 'D1'], 16))

        elif src == 3:
            if des == 0:
                if ele_picked == 'B2':
                    result.extend(get_chg('B2', ['A', 'C1', 'D1'], 16))
                elif ele_picked == 'C2':
                    result.extend(get_chg('C2', ['A', 'D1'], 31))
            elif des == 1:
                if ele_picked == 'C2':
                    # do something
                    result.extend(get_chg('C2', ['A', 'B2', 'D1'], 31))
        return result

    def _notice(self, chg_ele, temp_flr, des):
        # message = "The final destination of current elecar is {}, the people who go to {} should change to elecar {} at {}".format(temp_flr, des, chg_ele, temp_flr)
        message = "此电梯到达楼层为{}层, 去往{}层的乘客请在{}层换乘{}".format(temp_flr, des, temp_flr,chg_ele)
        return message

    def _get_y_status(self, picked_name):
        '''
        get the y_position of picked eles, return a dict that contains the name of ele and its corresponding y_location
        '''
        picked_ele = [self.eles[self.ELE_DICT[i]] for i in picked_name]
        return {i.ele_name: i.getLocation() for i in picked_ele}


if __name__ == '__main__':
    pass

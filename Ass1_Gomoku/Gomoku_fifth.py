import numpy as np
import random
import time

COLOR_BLACK = 1
COLOR_WHITE = -1
COLOR_NONE = 0
INFINITE = 1145141919
random.seed(114514)
ARRAY_SCORE = [1145141, 114514, 1000, 200, 51, 5, 3, -15, -10, -5]
# ARRAY_SCORE = [114514, 11451, 1000, 200, 51, 5, 3, -15, -10, -5]
DEPTH_OF_RUN = 0


# (alive_five, alive_four, jump_four, alive_three, sleep_three, alive_double, sleep_double, death_four, death_three, death_double)


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard_2):
        print(chessboard_2)
        print(self.color)
        chessboard = np.asanyarray(chessboard_2)
        times = time.time()
        self.candidate_list.clear()
        idx_null = np.where(chessboard != COLOR_NONE)
        if len(idx_null[0]) == 0:
            self.candidate_list.append((7, 7))
            return
        idx = self.judgement_location(chessboard)
        idx_used = idx.copy()
        dict_slip = {}
        numbers = [0] * len(idx)
        max_score = -INFINITE
        max_order = 0
        alpha = -INFINITE
        beta = INFINITE
        times = time.time()
        arrays_chessboard = get_arrays(chessboard)
        for i in range(0, len(idx)):
            print("{} finished".format(idx[i]))
            print(time.time() - times)
            idx_used.remove(idx[i])
            numbers[i] = self.basic_decides(chessboard, arrays_chessboard, idx[i], self.color, dict_slip)
            # numbers[i] = self.alpha_beta_decides(chessboard, idx_used, arrays_chessboard, idx[i], idx[i], DEPTH_OF_RUN, alpha, beta, self.color, dict_slip)
            idx_used.append(idx[i])
            print(numbers[i])
            if max_score < numbers[i]:
                max_score = numbers[i]
                max_order = i
                self.candidate_list.append(numbers[i])
        new_pos = idx[max_order]
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        print(new_pos)
        print("choose this one")
        self.candidate_list.append(new_pos)
        print(time.time() - times)
        return

    # first function
    def judgement_location(self, chessboard):
        notidx = np.where(chessboard != COLOR_NONE)
        willdelete = []
        length = 4
        xmin = max(0, min(notidx[0]) - length)
        xmax = min(max(notidx[0]) + length, self.chessboard_size)
        ymin = max(0, min(notidx[1]) - length)
        ymax = min(max(notidx[1]) + length, self.chessboard_size)
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for i in idx:
            if i[0] < xmin or i[0] > xmax or i[1] < ymin or i[1] > ymax:
                willdelete.append(i)
        for i in willdelete:
            idx.remove(i)
        return idx

    def basic_decides(self, chessboard, arrays_chessboard, point, full_color, dict_slip):
        chessboard[point[0]][point[1]] = full_color
        willreturn = self.get_grade(chessboard, point, arrays_chessboard, dict_slip)
        chessboard[point[0]][point[1]] = 0
        return willreturn

    def get_grade(self, chessboard, point, arrays_chessboard, dict_slip):
        net_score = 98 - (point[0] - 7) ** 2 - (point[1] - 7) ** 2
        point_color = chessboard[point[0]][point[1]]
        if point_color == self.color:
            my_foumula = produce_formula(arrays_chessboard, self.color, dict_slip)
            chessboard[point[0]][point[1]] = -self.color
            your_foumula = produce_formula(arrays_chessboard, self.color * -1, dict_slip)
            chessboard[point[0]][point[1]] = self.color
        else:
            your_foumula = produce_formula(arrays_chessboard, self.color * -1, dict_slip)
            chessboard[point[0]][point[1]] = self.color
            my_foumula = produce_formula(arrays_chessboard, self.color, dict_slip)
            chessboard[point[0]][point[1]] = -self.color
        for i in range(0, 10, 1):
            net_score += my_foumula[i] * ARRAY_SCORE[i]
            net_score += your_foumula[i] * ARRAY_SCORE[i]
        # 双冲四,双活三,冲四活三,活三眠三  初始化计分
        if my_foumula[2] >= 2 or (my_foumula[2] >= 1 and my_foumula[3] >= 1) or my_foumula[3] >= 2:
            net_score += 5141 * (my_foumula[2] + my_foumula[3])
        if my_foumula[3] >= 1 and my_foumula[4] >= 1:
            net_score += 514 * (my_foumula[3] + my_foumula[4])
        if your_foumula[2] >= 2 or (your_foumula[2] >= 1 and your_foumula[3] >= 1) or your_foumula[3] >= 2:
            net_score += 5141 * (your_foumula[2] + your_foumula[3])
        if your_foumula[3] >= 1 and your_foumula[4] >= 1:
            net_score += 514 * (your_foumula[3] + your_foumula[4])
        # 双冲四,双活三,冲四活三,活三眠三 进阶计分
        if my_foumula[2] >= 2:
            net_score += 1145
        if your_foumula[2] >= 2:
            net_score -= 800
        if my_foumula[2] == 1 and my_foumula[3] >= 1:
            net_score += 500
        if your_foumula[2] == 1 and your_foumula[3] >= 1:
            net_score -= 300
        if my_foumula[3] >= 2:
            net_score += 200
        if your_foumula[3] >= 2:
            net_score -= 100
        # 二系列计分
        if my_foumula[5] >= 2:
            net_score += 50 * my_foumula[5]
        if your_foumula[5] >= 2:
            net_score += 49 * your_foumula[5]
        if my_foumula[5] > 1 and my_foumula[6] > 1:
            net_score += (my_foumula[5] + my_foumula[6]) * 5
        if your_foumula[5] > 1 and your_foumula[6] > 1:
            net_score += (your_foumula[5] + your_foumula[6]) * 5
        return net_score

    def alpha_beta_decides(self, chessboard, idxs, arrays_chessboard, point, father_point, depth, alpha, beta, full_color, dict_slip):
        # print(depth)
        chessboard[point[0]][point[1]] = full_color
        if depth <= 0:
            willreturn = self.get_grade(chessboard, point, arrays_chessboard, dict_slip)
            chessboard[point[0]][point[1]] = 0
            return willreturn
        idxs_used = idxs.copy()
        point_choose = (114, 514)
        if full_color == self.color:
            value = -INFINITE
            for i in range(len(idxs)):
                idxs_used.remove(idxs[i])
                temp_value = self.alpha_beta_decides(chessboard, idxs_used, arrays_chessboard, idxs[i], father_point, depth - 1, alpha, beta, full_color * -1,
                                                     dict_slip)
                if value < temp_value:
                    value = temp_value
                    point_choose = idxs[i]
                idxs_used.append(idxs[i])
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
        else:
            value = INFINITE
            for i in range(len(idxs)):
                idxs_used.remove(idxs[i])
                temp_value = self.alpha_beta_decides(chessboard, idxs_used, arrays_chessboard, idxs[i], father_point, depth - 1, alpha, beta, full_color * -1,
                                                     dict_slip)
                if value > temp_value:
                    value = temp_value
                    point_choose = idxs[i]
                idxs_used.append(idxs[i])
                beta = min(beta, value)
                if alpha >= beta:
                    break
        chessboard[point[0]][point[1]] = 0
        print(point, "'s choose point is", point_choose)
        return value


# (alive_five, alive_four, jump_four, alive_three, sleep_three, alive_double, sleep_double, death_four, death_three, death_double)


# it will just run once
def get_arrays(chessboard):
    xmin = ymin = 0
    xmax = ymax = 14
    align = []
    # 切片进去的只有索引
    for i in range(ymin, ymax + 1):
        row2 = chessboard[..., i][xmin:xmax + 1]
        align.append(row2)
    for i in range(xmin, xmax + 1):
        column2 = chessboard[i, ...][ymin:ymax + 1]
        align.append(column2)
    temp_csc = np.fliplr(chessboard)
    for i in range(10):
        sec2 = chessboard.diagonal(offset=i)
        sec3 = chessboard.diagonal(offset=i * -1)
        csc2 = temp_csc.diagonal(offset=i)
        csc3 = temp_csc.diagonal(offset=i * -1)
        align.append(sec2)
        align.append(sec3)
        align.append(csc2)
        align.append(csc3)
    align.append(chessboard.diagonal(0))
    align.append(temp_csc.diagonal(0))
    return align


def produce_formula(arrays, color, dict_slip):
    '''
    :param arrays: a lot of arrays
    :return:
    '''
    formula = []
    net_score = 0
    for i in arrays:
        if (tuple(i), color) in dict_slip:
            formula.append(dict_slip[(tuple(i), color)])
        else:
            alive_five = get_alive_five(i, color)
            alive_four = get_live_four(i, color)
            deaths = get_death(i, color)
            jumps_four_three = multiplu_live_sleep_four_three(i, color)
            doubles = get_alive_sleep_double(i, color)
            dict_slip[(tuple(i), color)] = (
            alive_five, alive_four, jumps_four_three[0], jumps_four_three[1], jumps_four_three[2], doubles[0], doubles[1], deaths[0], deaths[1], deaths[2])
            formula.append(dict_slip[(tuple(i), color)])
    count_formula = [0] * len(formula[0])
    for i in formula:
        for j in range(0, 10, 1):
            count_formula[j] += i[j]
    return count_formula


# 活2 眠2 活2眠2 双活二
def get_alive_sleep_double(array, color):
    '''
    :param array: a list,length is 15
    :param color: 1 or -1,decide which it belongs
    :return:(multiply_live_two,multiply_sleep_two)
    双活二:50x
    活二眠二:5x
    Basic:5x,3x
    '''
    multiply_live_two = 0
    multiply_sleep_two = 0
    for j in range(0, len(array) - 4):
        # 活二 1
        if array[j] == 0 and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == color and array[j + 4] == 0:
            multiply_live_two += 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == 0:
            multiply_live_two += 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == 0:
            multiply_live_two += 1
        # 眠二 1
        elif array[j] == color and array[j + 1] == 0 and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color:
            multiply_sleep_two += 1
    for j in range(0, len(array) - 5):
        # 活二 2
        if array[j] == 0 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == 0:
            multiply_live_two += 1
        # 眠二 2
        elif array[j] == 0 and array[j + 1] == 0 and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color and array[j + 5] == color * -1:
            multiply_sleep_two += 1
        elif array[j] == 0 and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == color * -1:
            multiply_sleep_two += 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == color * -1:
            multiply_sleep_two += 1
        elif array[j] == color * -1 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == 0 and array[j + 5] == 0:
            multiply_sleep_two += 1
        elif array[j] == color * -1 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == 0 and array[j + 5] == 0:
            multiply_sleep_two += 1
        elif array[j] == color * -1 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == 0:
            multiply_sleep_two += 1
    for j in range(0, len(array) - 6):
        # 眠二 3
        if array[j] == color * -1 and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == 0 and \
                array[j + 6] == color * -1:
            multiply_sleep_two += 1
        elif array[j] == color * -1 and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == color and array[j + 4] == 0 and array[j + 5] == 0 and \
                array[j + 6] == color * -1:
            multiply_sleep_two += 1
        elif array[j] == color * -1 and array[j + 1] == 0 and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color and array[j + 5] == 0 and \
                array[j + 6] == color * -1:
            multiply_sleep_two += 1
    return multiply_live_two, multiply_sleep_two


# 死四三二
def get_death(array, color):
    """
    :return: (death_four,death_three,death_two)
    -15.-10,-5(我觉得应该更低一点)
    """
    death_four = 0
    death_three = 0
    death_two = 0
    for j in range(0, len(array) - 3):
        if array[j] == color * -1 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color * -1:
            death_two += 1
    for j in range(0, len(array) - 4):
        if array[j] == color * -1 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color * -1:
            death_three += 1
    for j in range(0, len(array) - 5):
        if array[j] == color * -1 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color and array[
            j + 5] == color * -1:
            death_two += 1
    return death_four, death_three, death_two


# 活五
def get_alive_five(array, color):
    # value: 1 to infinite
    alive_five = 0
    for j in range(0, len(array) - 4):
        if array[j] == color and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color:
            alive_five += 1
    return alive_five


# 活四
def get_live_four(array, color):
    alive_four = 0
    for j in range(0, len(array) - 5):
        if array[j] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color and array[j + 5] == 0:
            alive_four += 1
    return alive_four


# 解决 冲四,活三,眠三,双冲四,双活三,冲四活三,活三眠三
def multiplu_live_sleep_four_three(array, color):
    '''
    :return: jump_four,live_three,sleep_three
    values 1000,200,51
    双冲四/冲四活三/双活三:10000+
    活三眠三:1000+
    另有修正
    '''
    multiply_four = 0
    multiply_three = 0
    multiply_sleep_three = 0
    for j in range(0, len(array) - 4):
        # 冲四 1
        if array[j] == color and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color:
            multiply_four += 1
        elif array[j] == color and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color:
            multiply_four += 1
        elif array[j] == color and array[j + 1] == color and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color:
            multiply_four += 1
        # 眠三 1
        if array[j] == color and array[j + 1] == 0 and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color:
            multiply_sleep_three += 1
        elif array[j] == color and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == 0 and array[j + 4] == color:
            multiply_sleep_three += 1
        elif array[j] == color and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color:
            multiply_sleep_three += 1
        # 活三 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == 0:
            multiply_three += 1
    for j in range(0, len(array) - 5):
        # 冲四 2
        if array[j] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color and array[j + 5] == -1 * color:
            multiply_four += 1
        elif array[j + 5] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color and array[
            j] == -1 * color:
            multiply_four += 1
        # 活三 2
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == 0:
            multiply_three += 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color and array[j + 5] == 0:
            multiply_three += 1
        # 眠三 2
        elif array[j] == 0 and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color and array[j + 5] == color * -1:
            multiply_sleep_three += 1
        elif array[j] == color * -1 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == color and array[j + 4] == 0 and array[j + 5] == 0:
            multiply_sleep_three += 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color and array[j + 5] == color * -1:
            multiply_sleep_three += 1
        elif array[j] == color * -1 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == 0:
            multiply_sleep_three += 1
        elif array[j] == 0 and array[j + 1] == color and array[j + 2] == color and array[j + 3] == 0 and array[j + 4] == color and array[j + 5] == color * -1:
            multiply_sleep_three += 1
        elif array[j] == color * -1 and array[j + 1] == color and array[j + 2] == 0 and array[j + 3] == color and array[j + 4] == color and array[j + 5] == 0:
            multiply_sleep_three += 1
    for j in range(0, len(array) - 6):
        if array[j] == color * -1 and array[j + 1] == 0 and array[j + 2] == color and array[j + 3] == color and array[j + 4] == color and array[j + 5] == 0 and \
                array[j + 6] == color * -1:
            multiply_sleep_three += 1
    return multiply_four, multiply_three, multiply_sleep_three


# hard code,i dont wanna to look it
# second function
def can_put_stone(chessboard, point):
    # return True代表不行,其余可以
    x = point[0]
    y = point[1]
    # 首先 chessboard[x][y] != 0,其次,不能下的情况,只有四周全为-1*chessboard,才不能,即为true
    # 也就是说,可以将其写为[x][y] + [x][y+1] == 0
    if point[0] == 0 and point[1] == 0:
        return (chessboard[0][0] + chessboard[0][1] == 0) and (chessboard[0][0] + chessboard[1][0] == 0) and (
                chessboard[0][0] + chessboard[1][1] == 0)
    elif point[0] == 0 and point[1] == 14:
        return (chessboard[0][14] + chessboard[0][13] == 0) and (chessboard[0][14] + chessboard[1][13] == 0) and (
                chessboard[0][14] + chessboard[1][14] == 0)
    elif point[0] == 14 and point[1] == 0:
        return (chessboard[14][0] + chessboard[14][1] == 0) and (chessboard[14][0] + chessboard[13][1] == 0) and (
                chessboard[14][0] + chessboard[13][0] == 0)
    elif point[0] == 14 and point[1] == 14:
        return (chessboard[14][14] + chessboard[14][13] == 0) and (chessboard[14][14] + chessboard[13][14] == 0) and (
                chessboard[14][14] + chessboard[13][13] == 0)
    elif point[0] == 0 and point[1] != 0 and point[1] != 14:
        return (chessboard[0][y] + chessboard[0][y - 1] == 0) and (chessboard[0][y] + chessboard[0][y + 1] == 0) and (
                chessboard[0][y] + chessboard[1][y] == 0) and (chessboard[0][y] + chessboard[1][y - 1] == 0) and (
                       chessboard[0][y] + chessboard[0][y + 1] == 0)
    elif point[0] == 14 and point[1] != 0 and point[1] != 14:
        return (chessboard[14][y] + chessboard[14][y - 1] == 0) and (
                chessboard[14][y] + chessboard[14][y + 1] == 0) and (
                       chessboard[14][y] + chessboard[13][y] == 0) and (
                       chessboard[14][y] + chessboard[13][y - 1] == 0) and (
                       chessboard[14][y] + chessboard[13][y + 1] == 0)
    elif point[1] == 0 and point[0] != 0 and point[0] != 14:
        return (chessboard[x][0] + chessboard[x - 1][0] == 0) and (chessboard[x][0] + chessboard[x + 1][0] == 0) and (
                chessboard[x][0] + chessboard[x][1] == 0) and (chessboard[x][0] + chessboard[x - 1][0] == 0) and (
                       chessboard[x][0] + chessboard[x + 1][1] == 0)
    elif point[1] == 14 and point[0] != 0 and point[0] != 14:
        return (chessboard[x][14] + chessboard[x - 1][14] == 0) and (
                chessboard[x][14] + chessboard[x + 1][14] == 0) and (
                       chessboard[x][14] + chessboard[x][13] == 0) and (
                       chessboard[x][14] + chessboard[x - 1][13] == 0) and (
                       chessboard[x][14] + chessboard[x + 1][13] == 0)
    else:
        return (chessboard[x][y] + chessboard[x - 1][y] == 0) and (chessboard[x][y] + chessboard[x + 1][y] == 0) and (
                chessboard[x][y] + chessboard[x][y + 1] == 0) and (chessboard[x][y] + chessboard[x][y - 1] == 0) and (
                       chessboard[x][y] + chessboard[x - 1][y - 1] == 0) and (
                       chessboard[x][y] + chessboard[x - 1][y + 1] == 0) and (
                       chessboard[x][y] + chessboard[x + 1][y - 1] == 0) and (
                       chessboard[x][y] + chessboard[x + 1][y + 1] == 0)

    #

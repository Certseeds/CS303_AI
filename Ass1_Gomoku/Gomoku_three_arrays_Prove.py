import numpy as np
import random
import time

COLOR_BLACK = 1
COLOR_WHITE = -1
COLOR_NONE = 0
INFINITE = 1145141919
random.seed(114514)


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list.
        # System will get the end of your candidate_listas your decision .
        self.candidate_list = []
        # The input is current chessboard

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
        numbers = [0]*len(idx)
        max_score = 0
        max_order = 0
        '''test_number = self.get_max_value(chessboard, (5, 5), 1, -11451419, 1919810)
        print(test_number)
        print("test2")'''
        #time.sleep(10000)
        for i in range(0, len(idx)):
            numbers[i] = self.get_max_value(chessboard, idx[i], 0, -1 * 0x3f3f3f, 0x3f3f3f)
            #print(numbers[i])
            if max_score < numbers[i]:
                max_score = numbers[i]
                max_order = i
                self.candidate_list.append(numbers[i])
        '''for i in range(len(idx)):
            print(idx[i])
            print(numbers[i])
            print("-------")'''
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

    def get_max_value(self, chessboard, point, depth, alpha, beta):
        # print(depth)
        chessboard[point[0]][point[1]] = self.color
        # print(chessboard)
        if depth <= 0:
            '''if point == (1,9) or point == (3,2):
                willprint = True
            else:
                willprint = False'''
            willreturn = judgement_grade(chessboard,point)+ abs(7-point[0])**2 + abs(7-point[1])**2
            #willreturn = judgement_grade(chessboard,point) + abs(7-point[0])**2 + abs(7-point[1])**2
            chessboard[point[0]][point[1]] = 0
            return willreturn
        idxs = self.judgement_location(chessboard)
        max_value = -1145141919
        max_value_point = (0, 0)
        for i in idxs:

            score = self.get_min_value(chessboard, i, depth-1, alpha, beta)
            '''if i == (0,0) or i == (1,1):
                print("Trace ON")
                print(score)
                print(i)
                print("Trace off")'''
            if max_value < score:
                max_value = score
                max_value_point = i
            max_value = max(max_value, score)
            '''alpha = max(alpha, max_value)
            if alpha >= beta:
                print("break")
                break'''
        chessboard[point[0]][point[1]] = 0
        return max_value

    def get_min_value(self, chessboard, point, depth, alpha, beta):
        chessboard[point[0]][point[1]] = self.color * -1
        '''if point == (1, 1) or point == (0, 0):
            print(chessboard)
            print(judgement_grade(chessboard,False))'''
        if depth <= 0:
            # print("back to max")
            if point == (1,9) or point == (3,2):
                willprint = True
            else:
                willprint = False
            willreturn = judgement_grade(chessboard,point,willprint)
            chessboard[point[0]][point[1]] = 0
            return willreturn
        idxs = self.judgement_location(chessboard)
        min_value = 1145141919
        for i in idxs:
            score = self.get_max_value(chessboard, i, depth - 1, alpha, beta)
            min_value = min(min_value, score)
            '''beta = min(beta, min_value)
            if alpha > beta:
                break'''
        chessboard[point[0]][point[1]] = 0
        return min_value


def judgement_grade(chessboard,point,willprint = False):
    this_color = chessboard[point[0]][point[1]]
    net_score = 0
    # if return in he_re ,it means it can not be put
    judge_arrays = get_arrays(chessboard)
    if willprint:
        print(net_score)
        for i in judge_arrays:
            print(i)
            if np.array_equal(i, [0, 1, 1, 1, 1, -1, 0,  0,  0, 0 , 0 , 0 , 0 , 0 , 0]):
                print("yes")
                print(judgement_multiply_live_jump_four_or_three([i], 1))
        print(judgement_live_five(judge_arrays, this_color))
        print(judgement_live_four(judge_arrays, this_color))
        multiply_four_and_three_me = judgement_multiply_live_jump_four_or_three(judge_arrays, this_color)
        print(multiply_four_and_three_me)
        print(multiply_four_and_three_me[0])
        print(judgement_dead_four_three_two(judge_arrays, this_color))
        print(judgement_doubles(judge_arrays, this_color))
        this_color *= -1
        print(judgement_live_five(judge_arrays, this_color))
        print(judgement_live_four(judge_arrays, this_color))
        multiply_four_and_three_me = judgement_multiply_live_jump_four_or_three(judge_arrays, this_color)
        print(multiply_four_and_three_me)
        print(judgement_dead_four_three_two(judge_arrays, this_color))
        print(judgement_doubles(judge_arrays, this_color))
        this_color *= -1
        print("finished")
    if willprint:
        print(net_score)
    net_score += judgement_live_five(judge_arrays, this_color)
    if willprint:
        print(net_score)
    net_score += judgement_live_four(judge_arrays, this_color)
    if willprint:
        print(net_score)
    multiply_four_and_three_me = judgement_multiply_live_jump_four_or_three(judge_arrays, this_color)
    if willprint:
        print(multiply_four_and_three_me)
    net_score += multiply_four_and_three_me[0]
    if willprint:
        print(net_score)
    net_score += judgement_dead_four_three_two(judge_arrays, this_color)
    if willprint:
        print(net_score)
    net_score += judgement_doubles(judge_arrays, this_color)
    if willprint:
        print(net_score)
    chessboard[point[0]][point[1]] *= -1
    if willprint:
        print(net_score)
    this_color *= -1
    if willprint:
        print(net_score)
    net_score += judgement_live_five(judge_arrays, this_color)
    if willprint:
        print(net_score)
    net_score += judgement_live_four(judge_arrays, this_color)
    if willprint:
        print(net_score)
    multiply_four_and_three_other = judgement_multiply_live_jump_four_or_three(judge_arrays, this_color)
    if willprint:
        print(multiply_four_and_three_other)
    net_score += multiply_four_and_three_other[0]
    if willprint:
        print(net_score)
    net_score += judgement_dead_four_three_two(judge_arrays, this_color)
    if willprint:
        print(net_score)
    net_score += judgement_doubles(judge_arrays, this_color)
    if willprint:
        print(net_score)
    chessboard[point[0]][point[1]] *= -1
    if multiply_four_and_three_me[1] >= 2:
        net_score += 1145
        return net_score
    elif multiply_four_and_three_other[1] >= 2:
        net_score -= 800
        return net_score
    elif multiply_four_and_three_me[1] == 1 and multiply_four_and_three_me[2] >= 1:
        net_score += 500
        return net_score
    elif multiply_four_and_three_other[1] == 1 and multiply_four_and_three_other[2] >= 1:
        net_score -= 300
        return net_score
    elif multiply_four_and_three_me[2] >= 2:
        net_score += 200
        return net_score
    elif multiply_four_and_three_other[2] >= 2:
        net_score -= 100
        return net_score
    if willprint:
        print(net_score)
        print("--------------------")
    return net_score
def get_arrays(chessboard):
    notidx = np.where(chessboard != COLOR_NONE)
    min = 0
    max = 14
    align = []
    align_row = []
    align_column = []
    align_dig_pos = []
    align_dig_neg = []
    # 切片进去的只有索引
    for i in range(min, max+1):
        align_row.append(chessboard[..., i][min:max+1])
    for i in range(min, max+1):
        align_column.append(chessboard[i, ...][min:max+1])
    temp_csc = np.fliplr(chessboard)
    for i in range(-10, 0, 1):
        align_dig_pos.append(chessboard.diagonal(offset = i))
        align_dig_neg.append(temp_csc.diagonal(offset = i))
    align_dig_pos.append(chessboard.diagonal(offset = 0))
    align.dig_net.append(chessboard.diagonal(offset = 0))
    for i in range(0, 10, 1):
        align_dig_pos.append(chessboard.diagonal(offset = i))
        align_dig_neg.append(temp_csc.diagonal(offset=i))
    align.append(align_row)
    align.append(align_column)
    align.append(align_dig_pos)
    align.append(align_dig_neg)
    return align


# 活2 眠2 活2眠2 双活二
def judgement_doubles(align,color):
    net_score = 0
    multiply_live_two = 0
    multiply_sleep_two = 0
    for i in align:
        if len(i) < 5:
            continue
        for j in range(0, len(i)-4):
            # 活二 1
            if i[j] == 0 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color and i[j+4] == 0:
                net_score += 5
                multiply_live_two += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j+4] == 0:
                net_score += 5
                multiply_live_two += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j+4] == 0:
                net_score += 5
                multiply_live_two += 1
            # 眠二 1
            if i[j] == color and i[j + 1] == 0 and i[j + 2] == 0 and i[j + 3] == color and i[j+4] == color:
                net_score += 3
                multiply_sleep_two += 1
        if len(i) < 6:
            continue
        for j in range(0, len(i) - 5):
            # 活二 2
            if i[j] == 0 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0:
                net_score += 5
                multiply_live_two += 1
            # 眠二 2
            if i[j] == 0 and i[j + 1] == 0 and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == 0 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0:
                net_score += 3
                multiply_sleep_two += 1
        if len(i) < 7:
            continue
        for j in range(0, len(i) - 6):
            # 眠二 3
            if i[j] == color * -1 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0 and i[j+6] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0and i[j + 5] == 0 and i[j+6] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == 0 and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0 and i[j+6] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
    if multiply_live_two > 2:
        net_score += 50 * multiply_live_two
    elif multiply_live_two > 1 and multiply_sleep_two > 1:
        net_score += (multiply_sleep_two + multiply_live_two) * 5
    return net_score


# 眠三
'''
def judgement_sleep_three(align, color):
    net_score = 0
    for i in align:
        if len(i) < 5:
            continue
        for j in range(0, len(i) - 4):
            if i[j] == color  and i[j + 1] == 0 and i[j + 2] == 0 and i[j + 3] == color and i[j+4] == color:
                net_score += 51
            elif i[j] == color  and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] ==  0 and i[j+4] == color:
                net_score += 51
            elif i[j] == color  and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] ==  0 and i[j+4] == color:
                net_score += 51
        if len(i) < 6:
            continue
        for j in range(0, len(i) - 5):
            if i[j] == 0 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color* -1:
                net_score += 51
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 51
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color* -1:
                net_score += 51
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0:
                net_score += 51
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == color* -1:
                net_score += 51
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0:
                net_score += 51
        if len(i) < 7:
            continue
        for j in range(0,len(i) - 6):
            if i[j] == color * -1 and i[j + 1] == 0and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0 and i[j+6] == color * -1:
                net_score += 51
'''


# 死四 三 二
def judgement_dead_four_three_two(align, color):
    net_score = 0
    for i in align:
        if len(i) < 4:
            continue
        for j in range(0, len(i) - 3):
            if i[j] == color * -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color * -1:
                net_score -= 5
        if len(i) < 5:
            continue
        for j in range(0, len(i) - 4):
            if i[j] == color * -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j+4] == color * -1:
                net_score -= 10
        if len(i) < 6:
            continue
        for j in range(0, len(i) - 5):
            if i[j] == color * -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color* -1:
                net_score -= 15
    return net_score


# Get the array
# third function
def judgement_live_five(align, color):
    net_score = 0
    for i in align:
        if len(i) < 5:
            continue
        for j in range(0, len(i)-4):
            if i[j] == color and i[j+1] == color and i[j+2] == color and i[j+3] == color and i[j+4] == color:
                net_score += 1145141
    return net_score


# 活四
def judgement_live_four(align, color):
    net_score = 0
    # print(len(align))
    for i in align:
        # print(i)
        if len(i) < 6:
            continue
        for j in range(0, len(i)-5):
            if i[j] == 0 and i[j+1] == color and i[j+2] == color and i[j+3] == color and i[j+4] == color and i[j+5] == 0:
                net_score += 114514
    # print(net_score)
    return net_score


# 解决 冲四,活三,眠三,双冲四,双活三,冲四活三,活三眠三
def judgement_multiply_live_jump_four_or_three(align, color,willreturn = False):
    net_score = 0
    multiply_four = 0
    multiply_three = 0
    multiply_sleep_three = 0

    for i in align:
        if len(i) < 5:
            continue
        for j in range(0, len(i)-4):
            # 冲四 1
            if i[j] == color and i[j+1] == 0 and i[j+2] == color and i[j+3] == color and i[j+4] == color:
                net_score += 1000
                multiply_four += 1
            elif i[j] == color and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color:
                net_score += 1000
                multiply_four += 1
            elif i[j] == color and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color:
                net_score += 1000
                multiply_four += 1
            # 眠三 1
            if i[j] == color  and i[j + 1] == 0 and i[j + 2] == 0 and i[j + 3] == color and i[j+4] == color:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color  and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == 0 and i[j+4] == color:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color  and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == 0 and i[j+4] == color:
                net_score += 51
                multiply_sleep_three += 1
            # 活三 1
            if i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0:
                net_score += 200
                multiply_three += 1
        if len(i) < 6:
            continue
        for j in range(0, len(i)-5):
            # 冲四 2
            if i[j] == 0 and i[j+1] == color and i[j+2] == color and i[j+3] == color and i[j+4] == color and i[j+5] == -1*color:
                net_score += 1000
                multiply_four += 1
            elif i[j+5] == 0 and i[j+1] == color and i[j+2] == color and i[j+3] == color and i[j+4] == color and i[j] == -1*color:
                net_score += 1000
                multiply_four += 1
            # 活三 2

            #elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0 and i[j + 5] == 0:
            #   net_score += 200
            #    multiply_three += 1
            if i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0:
                net_score += 200
                multiply_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0  and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0:
                net_score += 200
                multiply_three += 1
            # 眠三 2
            if i[j] == 0 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color * -1:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color * -1:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == color * -1:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0:
                net_score += 51
                multiply_sleep_three += 1
        if len(i) < 7:
            continue
        for j in range(0,len(i) - 6):
            if i[j] == color * -1 and i[j + 1] == 0and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0 and i[j+6] == color * -1:
                net_score += 51
                multiply_sleep_three += 1
    if multiply_four >= 2 or (multiply_three >= 1 and multiply_four >= 1) or multiply_three >= 2:
        net_score += 5141 * (multiply_three + multiply_four)
    elif multiply_three >= 1 and multiply_sleep_three >= 1:
        net_score += 514 * (multiply_three + multiply_sleep_three)
    return net_score, multiply_four, multiply_three, multiply_sleep_three


'''if multiply_four >= 2 or (multiply_three >= 1 and multiply_four >= 1) or multiply_three >= 2:
        net_score = 11451 * ( (multiply_three + multiply_three) /2)
    elif multiply_three  >= 1 and multiply_sleep_three >= 1:
    net_score = 1145 *( (multiply_three + multiply_sleep_three) /2)
    return net_score 
'''


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
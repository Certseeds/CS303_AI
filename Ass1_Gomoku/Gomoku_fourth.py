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
        numbers = [0]*len(idx)
        max_score = 0
        max_order = 0
        alpha = -INFINITE
        beta = INFINITE
        times = time.time()
        arrays_chessboard = get_arrays(chessboard)
        for i in range(0, len(idx)):
            print("{} finished".format(idx[i]))
            print(time.time() - times)
            idx_used.remove(idx[i])
            numbers[i] = self.alpha_beta_decides(chessboard, idx_used, arrays_chessboard, idx[i], 2, alpha, beta, self.color)
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

    def alpha_beta_decides(self, chessboard, idxs, arrays_chessboard, point, depth, alpha, beta, full_color):
        #print(depth)
        chessboard[point[0]][point[1]] = full_color
        if depth <= 0:
            willreturn = judgement_grade(chessboard, point, arrays_chessboard)
            chessboard[point[0]][point[1]] = 0
            return willreturn
        idxs_used = idxs.copy()
        if full_color == self.color:
            value = -INFINITE
            for i in range(len(idxs)):
                idxs_used.remove(idxs[i])
                value = max(value, self.alpha_beta_decides(chessboard, idxs_used,arrays_chessboard, idxs[i], depth-1, alpha, beta, full_color * -1))
                idxs_used.append(idxs[i])
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
        else:
            value = INFINITE
            for i in range(len(idxs)):
                idxs_used.remove(idxs[i])
                value = min(value, self.alpha_beta_decides(chessboard, idxs_used, arrays_chessboard, idxs[i], depth-1, alpha, beta, full_color * -1))
                idxs_used.append(idxs[i])
                beta = min(beta, value)
                if alpha >= beta:
                    break
        chessboard[point[0]][point[1]] = 0
        return value


def judgement_grade(chessboard, point, arrays_chessboard, willprint = False):
    this_color = chessboard[point[0]][point[1]]
    net_score = 98-(point[0]-7)**2 - (point[1]-7)**2
    net_score += judgement_live_five(arrays_chessboard, this_color)
    net_score += judgement_live_four(arrays_chessboard, this_color)
    multiply_four_and_three_me = judgement_multiply_live_jump_four_or_three(arrays_chessboard, this_color)
    net_score += multiply_four_and_three_me[0]
    net_score += judgement_dead_four_three_two(arrays_chessboard, this_color)
    net_score += judgement_doubles(arrays_chessboard, this_color)
    chessboard[point[0]][point[1]] *= -1
    this_color *= -1
    net_score += judgement_live_five(arrays_chessboard, this_color)
    net_score += judgement_live_four(arrays_chessboard, this_color)
    multiply_four_and_three_other = judgement_multiply_live_jump_four_or_three(arrays_chessboard, this_color)
    net_score += multiply_four_and_three_other[0]
    net_score += judgement_dead_four_three_two(arrays_chessboard, this_color)
    net_score += judgement_doubles(arrays_chessboard, this_color)
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
    return net_score

# it will just run once
def get_arrays(chessboard):
    notidx = np.where(chessboard != COLOR_NONE)
    length = 2
    xmin = max(0, min(notidx[0]) - length)
    xmax = min(max(notidx[0]) + length, 14)
    ymin = max(0, min(notidx[1]) - length)
    ymax = min(max(notidx[1]) + length, 14)
    align = []
    # 切片进去的只有索引
    for i in range(ymin, ymax+1):
        row2 = chessboard[..., i][xmin:xmax+1]
        align.append(row2)
    for i in range(xmin, xmax+1):
        column2 = chessboard[i, ...][ymin:ymax+1]
        align.append(column2)
    temp_csc = np.fliplr(chessboard)
    for i in range(10):
        sec2 = chessboard.diagonal(offset=i)
        sec3 = chessboard.diagonal(offset=i*-1)
        csc2 = temp_csc.diagonal(offset=i)
        csc3 = temp_csc.diagonal(offset=i*-1)
        align.append(sec2)
        align.append(sec3)
        align.append(csc2)
        align.append(csc3)
    align.append(chessboard.diagonal(0))
    align.append(temp_csc.diagonal(0))
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
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

    def go(self, chessboard):
        # print(chessboard)
        #chessboard = np.asanyarray(chessboar)
        # Write your algorithm here25
        # #Here is the simplest sample:Randomdecision
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
        # print(len(idx))
        for i in range(0,len(idx)):
            numbers[i] = self.judgement_grade(chessboard,idx[i])
            if max_score < numbers[i]:
                max_score = numbers[i]
                max_order = i
                self.candidate_list.append(numbers[i])
        new_pos =  idx[max_order]
        #print(new_pos)
        #print("chose this one")
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        self.candidate_list.append(new_pos)
        print(time.time() - times)
        return
    # first function
    def judgement_location(self, chessboard):
        notidx = np.where(chessboard != COLOR_NONE)
        willdelete = []
        # print(notidx[0])#print(notidx[1])
        xmin = max(0, min(notidx[0]) - 4)
        xmax = min(max(notidx[0]) + 4, self.chessboard_size)
        ymin = max(0, min(notidx[1]) - 4)
        ymax = min(max(notidx[1]) + 4, self.chessboard_size)
        # print(xmin)#print(xmax)#print(ymin)#print(ymax)
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for i in idx:
            if i[0] < xmin or i[0] > xmax or i[1] < ymin or i[1] > ymax:
                willdelete.append(i)
        for i in willdelete:
            idx.remove(i)
        return idx

    def judgement_grade(self, chessboard, point):
        csbd = chessboard.copy()
        csbd[point[0]][point[1]] = self.color
        net_score = abs(point[0]-7) + abs(point[1]-7)
        if can_put_stone(csbd, point):
            return 0
        # if return in he_re ,it means it can not be put
        judge_arrays = get_arrays(csbd, point)
        # if point[0] == 4 and point[1] == 14 :
        #   for i in judge_arrays:
        #        print(i)
        net_score += judgement_live_five(judge_arrays, self.color)
        net_score += judgement_live_four(judge_arrays, self.color)
        multiply_four_and_three_me = judgement_multiply_live_jump_four_or_three(judge_arrays, self.color)
        net_score += multiply_four_and_three_me[0]
        net_score += judgement_dead_four_three_two(judge_arrays, self.color)
        net_score += judgement_doubles(judge_arrays, self.color)
        csbd[point[0]][point[1]] = self.color * -1
        judge_arrays_2 = get_arrays(csbd, point)
        # if point[0] == 4 and point[1] == 14 :
        #   for i in judge_arrays_2:
        #       print(i)
        net_score += judgement_live_five(judge_arrays_2, self.color * -1)
        net_score += judgement_live_four(judge_arrays_2, self.color * -1)
        multiply_four_and_three_other = judgement_multiply_live_jump_four_or_three(judge_arrays, self.color * -1)
        net_score += multiply_four_and_three_other[0]
        net_score += judgement_dead_four_three_two(judge_arrays_2, self.color * -1)
        net_score += judgement_doubles(judge_arrays_2, self.color * -1)
        return net_score


def get_arrays(chessboard,point):
    Align = []
    x = point[0]
    y = point[1]
    length = 5
    xmin = max(point[0] - length,0)
    xmax = min(point[0] + length,14)
    ymin = max(point[1] - length,0)
    ymax = min(point[1] + length,14)
    rowN = []
    columnN =[]
    secN= []
    cscN = []
    for i in range(xmin,xmax+1):
        rowN.append(chessboard[i][y])
    for i in range(ymin,ymax+1):
        columnN.append(chessboard[x][i])
    # for i in range(1,min(x-xmin,ymax - y)+1):
    for i in range(min(x-xmin,ymax-y),0,-1):
        secN.append(chessboard[x-i][y+i])
    secN.append(chessboard[x][y])
    for i in range(1,min(xmax - x,y-ymin)+1):
        secN.append(chessboard[x+i][y-i])

    # for i in range(1,min(x-xmin,y-ymin)):
    for i in range(min(x - xmin, y - ymin),0,-1):
        cscN.append(chessboard[x-i][y-i])
    cscN.append(chessboard[x][y])
    for i in range(1,min(xmax-x,ymax-y)):
        cscN.append(chessboard[x+i][y+i])

    Align.append(np.asarray(rowN))
    Align.append(np.asarray(columnN))
    Align.append(np.asarray(secN))
    Align.append(np.asarray(cscN))
    return Align

# 活2 眠2 活2眠2 双活二
def judgement_doubles(align,color):
    net_score = 0
    multiply_live_two = 0
    multiply_sleep_two = 0
    for i in align:
        if len(i) < 5:
            continue
        for j in range(0,len(i)-4):
            #活二 1
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
            if  i[j] == color and i[j + 1] == 0 and i[j + 2] == 0 and i[j + 3] == color and i[j+4] == color:
                net_score += 3
                multiply_sleep_two += 1
        if len(i) < 6:
            continue
        for j in range(0,len(i) -5):
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
            elif i[j] == color * -1 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] ==  color and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] ==  0 and i[j + 4] ==  color and i[j + 5] == 0:
                net_score += 3
                multiply_sleep_two += 1
        if len(i) < 7:
            continue
        for j in range(0,len(i)-6):
            # 眠二 3
            if i[j] == color * -1 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0 and i[j+6] == color * -1:
                net_score += 3
                multiply_sleep_two += 1
            elif i[j] == color * -1 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color  and i[j + 4] == 0and i[j + 5] == 0 and i[j+6] == color * -1:
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


#活四
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
def judgement_multiply_live_jump_four_or_three(align, color):
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
            elif i[j] == color  and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] ==  0 and i[j+4] == color:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color  and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] ==  0 and i[j+4] == color:
                net_score += 51
                multiply_sleep_three += 1
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
            # 活三
            if i[j] == 0 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == 0:
                net_score += 200
                multiply_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 200
                multiply_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] ==  0 and i[j + 4] ==  color and i[j + 5] == 0:
                net_score += 200
                multiply_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0  and i[j + 3] == color and i[j + 4] ==  color and i[j + 5] == 0:
                net_score += 200
                multiply_three += 1
            # 眠三 2
            if i[j] == 0 and i[j + 1] == 0 and i[j + 2] == color and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color* -1:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == color and i[j + 4] == 0 and i[j + 5] == 0:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == 0 and i[j + 3] == color and i[j + 4] == color and i[j + 5] == color* -1:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == color* -1 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == 0:
                net_score += 51
                multiply_sleep_three += 1
            elif i[j] == 0 and i[j + 1] == color and i[j + 2] == color and i[j + 3] == 0 and i[j + 4] == color and i[j + 5] == color* -1:
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
        net_score = 11451 * ((multiply_three + multiply_three) / 2)
    elif multiply_three >= 1 and multiply_sleep_three >= 1:
        net_score = 1145 * ((multiply_three + multiply_sleep_three) / 2)
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
    #return True代表不行,其余可以
    x = point[0]
    y = point[1]
    # 首先 chessboard[x][y] != 0,其次,不能下的情况,只有四周全为-1*chessboard,才不能,即为true
    # 也就是说,可以将其huanwei [x][y] + [x][y+1] == 0
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
    elif (point[0] == 0 and point[1] != 0 and point[1] != 14):
        return (chessboard[0][y] + chessboard[0][y - 1] == 0) and (chessboard[0][y] + chessboard[0][y + 1] == 0) and (
                chessboard[0][y] + chessboard[1][y] == 0) and (chessboard[0][y] + chessboard[1][y - 1] == 0) and (
                       chessboard[0][y] + chessboard[0][y + 1] == 0)
    elif (point[0] == 14 and point[1] != 0 and point[1] != 14):
        return (chessboard[14][y] + chessboard[14][y - 1] == 0) and (
                    chessboard[14][y] + chessboard[14][y + 1] == 0) and (
                       chessboard[14][y] + chessboard[13][y] == 0) and (
                           chessboard[14][y] + chessboard[13][y - 1] == 0) and (
                       chessboard[14][y] + chessboard[13][y + 1] == 0)
    elif (point[1] == 0 and point[0] != 0 and point[0] != 14):
        return (chessboard[x][0] + chessboard[x - 1][0] == 0) and (chessboard[x][0] + chessboard[x + 1][0] == 0) and (
                chessboard[x][0] + chessboard[x][1] == 0) and (chessboard[x][0] + chessboard[x - 1][0] == 0) and (
                       chessboard[x][0] + chessboard[x + 1][1] == 0)
    elif (point[1] == 14 and point[0] != 0 and point[0] != 14):
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
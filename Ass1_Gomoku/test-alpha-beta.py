import numpy as np
import random
import time

COLOR_BLACK = 1
COLOR_WHITE = -1
COLOR_NONE = 0
INFINITE = 1145141919
random.seed(114514)

class AI(object):
    def __init__(self,node_array, color, ):
        self.node_array = node_array
        self.color = color
    def go(self,node_array,color):
        max_value = -114514
        node = 0
        for i in range(len(node_array)):
            node_array[i] = color
            value = get_max(node_array, color)
            if max_value < value:
                max_value = value
                node = i
            node_array[i] = 0
        return node


def get_max(node_array,color):
    for i in [0,1,3,4]:
        if node_array[i] == node_array[2]:
            return 1* color
    if node_array[0] != 0 and node_array[1] != 0 and node_array[2] != 0 and node_array[3] != 0 and node_array[4] != 0:
        return 0
    max_value = -114514
    list = []
    for i in range(len(node_array)):
        if node_array[i] != 0:
            list.append(i)
    for i in list:
        node_array[i] = color
        value = get_min(node_array, -color)
        if max_value < value:
            max_value = value
        node_array[i] = 0
    return  max_value


def get_min(node_array,color):
    for i in [0, 1, 3, 4]:
        if node_array[i] == node_array[2]:
            return 1 * color
    if node_array[0] != 0 and node_array[1] != 0 and node_array[2] != 0 and node_array[3] != 0 and node_array[4] != 0:
        return 0
    min_value = 114514
    list = []
    for i in range(len(node_array)):
        if node_array[i] != 0:
            list.append(i)
    return min_value

def judgement_grade(chessboard, point, arrays_chessboard, willprint = False):

    return net_score


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
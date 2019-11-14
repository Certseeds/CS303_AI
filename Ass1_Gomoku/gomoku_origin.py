import numpy as np
import random
import re
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
        self.color= color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_listas your decision .
        self.candidate_list = []
        # The input is current chessboard
    def go(self,chessboard):
        #Write your algorithm here25
        # #Here is the simplest sample:Randomdecision
        self.candidate_list.clear()
        #idx = np.where(chessboard == COLOR_NONE)
        #此处应该会返回一个[2][x]的array,[0][a] x 坐标 [1][a] y坐标
        #idx = list(zip(idx[0], idx[1]))
        #形成一个array ,元素为tuple(x,y)
        idx = judgementLocation(chessboard)
        #筛选出有意义的部分
        pos_idx = random.randint(0, len(idx) - 1)

        #随机选择一个
        new_pos = idx[pos_idx]
        #找到了
        # ==============Find new pos========================================
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        self.candidate_list.append(new_pos)

    def judgementGrade(self,chessboard, point):
        csbd = chessboard.copy()
        csbd[point[0]][point[1]] =self.color
        thisColor = str(self.color)
        otherColor = str(self.color*-1)
        netScore = abs(point[0]-7) + abs(point[1]-7)
        if canPutStone(csbd,point):
            return 0
        judgeStrings = getStrings(csbd,point)
        # into Five
        intoFive = thisColor* 5
        for i in judgeStrings:
            if re.search(i,intoFive) != None:
                netScore += INFINITE
                return netScore
        #into Five finish
        #Live four
        liveFour = "0"+thisColor*4+"0"
        for i in judgeStrings:
            if re.search(i,liveFour) != None:
                netScore += 100000
                return netScore
        #live four finish
        #Flush Four
        flushFour_1 = otherColor+thisColor*4+"0"
        flushFour_2 = "0"+thisColor*4+otherColor
        for i in judgeStrings:
            if (re.search(i, flushFour_1) != None) or (re.search(i,flushFour_2)!= None):
                netScore += 10000
        #Flush Four finish
        #Flush Jump Four
        flushJumpFour_1 =otherColor+ thisColor+"0"+thisColor*3
        flushJumpFour_2 =otherColor + thisColor*2 + "0"+thisColor*2
        flushJumpFour_3 = otherColor + thisColor*3 + "0"+thisColor
        flushJumpFour_4 = thisColor+"0"+thisColor*3 + otherColor
        flushJumpFour_5 = thisColor*2+"0"+thisColor*2+otherColor
        flushJumpFour_6 = thisColor*3 + "0" + thisColor+otherColor
        for i in judgeStrings:
            if (re.search(i,flushJumpFour_1)!= None) or (re.search(i,flushJumpFour_2)!= None)or(
                re.search(i, flushJumpFour_3)!= None) or (re.search(i, flushJumpFour_4)!= None)or(
                    re.search(i, flushJumpFour_5)!= None) or (re.search(i, flushJumpFour_6)!= None):
                netScore+=5000
        #Flush jump Four finish
        #Live Three
        liveThree_1 = "0"+thisColor*3+"0"
        liveJumpThree_2 = "0"+thisColor*2+"0"+thisColor+"0"
        liveJumpThree_3 = "0" + thisColor + "0" + thisColor*2 + "0"
        for i in judgeStrings:
            if (re.search(i,liveThree_1)!= None) or (re.search(i,liveJumpThree_2)!= None) or (re.search(i,liveJumpThree_3)!=None):
                netScore += 100
        #Live Three Finish
#Get the string of the nodes
def getStrings(chessboard,point):
    Align = []
    x = point[0]
    y = point[1]
    xmin = max(point[0]-4,0)
    xmax = min(point[0]+4.14)
    ymin = max(point[1]-4,0)
    ymax = min(point[1] + 4.14)
    rowN = []
    columnN =[]
    secN= []
    cscN = []
    for i in range(xmin,xmax+1):
        rowN.append(chessboard[i][y])
    for i in range(ymin,ymax+1):
        columnN.append(chessboard[x][i])
    for i in range(1,min(x-xmin,ymax - y)+1):
        secN.append(chessboard[x-i][y+i])
    secN.append(chessboard[x][y])
    for i in range(1,min(xmax - x,y-ymin)+1):
        secN.append(chessboard[x+i][y-i])
    for i in range(1,min(x-xmin,y-ymin)):
        cscN.append(chessboard[x-i][y-i])
    cscN.append(chessboard[x][y])
    for i in range(1,min(xmax-x,ymax-y)):
        cscN.append(chessboard[x+i][y+i])
    rowString = "".join(str(i) for i in rowN)
    columnString = "".join(str(i)for i in columnN)
    secString = "".join(str(i) for i in secN)
    cscString = "".join(str(i) for i in cscN)
    Align.append(rowString)
    Align.append(columnString)
    Align.append(secString)
    Align.append(cscString)
    return Align

#hard code,i dont wanna to look it
def canPutStone(chessboard, point):
    #return True代表不行,其余可以
    xplus = xminus = yplus = yminus = False
    leftup = leftdown = rightup = rightdown = False
    x = point[0]
    y = point[1]
    # 这里的True代表没有对方棋子,False代表有子,初始化为有子
    if point[0] == 0 and point[1] == 0:
        return (chessboard[0][0] != chessboard[0][1])and (chessboard[0][0] != chessboard[1][0])and (chessboard[0][0] != chessboard[1][1])
    elif point[0] == 0 and point[1] == 14 :
        return (chessboard[0][14] != chessboard[0][13]) and (chessboard[0][14] != chessboard[1][13]) and (chessboard[0][14] != chessboard[1][14])
    elif point[0] == 14 and point[1] == 0  :
        return (chessboard[14][0] != chessboard[14][1]) and (chessboard[14][0] != chessboard[13][1]) and (chessboard[14][0] != chessboard[13][0])
    elif point[0] == 14 and point[1] == 14:
        return (chessboard[14][14] != chessboard[14][13]) and (chessboard[14][14] != chessboard[13][14]) and (chessboard[14][14] != chessboard[13][13])
    elif (point[0] == 0 and point[1] != 0  and point[1] != 14):
        return (chessboard[0][y] != chessboard[0][y-1]) and (chessboard[0][y] != chessboard[0][y+1]) and (
                chessboard[0][y] != chessboard[1][y]) and (chessboard[0][y] != chessboard[1][y-1]) and (
                chessboard[0][y] != chessboard[0][y+1])
    elif (point[0] == 14 and point[1] != 0 and point[1] != 14):
        return (chessboard[14][y] != chessboard[14][y - 1]) and (chessboard[14][y] != chessboard[14][y + 1]) and (
                    chessboard[14][y] != chessboard[13][y]) and (chessboard[14][y] != chessboard[13][y - 1]) and (
                           chessboard[14][y] != chessboard[13][y + 1])
    elif (point[1] == 0 and point[0] != 0 and point[0] != 14):
        return (chessboard[x][0] != chessboard[x-1][0]) and  (chessboard[x][0] != chessboard[x+1][0]) and (
                    chessboard[x][0] != chessboard[x][1]) and (chessboard[x][0] != chessboard[x-1][0]) and (
                           chessboard[x][0] != chessboard[x+1][1])
    elif (point[1] == 14 and point[0] != 0 and point[0] != 14):
        return (chessboard[x][14] != chessboard[x - 1][14]) and (chessboard[x][14] != chessboard[x + 1][14]) and (
                chessboard[x][14] != chessboard[x][13]) and (chessboard[x][14] != chessboard[x - 1][13]) and (
                       chessboard[x][14] != chessboard[x + 1][13])
    else :
        return (chessboard[x][y] != chessboard[x-1][y]) and (chessboard[x][y] != chessboard[x+1][y]) and (
                chessboard[x][y] != chessboard[x][y + 1]) and (chessboard[x][y] != chessboard[x][y-1]) and(
                chessboard[x][y] != chessboard[x-1][y -1]) and (chessboard[x][y] != chessboard[x-1][y + 1]) and (
                chessboard[x][y] != chessboard[x+1][y -1]) and (chessboard[x][y] != chessboard[x+1][y + 1])

def judgementLocation(chessboard):
    notidx = np.where(chessboard!= COLOR_NONE)
    willdelete = []
    #print(notidx[0])#print(notidx[1])
    xmin = max(0,min(notidx[0])-4)
    xmax =  min(max(notidx[0])+4,14)
    ymin =max(0,min(notidx[1])-4)
    ymax = min(max(notidx[1])+4,14)
    #print(xmin)#print(xmax)#print(ymin)#print(ymax)
    idx = np.where(chessboard == COLOR_NONE)
    idx = list(zip(idx[0], idx[1]))
    for i in idx:
        #print("{}{}{}".format(i[0]," ",i[1]))
        if i[0] < xmin or i[0] > xmax or i[1]< ymin or i[1] > ymax :
            #print("{}{}{}{}".format(i[0]," ",i[1],"will be delete"))
            willdelete.append(i)
    for i in willdelete:
        idx.remove(i)
    return idx


z = np.zeros((15,15),dtype= np.int)
print(114514)
print(z)
for i in range(13):
    for j in range(13):
        tempRand = random.random()
        if tempRand < 0.1:
            z[i][j] = 0
        if tempRand >0.1 and tempRand < 0.9:
            z[i][j] = 0
        if tempRand > 0.9:
            z[i][j] = 0
z[7][7] = 1
print(z)
notes = judgementLocation(z)
print(notes)

x = np.ones((15,15),dtype = np.int)
x[7][7] = -1
x[7][6] = -1
print(canPutStone(x,(7,7)))

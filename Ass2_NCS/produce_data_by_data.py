import sys
import random
from float_and_bin import *
print(sys.argv[1])
jilu = open("jilu.txt",mode="a+")
jilu.writelines("this is once produce data by data\r\n")
jilu.close()
store_datas_name="store_datas_{}.txt".format(str(int(sys.argv[1])))
data = open(store_datas_name,"r+")
reads = data.read()
data.close()
datas = reads.split("\n")
matrix=[]
class longs(object):
    def __init__(self,lam,r,epoch,n,score):
        self.lam = lam
        self.r = r
        self.epoch =epoch
        self.n = n
        self.score = score
    def __cmp__(self,other):
        return cmp(self.score,other.score)
def produce_random_father():
    # fenche                
    random_numeber =random.random()
    if random_numeber > 0.9:
        return 0
    elif random_numeber>0.7:
        return random.randint(1,5)
    elif random_numeber>0.2:
        return random.randint(6,15)
    return random.randint(16,20)
def get_son(father1,father2):
    random1 = random.randint(1,21)
    random2 = random.randint(1,21)
    random3 = random.randint(1,5)
    random4 = random.randint(1,5)
    random5= random.random()
    change_number = 0
    if random5>0.20:
        change_number += 1
    elif random5 > 0.50:
        change_number += 1
    elif random5 > 0.60:
        change_number += 1
    elif random5 > 0.75:
        change_number += 1
    elif random5 > 0.90:
        change_number += 1
    elif random5 > 0.99:
        change_number += 1
    new_lam = father1.lam[0:random1] + father2.lam[random1:]
    new_r = father1.r[0:random2] + father2.r[random2:]
    new_epoch = father1.epoch[0:random3] + father2.epoch[random3:]
    new_n = father1.n[0:random4] + father2.n[random4:]
    for i in range(0,change_number,1):
        random_number2 = random.randint(0,20)
        new_lam = new_lam[0:random_number2]+("0" if new_lam[random_number2]=="1" else "1")+new_lam[random_number2+1:]
        new_r = new_r[0:random_number2]+("0" if new_r[random_number2]=="1" else "1")+new_r[random_number2+1:]
    print(new_lam,new_r,new_epoch,new_n)
    return longs(new_lam,new_r,new_epoch,new_n,0)
print(len(datas))
for j in range(len(datas)-1):
    i = datas[j]
    #print(i)
    temp = i.split(",")
    print(temp[0][9:],temp[1][4:],temp[2][8:],temp[3][4:],temp[5][7:])
    temp_long = longs(float_to_bin(float(temp[0][9:])),float_to_bin(float(temp[1][4:])),int_to_bin(int(temp[2][8:])),int_to_bin(int(temp[3][4:])),float(temp[5][7:]))
    matrix.append(temp_long)
matrix = sorted(matrix,key = lambda longs:longs.score)
for i in matrix:
    print(i.score)
result =[]
sons = []
length_of_matrix=len(matrix)
for i in range(0,30,1):
    order1=  produce_random_father()
    order2=  produce_random_father()
    father1 = matrix[order1]
    father2 = matrix[order2]
    sons.append(get_son(father1,father2))
for i in range(0,30,1):
    result.append("{} {} {} {}\r\n".format(bin_to_float(sons[i].lam),bin_to_float(sons[i].r),bin_to_int(sons[i].epoch),bin_to_int(sons[i].n)))
willbewrite = open("datas.txt","w")
for i in range(0,30,1):
    willbewrite.writelines(result[i])
willbewrite.close()

data = open(store_datas_name,"w+")
data.write("")
data.close()
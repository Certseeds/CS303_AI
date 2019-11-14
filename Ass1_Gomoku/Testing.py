import re
import numpy as np
import time
number = []
for i in range(7):
    number.append(-1)
string1 = "".join(str(i) for i in number)
print(string1)
print(type(string1))
print(re.match("-1-1-1",string1) == None)

for i in range(14,51):# 14~50
    print (i)

print(("".join(str(-1))) * 5)
print("0"+"-1"*4+"0")
print("" +str(1))
print(str(-1) * 5)
str2 = "1-1-1-10-1"
print(str2)
print(reversed(str2))
test = [1,1,1,1,1]
print(test)
test2 = np.asarray(test)
print(test2)
print(test2-1)
test3 = np.zeros(5)
print(test3)
if 2>3>4:
    print("wtf")
test4 = np.ones([3,3],dtype = int)
print(test4)
test5 = np.where(test4 != 1)
print(test5)
print(len(test5[0]))
print(1 == 1 == -1 == 1 == 1)

test6 = (1,1,4,5,14,1919)
print(test6[2])
print(test6[4])
for i in range(114,51,-1):
    print (i)
for i in range(15):
    print(i)
testing = [1,1,4,5,1,4]
print(testing[2:4] == [4,5])
test7 = np.asanyarray([[1,1,4,5,1,4],[1,9,9,1,8,1]])
queue = []
test8 = np.ones((15, 15))
test8[7][7] = -1
test8[7][8] = -1
print(np.fliplr(test8).diagonal(offset = -1))

times = time.time()
for i in range(1000):
    for j in range(5,15):
        queue.append(test8.diagonal(offset = j))
print(time.time() - times)
queue = []
times = time.time()
for i in range(1000):
    for j in range(5,15):
        temp = []
        for k in range(j):
            temp.append(test8[15-j+k][k])
        queue.append(temp)
print(time.time() - times)

queue = []
times = time.time()
for i in range(1000):
    diaboluo = np.fliplr(test8)
    for j in range(5,15):
        queue.append(diaboluo.diagonal(offset = j))
print(time.time() - times)


testing_numpy = np.zeros((13, 13), dtype = np.int8)
xmin = 1
xmax = 3
row_from = testing_numpy[2,...][xmin:xmax]
print(row_from)
testing_numpy[2][2] = -1
print(row_from)
testing_array = np.zeros((3, 3), dtype = np.int8)
for i in range(3):
    for j in range(3):
        testing_array[i][j] = 3*i+j
print(testing_array)
print(testing_array[...,2])
print(testing_array[2,...])
test_array_minus = []
for i in range(100):
    test_array_minus.append((i,i+1))

for i in range(99):
    print( test_array_minus[i])
test_array_minus.remove((1,2))
print((1,2) in test_array_minus)
slip1 = (1,2,3)
docotr = {}
docotr[slip1] = (1,2,3,4,5)
print(docotr[slip1])
counti = 4
for i in range(100,counti):
    print (i)
test_array_2 = [114514, 1919, 810, 1919, 114514]
print(test_array_2[1:3])
print(test_array_2[1:3] == [1919,810])
test_array_3 = [
    [114,514],
    [1919,810]
]
print(test_array_2[1:3] in test_array_3)
numpy_array = np.asarray(test_array_2)
print((numpy_array[1:3] == [1919,810]).all())
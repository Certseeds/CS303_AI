import random


lambad = 1 # 1-100,double
r = 0.90 # no range,double
epoch = 100 # no range, int? 
n = 10 # >10,int
stored = []
for i in range(0,50,1):
    lambad = (1 + (1 if random.random() > 0.5 else -1) * random.random())   
    epoch = random.randint(8,20)
    r = (1 + (1 if random.random() > 0.5 else -1) * random.random()) 
    n = 10 + int(random.random()*11)
    if lambad < 0:
        lambad *= -1
    if r < 0:
        r *= -1
    stored.append("{} {} {} {}\r\n".format(lambad,r,epoch,n))
# for i in stored:
    # print(i)
datas=open("datas.txt","w")
for i in stored:
    datas.writelines(i)
datas.close()
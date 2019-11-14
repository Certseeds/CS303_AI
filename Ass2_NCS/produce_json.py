import sys
print(sys.argv[1])
canshu = ["lambda","r","epoch","n"]
juti = [0,0,0,0]
file0 = open("datas.txt",mode='r')
data = file0.read()
datas=data.split('\n')
line_number = 2
for i in range(0,4,1):
    juti[i] = datas[int(sys.argv[1])].split(" ")[i]

for i in juti:
    print(i)
file1 = open("parameter.json",mode='w')
list_1 = []

for i in range(len(canshu)):
    list_1.append("\"{}\":{}{}\r\n".format(canshu[i],juti[i],"," if i != len(canshu)-1 else ""))

willreturn = "{\r\n"
for i in range(len(list_1)):
    willreturn += list_1[i]
willreturn += "}"
file1.write(willreturn)
file1.close()

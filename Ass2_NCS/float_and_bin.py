def float_to_bin(number,jingdu = 21):
    willreturn = ""
    for i in range(0,jingdu,1):
        if number >= 1:
            willreturn += "1"
            number -=1
        else :
            willreturn += "0"
        number *= 2
    return willreturn
def int_to_bin(number,jingdu = 5):
    willreturn = ""
    for i in range(0,jingdu,1):
        willreturn = str(number %2) +willreturn
        number //=2
    return willreturn

def bin_to_float(number,jingdu=21):
    willreturn = 0
    count = 1
    for i in range(0,21,1):
        if number[i] == "1":
            willreturn += count
        count /=2
    return float(willreturn)

def bin_to_int(number,jingdu = 5):
    willreturn = 0
    count = 16
    for i in range(0,5,1):
        if number[i] == "1":
            willreturn += count
        count /=2
    return int(willreturn) 
print(bin_to_float(float_to_bin(1.1154487)))
print(int_to_bin(29))
print(bin_to_int(int_to_bin(29)))
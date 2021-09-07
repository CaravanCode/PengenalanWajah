import os

x = []
file_in = open('output/Disirvan_20luxMSR.txt', 'r')
#for y in file_in.read().split('\n'):
for y in file_in.readlines():
    print(y)
    x.append(float(y))



def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return avg

print("Rata-rata: "+str(cal_average(x)))


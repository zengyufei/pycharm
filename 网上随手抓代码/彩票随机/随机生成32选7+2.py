import random

temp = [i + 1 for i in range(32)]
random.shuffle(temp)
i = 0
list = []
while i < 9:
    list.append(temp[i])
    i = i + 1
list.sort()
print('\033[0;31;;1m')
print(*list[0:7], end="")
print('\033[0;34;;1m', end=" ")
print(*list[-2::])

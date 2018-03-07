str1 = "helloworld"

print(str1[0], str1[1], str1[2], str1[3])  # h e l l
print(str1[2:3])  # 从 2 开始到 3，不包括 2，即3 结果 l
print(str1[5:9])  # 从 5 开始到 9，不包括 5，即6789 结果 worl
print("----------------------")
rindex = str1.rindex("w")
print("rindex = ", rindex)
print(str1[rindex])
print(str1[rindex:9])  # 从 rindex 开始到 9，不包括 rindex，即 for i in range(9 - rindex): print(i + rindex + 1)  结果 for i in range(9 - rindex): print(i + rindex + 1, " = ", str1[i + rindex])
print(str1[rindex:-1])
print(str1[-5::])



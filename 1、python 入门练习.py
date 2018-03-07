# python 入门练习

# 1、变量
print(
    "------------------------------------------------------1、变量-------------------------------------------------------")
one = 1.5
print("浮点数据类型变量：", one) # 1.5

one, two = 1, 2
print("同时分别赋值：", one, two) # 1 2

one = two = 3
print("赋相同值：", one, two) # 3 3

#### 字符串
str = "测试"
print("输出字符串：", str) # 测试

str = '''(测试
多行
文本)
'''
print("多行文字输出：", str)

#### 布尔值
isTrue = True
isFalse = False
print("布尔值类型输出：", isTrue, isFalse) # True False

# 2、流程控制
print(
    "------------------------------------------------------2、流程控制-------------------------------------------------------")

#### 单纯 if
if True:
    print("true 布尔类型 true 的 if 输出")

if 2 > 1:
    print("2 > 1 的逻辑条件判断的 if 输出 ")

#### if-else
if 1 > 2:
    pass
else:
    print("if-else 输出")

#### if-elif-else
if 1 > 2:
    pass
elif 2 > 1:
    print("if-elif-else 输出")
else:
    pass

# 3、迭代循环
print(
    "------------------------------------------------------3、迭代循环-------------------------------------------------------")

print("-----------------------------------while 循环----------------------------------")
#### while 循环
num = 1
while num <= 10:
    print("迭代循环输出：", num) # 1 2 3 4 5 6 7 8 9 10
    num += 1

stop_condition = True
while stop_condition:
    print("迭代循环退出条件")
    stop_condition = False

print("-----------------------------------for 循环----------------------------------")
#### for 循环
######## 从 1 循环到 10
for i in range(1, 11):
    print("从 1 循环到 10：", i) # 1 2 3 4 5 6 7 8 9 10

######## 从有限集合循环
for j in 2, 4, 6, 8, 10:
    print("从有限集合循环 1：", j) # 2 4 6 8 10

for k in [1, 3, 5, 7, 9]:
    print("从有限集合循环 2：", k) # 1 3 5 7 9

# 4、List 列表
print(
    "------------------------------------------------------4、List 列表-------------------------------------------------------")
newList = [
    1,
    "two",
    "three",
    4,
    True,
]

print("List 列表输出：", newList[0]) # 1
print("List 列表输出：", newList[1]) # two
print("List 列表输出：", newList[2]) # three
print("List 列表输出：", newList[3]) # 4
print("List 列表输出：", newList[4]) # True

appendList = newList.append("append last List")
print("List 列表输出：", newList[5]) # append last List

# 5、Dictionary 字典
print(
    "------------------------------------------------------5、Dictionary 字典-------------------------------------------------------")

kv = {
    "1": "zengyufei",
    2: "no",
    "age": 27
}

print("my name is %s" % (kv["1"])) # zengyufei
print("age 35 ? %s" % (kv[2])) # no
print("How age ? %i" % (kv["age"])) # 27

# 6、迭代 Iteration
print(
    "------------------------------------------------------6、迭代 Iteration-------------------------------------------------------")

for item in newList:
    print("List 迭代：", item)

for k, v in kv.items():
    print("字典迭代：%s --> %s" % (k, v))

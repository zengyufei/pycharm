import re  # 正则包

# python 基本数据类型练习

# 1、使用内建函数进行强制类型转换
print(
    "------------------------------------------------------1、使用内建函数进行强制类型转换-------------------------------------------------------")

str1 = 7
str2 = 1.5

strToInt = int(str1)
strToFloat = float(str2)
print("int(str) = ", type(strToInt))  # <class 'int'>
print("float(str) = ", type(strToFloat))  # <class 'float'>

numb = 99
floatNumb = 99.99

intToStr = str(numb)
floatToStr = str(floatNumb)
print("str(int) = ", type(intToStr))  # <class 'str'>
print("str(float) = ", type(floatToStr))  # <class 'str'>

# 2、数值类型
print(
    "------------------------------------------------------2、数值类型-------------------------------------------------------")

x = 3
print("x 的类型为： ", type(x))  # <class 'int'>
print("x 的值： ", x)  # 3
print("x + 1, x - 1, x * 2, x / 3, x ** 2 = ", x + 1, x - 1, x * 2, x / 3, x ** 2)

y = 3
y += 1
print("y 的值： ", y)  # 4

z = 3
z *= 2
print("z 的值： ", z)  # 6

# 3、布尔类型
print(
    "------------------------------------------------------3、布尔类型-------------------------------------------------------")

t = True
f = False

print("t 的类型为： ", type(t))  # <class 'bool'>
print("t && f = ", t and f)  # False， 相当于 java 的 &&
print("t || f = ", t or f)  # True， 相当于 java 的 ||
print("!t = ", not t, "!f = ", not f)  # False， True， 相当于 java 的非！
print("t != f 的结果为： ", t != f)  # True，异或

# 4、字符串类型
print(
    "------------------------------------------------------4、字符串类型-------------------------------------------------------")

#### 字符串支持分片、模板字符串。
str1 = "hello world!"

#### 从左到右起始位置为 0，从右往左起始位置为 -1。
print("str1[1] = ", str1[1])  # e
print("str1[-1] = ", str1[-1])  # !
print("str1[0:1] = ", str1[0:1])  # h
print("str1[1:5] = ", str1[1:5])  # ello
print("str1[-5:-1] = ", str1[-5:-1])  # orld

print('str1.find("ll") = ', str1.find("ll"))  # 2
print('str1.find(",") = ', str1.find(","))  # -1
print('str1.index("ll") = ', str1.index("ll"))  # 2
try:
    print(str1.index(","))  # error
except:
    pass

print("%s %s" % ("hello", "mary"))  # hello mary
print("hi {0}, my name is {1}".format("mary", "zengyufei"))  # hi mary, my name is zengyufei

#### 长度
print(len("hello"))  # 5
print("xxxlll".count("x"))  # 3

#### 替换合并插入转换
print("a-b-c".replace("-", ""))  # abc
arr = ["a", "b", "c"]
print(", ".join(arr))  # a, b, c
print("a-b-c".split("-"))  # ['a', 'b', 'c']

print("ABc".lower())  # abc
print("ABc".upper())  # ABC

print("abc".islower())  # True
print("aBc".islower())  # False

print("Abc".title())  # Abc
print("abc".title())  # Abc

#### 去除空格
print("  abc".lstrip())  # abc
print("abc    ".rstrip())  # abc
print("     abc     ".strip())  # abc

#### 去除特殊符号
print(re.sub('[^A-Za-z0-9]+', '', "jk2*)(!][])"))  # jk2


#### 在字符串中查找
def findYu(findStr):
    if findStr in "zengyufei":
        print(findStr, " 在 zengyufei 之中")
    elif findStr not in "zengyufei":
        print(findStr, " 不在 zengyufei 之中")


findYu("yu")
findYu("haha")


def findIs(findStr):
    str = "my name is zengyufei"
    if str.find(findStr) == -1:
        print("找不到 ", findStr)
    else:
        print("找到 ", findStr)


findIs("is")
findIs("haha")



import os
from time import sleep


def printConsole(title, content):
    print(title)
    print(content)


def writeFile(fileName, fileContent, dir=""):
    if not os.path.exists(dir):
        os.mkdir(dir)
        if not os.path.isdir(dir):
            os.remove(dir)
    f = open(dir + fileName + ".txt", "w", encoding="UTF-8")
    f.write(str(fileName) + "\n")
    f.write(str(fileContent) + "\n")
    f.close()


def readFile(fileName):
    f = open(fileName + ".txt", "r", encoding="UTF-8")
    lines = f.readlines()
    for line in lines:
        print(line)


def writeAndSleepReaderTempFile(fileName, fileContent):
    f = open("temp.txt", "w", encoding="UTF-8")
    f.write(str(fileName) + "\n")
    f.write(str(fileContent) + "\n")
    f.close()
    f = open("temp.txt", "r", encoding="UTF-8")
    lines = f.readlines()
    for line in lines:
        print(line)
        sleep(0.75)
    f.close()


# 递归创建文件夹
def createDir(path):
    try:
        os.makedirs(path)
    except:
        print('目录已经存在：' + path)

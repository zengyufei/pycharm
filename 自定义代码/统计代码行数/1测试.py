# encoding:utf-8

import os

mainpath = 'D:/dowork/ideac/hd/itmc/services/showcase'


# mainpath = 'D:\ProjectFiles\SIMClient\src'

def getlines(path):
    files = os.listdir(path)
    theline = 0
    for file in files:
        newpath = path + "\\" + file

        print(newpath)
        if os.path.isdir(newpath):
            theline += getlines(newpath)

        if os.path.isfile(newpath):
            data = ''
            try:
                data = open(newpath, encoding='UTF-8')
            except:
                data = open(newpath, encoding='GBK')
            num = len(data.readlines())
            theline += num

    return theline


if __name__ == '__main__':
    lines = getlines(mainpath)
    print('代码行数：', lines)

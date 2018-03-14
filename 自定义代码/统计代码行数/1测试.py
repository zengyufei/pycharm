# encoding:utf-8

import os

pre_mainpath = 'D:/dowork/ideac/hd/itmc/endpoints'

java_mainpath = 'D:/dowork/ideac/hd/itmc/services/showcase'


# mainpath = 'D:\ProjectFiles\SIMClient\src'

def getlines(path):
    files = os.listdir(path)
    theline = 0
    for file in files:
        newpath = path + "\\" + file
        if file.endswith('.original'):
            continue
        if file.endswith('.jar'):
            continue
        if file.endswith('.class'):
            continue
        if file.endswith('.logs'):
            continue
        if file.endswith('.log'):
            continue
        if file.endswith('.ico'):
            continue
        if file.endswith('.jpg'):
            continue
        if file.endswith('.png'):
            continue
        if file.endswith('.gz'):
            continue
        if file.endswith('.DS_Store'):
            continue
        if newpath.find('node_modules') > -1:
            continue
        # if newpath.find('itmc-frontend\static') > -1:
        #    continue
        if newpath.find('\\target\\') > -1:
            continue
        print(newpath)
        if os.path.isdir(newpath):
            theline += getlines(newpath)

        if os.path.isfile(newpath):
            data = ''
            try:
                data = open(newpath, encoding='UTF-8')
            except:
                try:
                    data = open(newpath, encoding='GBK')
                except:
                    continue
            num = len(data.readlines())
            theline += num

    return theline


if __name__ == '__main__':
    lines1 = getlines(pre_mainpath)
    print('\n')
    print('\n')
    print('\n')
    print(
        '----------------------------------------------------------------------------------------------------------------------分割线-------------------------------------------------------------------------------------------------------------------------------')
    print(
        '----------------------------------------------------------------------------------------------------------------------分割线-------------------------------------------------------------------------------------------------------------------------------')
    print(
        '----------------------------------------------------------------------------------------------------------------------分割线-------------------------------------------------------------------------------------------------------------------------------')
    print(
        '----------------------------------------------------------------------------------------------------------------------分割线-------------------------------------------------------------------------------------------------------------------------------')
    print('\n')
    print('\n')
    print('\n')
    lines2 = getlines(java_mainpath)
    print('前端代码行数：', lines1)
    print('后端代码行数：', lines2)
    print('总数：', int(lines1) + int(lines2))

import os


# 递归创建文件夹
def createDir(path):
    try:
        os.makedirs(path)
    except:
        print('目录已经存在：' + path)

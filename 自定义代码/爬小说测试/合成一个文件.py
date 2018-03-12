import os


def load(dir):
    file_list = []
    for file in os.listdir(dir) :
        filePath = os.path.join(dir, file)
        file_list.append(filePath)
    file_list.sort(key=compare)
    return file_list

def compare(x):
    stat_x = os.stat(x)
    return stat_x.st_ctime

f = open('合成召唤.txt', 'w+', encoding="UTF-8")
files = load("合成召唤")
for file in files:
    #print(file)
    tempF = open(file, 'r', encoding="UTF-8")
    read = tempF.read()
    f.write(read + "\n\n")
    tempF.close()
f.close()
from time import sleep

def printConsole(title, content):
    print(title)
    print(content)

def writeFile(fileName, fileContent):
    f = open(fileName + ".txt", "w", encoding="UTF-8")
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

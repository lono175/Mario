import random

def SampleData(dataList, sampleNum):
    sample = []
    dataLen = len(dataList)
    i = 0
    for data in dataList:
        if i == sampleNum:
           break 
        sample.append(dataList[random.randint(0, dataLen-1)])
        i = i + 1
    return sample

def getMarioLoc(observation, size):
    height, width = size
    for y in range(0, height):
        for x in range(0, width):
            key = (y, x)
            if(observation[key] == 1):
                return key
    return (-1, -1)
     
def getObjLoc(observation, size):
    res = []
    height, width = size
    for y in range(0, height):
        for x in range(0, width):
            key = (y, x)
            if(observation[key] == 2):
                res.append( (2, y, x))
            elif (observation[key] == 3):
                res.append( (3, y, x))
    return res
def addGoalLoc(objLoc, goal):
    newObjLoc = objLoc[:]
    newObjLoc.append((4, goal[0], goal[1]))
    return newObjLoc

def Save(agent, filename): 
    import cPickle
    output = open(filename, 'wb')
    cPickle.dump(agent, output)
    output.close()

def Load(filename):
    import cPickle
    input = open(filename, 'rb')
    return cPickle.load(input)

def SaveToCSVSingle(list, filename):
    FILE = open(filename,"w")
    for line in list:
        FILE.write(str(line))
        FILE.write('\n')
    FILE.close()
def SaveToCSV(list, filename):
    FILE = open(filename,"w")
    for line in list:
        for item in line:
            FILE.write(str(item))
            FILE.write(', ')
        FILE.write('\n')
    FILE.close()
from MarioAgent import *
if __name__ == '__main__':
    agent = Load('mario_sarsa_999_0.01_0.db')
    SaveToCSV(agent.distList, 'mario_sarsa_999_0_01_0.csv')

   

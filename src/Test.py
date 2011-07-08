from Def import *

class Observation:
    def __init__(self):
        pass


def addMonster(m, obs):
    obs.doubleArray.append(m.x)
    obs.doubleArray.append(m.y)
    obs.doubleArray.append(m.sx)
    obs.doubleArray.append(m.sy)
    obs.intArray.append(m.type)
    obs.intArray.append(m.winged)
    return obs

def getDummyObservation():
    obs = Observation()
    obs.doubleArray = []
    obs.intArray = [40] #originX
    obs.charArray = []
    for y in range(0, MaxY):
        for x in range(0, MaxX):
            obs.charArray.append('7')

    m = createMario()
    obs = addMonster(m, obs)

    m = createSpikey()
    obs = addMonster(m, obs)
    
    m = createMushroom()
    obs = addMonster(m, obs)
    return obs

def createMario():
    m = Monster()
    m.type = 10
    m.winged = False
    m.x = 55
    m.y = 2
    m.sx = 2.0
    m.sy = 1.0
    return m

def createMushroom():
    m = Monster()
    m.type = 6
    m.winged = False
    m.x = 52
    m.y = 4
    m.sx = 40.0
    m.sy = 41.0
    return m
def createSpikey():
    m = Monster()

    m.type = 4 #use original id
    m.winged = False
    m.x = 57
    m.y = 2
    m.sx = 42.0
    m.sy = 43.0
    return m
#-------------------UNIT TEST--------------------------
#def getDummyRewardTree():
        #modelFea = [str(lastActionId), round(lastMario.sx, 1), round(lastMario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))] + [round(mario.sx, 1), round(mario.sy, 1), round(deltaX, 1), round(deltaY, 1), 0] #don't learn the pseudo reward
        #rewardFea = toRewardFea(modelFea, len(self.domainList))
#def getDummyTree():
        #
#def getDummyMario():
    #m = Monster()
    #m.type = MonType.Mario 

    #m.x = 11
    #m.y = 13
    #m.sx = 0
    #m.sy = 0
    #return m
    #
#def getDummyMonsterList():
    #monList = []
    #m = Monster()
    #m.type = MonType.RedKoopa 

    #m.x = 15
    #m.y = 13
    #m.sx = 0
    #m.sy = 0
    #monList.append(m)
    #return monList

from rlglue.types import Action

InPitPenalty = -50.0
DeathPenalty = -50.0
class MonType:
    Mario = ord('M') #good 0
    RedKoopa = ord('R') #1
    GreenKoopa = ord('G') #2
    Goomba = ord('O') #3
    Spikey = ord('S') #4
    PiranhaPlant = ord('P') #5
    Mushroom = ord('U') #good 6
    FireFlower = ord('F') #good 7
    Fireball = ord('B') #good 8
    Shall = ord('H') #9
    BigMario = ord('m') #good 10
    FieryMario = ord('E') #good 11
    FlyRedKoopa = ord('r') #12
    FlyGreenKoopa = ord('g') #13
    FlyGoomba = ord('o') #14
    FlySpikey = ord('s') #exist? #15
    GeneralObj = ord('Z') #16

MaxY = 16
MaxX = 22
def getActionRange():
    range = []
    actionList = getAllAction()
    for action in actionList:
        range.append(getActionId(action))
    return range


class Monster:
    def __init__(self):
        pass

def getAction(dir, isJump, isSpeed):
    #-1, 0, 1 for direction, 1 is to the right
    #0, 1 for jump
    #0, 1 for speed
    action = Action()
    action.numInts = 3
    action.numDoubles = 0
    action.numChars = 0
    action.intArray = []
    action.doubleArray = []
    action.charArray = []
    action.intArray.append(dir)
    action.intArray.append(isJump)
    action.intArray.append(isSpeed)
    return action

def getActionType(actionId):
    isSpeed = actionId & 1
    isJump = (actionId >> 1) & 1
    dir = (actionId >> 2) - 1
    return dir, isJump, isSpeed
def dumpAction(action):
    print action.intArray[0], " ", action.intArray[1], " ", action.intArray[2]

def dumpActionList(actionList):
    for action in actionList:
        print (action.intArray[0], action.intArray[1], action.intArray[2]),
    print ""

def dumpList(list):
    for item in list:
        print '%02.3f'%item, " ",
    print " "

def dumpObj(obj):
    print "dump4...."
    print dir(obj) 
    print "dump4...."
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))

def getAllAction():
    actionList = []
    for dir in [-1, 0, 1]:
        for isJump in [0, 1]:
            for isSpeed in [0, 1]:
                if dir == 0 and isJump == 0 and isSpeed == 0:
                    continue
                if dir == 0 and isJump == 0 and isSpeed == 1:
                    continue
                if dir == 0 and isJump == 1 and isSpeed == 1:
                    continue
                action = getAction(dir, isJump, isSpeed)
                actionList.append(action)
    #actionList = [getAction(1, 1, 1)]
    return actionList

def getActionId(action):
    id = ((action.intArray[0] + 1) << 2) + ((action.intArray[1]) << 1) + (action.intArray[2])
    return id

def makeAction(actionId):
    isSpeed = actionId & 1
    isJump = (actionId >> 1) & 1
    dir = (actionId >> 2) - 1
    return getAction(dir, isJump, isSpeed)

ActionRange = getActionRange()


#desired action, x-speed, y-speed(-2~2), observation around mario (5 by 5) -> new x-speed (-2~2), new y-speed (-2~2), (delta x ( , delta y
#0~7((0, 1, 1),     1,       -1,          , 32,                              , x + x-speed + delta x

import orange, random

    #Returns the char representing the tile at the given location.
    #If unknown, returns 'x'.
    #
    #Valid tiles:
    #M - the tile mario is currently on. there is no tile for a monster.
    #$ - a coin
    #b - a smashable brick
    #? - a question block
    #| - a pipe. gets its own tile because often there are pirahna plants
        #in them
    #! - the finish line
    #And an integer in [1,7] is a 3 bit binary flag
    #first bit is "cannot go through this tile from above"
    #second bit is "cannot go through this tile from below"
    #third bit is "cannot go through this tile from either side"
#x, y is the relative coordinate
def getTileAt(x, y, obs):
    assert(x >= 0)
    assert(x < MaxX)
    assert(y >= 0)
    assert(y < MaxY)
    index = y*MaxX+x;
    tile = obs.charArray[index]
    #disable coin
    val = ord(tile)
    if val == ord('$'):
        return ord(' ')
    return val

class Action():
    def __init__(self):
        pass

# 3 + 25 + 4 classes= 32 
def getClassifier(data):
    FeatureNum = 28
    var = orange.EnumVariable("new x-speed", values = ['%i'%x for x in range()])
    assert(len(data) > 0)
    inputNum = len(data[0])
    classNum = inputNum - FeatureNum

    commonDomain = getDomain()
    for i in range(classNum):
        if i == 0:
            
    
def getDomain():
    tileList = ['$', 'b', '?', '|', '!', 'M', '1', '2', '3', '4', '5', '6', '7']
    domain = []
    #var = orange.EnumVariable("action", values=actionList)
    var = orange.EnumVariable("action", values = ['%i'%x for x in range(8)])
    domain.append(var)
    var = orange.EnumVariable("x-speed", values = ['%i'%x for x in range(-2, 3)])
    domain.append(var)
    var = orange.EnumVariable("y-speed", values = ['%i'%x for x in range(-2, 3)])
    domain.append(var)
    for x in range(25):
        var = orange.EnumVariable("obs%i"%x, values = tileList)
        domain.append(var)
    d = orange.Domain(domain)
    return d
    
    #a = [[1], [2], [1], [2]]
    #a = [['1', 1.2], ['2', 1.3], ['1', 1.4], ['2', 1.5]]
    #data = orange.ExampleTable(d, a)
    #print data[0]
    #print data[1]
    #print data[2]
    #print data[3]
    #treeClassifier = orange.TreeLearner(data) 

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

def getAllAction():
    actionList = []
    for dir in [-1, 0, 1]:
        for isJump in [0, 1]:
            for isSpeed in [0, 1]:
                action = getAction(dir, isJump, isSpeed)
                actionList.append(action)
    #actionList = [getAction(1, 1, 1)]
    return actionList
#classattr = orange.EnumVariable("y", values = ["0", "1"])
#card = [3, 3, 2, 3, 4, 2]
#values = ["1", "2", "3", "4"]
#print values
#attributes = [ orange.EnumVariable(chr(97+i), values = values[:card[i]]) for i in range(6)]
#domain = orange.Domain(attributes + [classattr])
#data = orange.ExampleTable(domain)
#print len(data)
#print attributes
#print data[0]
#for i in range(0, len(data)):
    #print data[i]

import numpy
if __name__ == '__main__':
    getDomain() 
    #deg3 = orange.EnumVariable("deg3", values=["little", "medium", "big"])
    #d = orange.Domain([orange.FloatVariable('a%i'%x) for x in range(5)])
    #domain = [orange.FloatVariable('a%i'%x) for x in range(4)]
    #domain.append(orange.EnumVariable("b1", base))
    #d = orange.Domain(domain)
    #a = numpy.array([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]])
    #t = orange.ExampleTable(d, a)
    #print t[0]
    #print t[1]


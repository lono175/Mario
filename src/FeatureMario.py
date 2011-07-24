#from numpy  import *
from Def    import MonType, MaxX, MaxY, Precision
from WorldState import *
BlockLen = 2
def getTestFeature(state, actionId):
    mario = state.mario
    tileList = getTileAroundMario(state, BlockLen)
    assert(len(tileList) == 25)
    offsetX = round(mario.x - int(mario.x), Precision)
    offsetY = round(mario.y - int(mario.y), Precision)
    fea = [str(actionId), offsetX, offsetY, round(mario.sx, Precision), round(mario.sy, Precision)] + [chr(tileList[x]) for x in range(len(tileList))] 
    #fea = [str(actionId), round(mario.sx, Precision), round(mario.sy, Precision)] + [chr(tileList[x]) for x in range(len(tileList))] 
    return fea

def getTrainFeature(state, classValueList, actionId):
    mario = state.mario
    tileList = getTileAroundMario(state, BlockLen)
    assert(len(tileList) == 25)
    offsetX = round(mario.x - int(mario.x), Precision)
    offsetY = round(mario.y - int(mario.y), Precision)
    fea = [str(actionId), offsetX, offsetY, round(mario.sx, Precision), round(mario.sy, Precision)] + [chr(tileList[x]) for x in range(len(tileList))]  + classValueList
    #fea = [str(actionId), round(mario.sx, 1), round(mario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))]  + classValueList
    return fea
def getModelFeature(state, classValueList):
    mario = state.mario
    tileList = getTileAroundMario(state, BlockLen)
    assert(len(tileList) == 25)
    offsetX = round(mario.x - int(mario.x), Precision)
    offsetY = round(mario.y - int(mario.y), Precision)
    fea = [offsetX, offsetY, round(mario.sx, Precision), round(mario.sy, Precision)] + [chr(tileList[x]) for x in range(len(tileList))]  + classValueList
    #fea = [round(mario.sx, 1), round(mario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))]  + classValueList
    return fea

def getTileAroundMario(state, halfLen):
    m = state.mario
    originX = state.origin
    return getTileBlock(state.gridMap, int(m.x - originX), int(m.y), halfLen)
    
def isMarioInPit(state):
    m = state.mario
    pitList = state.pitList
    mx = m.x - state.origin
    my = m.y

    for pit in pitList:
        if mx >= pit.x and mx < (pit.x + pit.width) and my >= pit.y and my < (pit.y+pit.height):
            print "pit: ", mx, " ", my, " ", pit.x, " ", pit.y
            return True
    return False

#OBS, int, int, int -> list of tile and monster
#x, y is the coordinate of screen
def getTileBlock(monMap, inX, inY, halfLen):
    res = []
    for y in range(-halfLen + inY, halfLen + inY + 1):
        for x in range(-halfLen + inX, halfLen + inX + 1):
            if (not x in range(MaxX)) or (not y in range(MaxY)):
                if x < 0:
                    tile = ord('w')
                else:
                    tile = ord(' ') #the end of the world
            else:
                tile = monMap[y, x]
            res.append(tile)
    return res

def getGridFeature(map, x, y, halfLen):
    #print x
    #print y
    #assert(x >= -1)
    #assert(x < MaxX)
    #assert(y >= 0)
    bX = max(x - halfLen, 0)
    bY = max(y - halfLen, 0)
    eX = min(x + halfLen + 1, MaxX)
    eY = min(y + halfLen + 1, MaxY)
    subMat = map[bY:eY, bX:eX]
    fea = [(x, y)] #add coordinate
    for row in subMat:
        fea.append(tuple(row))
    if len(fea) == 1:
        return ()
    return tuple(fea)

#int, int, int->listof loc
def getRegularGridShape(x, y, halfLen):
    locList = []
    blockLen = 2*halfLen + 1

    #5 by 5 large block
    for i in range(-1, 3):
        for j in range(-1, 3):
            locList.append((x + blockLen*i, y + blockLen*j))
            
    return locList

def getReducedRegularGridShape(x, y, halfLen):
    locList = []
    blockLen = 2*halfLen + 1
    
    locList.append((x, y))
    locList.append((x, y + blockLen))
    locList.append((x, y + 2*blockLen))
    locList.append((x + blockLen, y))
    locList.append((x + 2*blockLen, y))
    #5 by 5 large block
    #for i in range(0, 3):
        #for j in range(-2, 2):
            #locList.append((x + blockLen*i, y + blockLen*j))
            
    return locList

def getCrossShape(x, y, halfLen):
    locList = []
    locList.append((x + halfLen, y - halfLen))
    locList.append((x + halfLen, y + halfLen))
    locList.append((x - halfLen, y - halfLen))
    locList.append((x - halfLen, y + halfLen))

    locList.append((x + 2*halfLen, y + 3*halfLen))
    locList.append((x + 2*halfLen, y - 3*halfLen))
    locList.append((x + 3*halfLen, y))
    #locList.append(x, y)
    #locList.append(x, y + 2*halfLen)
    #locList.append(x, y - 2*halfLen)
    #locList.append(x - 2*halfLen, y)
    #locList.append(x + 2*halfLen, y)
    return locList

def getQuanVec(vec):
    quanLevel = 0.8
    val = 1
    if vec == 0:
        return 0
    if vec > 0:
       val = 1
    else:
       val = -1

    return val + int(vec/quanLevel)

def getGridFeatureList(obs):
    halfLen = 1
    map = getMonsterGridMap(obs)
    #sample with cross shape
    mario = getMario(obs)
    vx = getQuanVec(mario.sx)
    vy = getQuanVec(mario.sy)
    #print "mario Loc: ", mario.x
    #print "mario Loc: ", mario.y
    #print "origin Loc: ", getOrigin(obs)
    #locList = getCrossShape(int(mario.x - getOrigin(obs)), int(mario.y), halfLen)
    locList = getRegularGridShape(int(mario.x - getOrigin(obs)), int(mario.y), halfLen)
    #locList = getReducedRegularGridShape(int(mario.x - getOrigin(obs)), int(mario.y), halfLen)
    feaList = []
    for loc in locList:
        fea = getGridFeature(map, loc[0], loc[1], halfLen)
        if fea == ():
            continue
        #get a feature for x and another feature for y 
        feaList.append((vx, fea))
        feaList.append((vy, fea))

    return feaList

def getConstantQ(obs, agent):
    feaList = getConstantFeature(obs)    
    Q = agent.getAllQ(feaList)
    return Q

def getTileQ(obs, agent):
    feaList = getTileList(obs)    
    Q = agent.getAllQ(feaList)
    return Q

def getGridQ(obs, agent):
    feaList = getGridFeatureList(obs)    
    Q = agent.getAllQ(feaList)
    return Q

def getGridQInd(obs, agent, index):
    oldfeaList = getGridFeatureList(obs)    
    fea = oldfeaList[index]
    Q = agent.getAllQ([fea])
    return Q

def getMonsterQ(obs, agent):
    feaList = getMonsterFeatureList(obs)
    Q = agent.getAllQ(feaList)
    return Q

def getConstantFeature(obs):
    mario = getMario(obs)
    feaList = []
    feaList.append(1) #add a constant term
    #add a dummy term to indicate the location of mario
    #feaList.append((int(0), int(mario.y + 0.5), int(mario.sx+0.5), int(mario.sy+0.5), 0, 2))
    return feaList


def getRewardFeature(state, prevAction):
    feaList = []
    monList = getBadMonster(state) 
    mario = state.mario
    #vx = getQuanVec(mario.sx)
    #vy = getQuanVec(mario.sy)
    #for m in monList:
        #a general one to let mario "fear" the monster
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), MonType.GeneralObj, m.winged)
        #feaList.append(fea)
    for m in monList:
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sx - mario.sx + 0.5), int(m.sy - mario.sy + 0.5), m.type, m.winged)
        dx = round(m.x - mario.x, 0)
        dy = round(m.y - mario.y, 0)
        if dx > 3 or dx <= -3:
            continue
        if abs(dy) > 4 :
            continue
        #fea = (dx, dy, prevAction, m.type)
        fea = (dx, dy, m.type)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sy + 0.5), vy, m.type)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5),  m.type, m.winged)
        feaList.append(fea)
    for p in state.pitList:
        dx = round(p.x - mario.x + state.origin, 0)
        dy = round(p.y - mario.y, 0)
        if dx > 3 or dx <= -4:
            continue
        if abs(dy) > 7 :
            continue
        #fea = (dx, dy, prevAction, m.type)
        if dx <= 0 and dy < 0:
            fea = (0, dx, dy, 0) #prevAction is not useful here
        else:
            fea = (0, dx, dy, prevAction)
        #fea = (dx, dy)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sy + 0.5), vy, m.type)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5),  m.type, m.winged)
        feaList.append(fea)
    if feaList == []:
        feaList = [()]
    return feaList

def getMonsterFeatureList(state, prevAction):
    feaList = []
    monList = getBadMonster(state) 
    mario = state.mario
    #vx = getQuanVec(mario.sx)
    #vy = getQuanVec(mario.sy)
    #for m in monList:
        #a general one to let mario "fear" the monster
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), MonType.GeneralObj, m.winged)
        #feaList.append(fea)
    for m in monList:
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sx - mario.sx + 0.5), int(m.sy - mario.sy + 0.5), m.type, m.winged)
        dx = round(m.x - mario.x, 0)
        dy = round(m.y - mario.y, 0)
        #vx = getQuanVec(m.sx)
        #vy = getQuanVec(m.sy)
        if dx > 7 or dx <= -3:
            continue
        if abs(dy) > 5 :
            continue
        #fea = (dx, dy, prevAction, m.type)
        #fea = (dx, dy, vx, vy, m.type)
        fea = (dx, dy, m.type)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sy + 0.5), vy, m.type)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5),  m.type, m.winged)
        feaList.append(fea)
    for p in state.pitList:
        dx = round(p.x - mario.x + state.origin, 0)
        dy = round(p.y - mario.y, 0)
        if dx > 7 or dx <= -5:
            continue
        if abs(dy) > 7 :
            continue
        #fea = (dx, dy, prevAction, m.type)
        if dx <= 0 and dy < 0:
            fea = (0, dx, dy, 0) #prevAction is not useful here
        else:
            fea = (0, dx, dy, prevAction)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sy + 0.5), vy, m.type)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5),  m.type, m.winged)
        feaList.append(fea)

    return feaList
    
def getSarsaFeature(state, prevAction):
    feaList = []
    #feaList.append((int(0), int(mario.y + 0.5), int(mario.sx), int(mario.sy), 0, mario.winged))
    #fea = getConstantFeature(obs)
    #feaList.extend(fea)
    fea = getMonsterFeatureList(state, prevAction)
    feaList.extend(fea)
    #fea = getTileList(obs)
    #fea = getGridFeatureList(obs)
    #feaList.extend(fea)

    if feaList == []:
        feaList.append(())
    return feaList

#------------unit test function------------------
from Test import * 
def Test():
    obs = getDummyObservation(10, 15)
    state = WorldState(obs)
    print "x, y ", state.mario.x, " ", state.mario.y
    state.dump()
    tileList = getTileAroundMario(state, BlockLen)
    modelFea = getTrainFeature(state, [], 0)
    print modelFea

    obs = getDummyPitObservation(10, 13)
    state = WorldState(obs)
    assert(isMarioInPit(state) == True)
    obs = getDummyPitObservation(9, 13)
    state = WorldState(obs)
    assert(isMarioInPit(state) == True)
    obs = getDummyPitObservation(11, 13)
    state = WorldState(obs)
    assert(isMarioInPit(state) == True)
    obs = getDummyPitObservation(11, 12)
    state = WorldState(obs)
    state.mario.y = 10.95
    state.mario.x = 12.9 + state.origin
    state.dump()
    assert(isMarioInPit(state) == False)


    
if __name__ == '__main__':
    Test()
    

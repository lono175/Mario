from numpy  import *
MaxY = 15
MaxX = 21
class MonType:
    Mario = 0 #good
    RedKoopa = 1
    GreenKoopa = 2
    Goomba = 3
    Spikey = 4
    PiranhaPlant = 5
    Mushroom = 6 #good
    FireFlower = 7 #good
    Fireball = 8 #good
    Shall = 9
    BigMario = 10 #good
    FieryMario = 11 #good
    GeneralObj = 12
class Monster:
    def __init__(self):
        pass
def getMonsterGridMap(obs):
    map = zeros( (MaxY+1, MaxX+1), dtype=int )     
    for y in range(0, MaxY):
        for x in range(0, MaxX):
            map[y, x] = getTileAt(x, y, obs)
    #add monster
    monList = getMonsterNoMario(obs)
    #TODO: adjust coordinate here
    originX = getOrigin(obs)
    #print "ori:", originX
    for m in monList:
        #print "x:", m.x
        x = int(m.x - originX)
        if x > MaxX:
            continue
        map[int(m.y), int(m.x - originX)] = m.type
    return map
def getOrigin(obs):
    return obs.intArray[0]
        
def getGridFeature(map, x, y, halfLen):
    bX = max(x - halfLen, 0)
    bY = max(y - halfLen, 0)
    eX = min(x + halfLen + 1, MaxX + 1)
    eY = min(y + halfLen + 1, MaxY + 1)
    subMat = map[bY:eY, bX:eX]
    fea = []
    for row in subMat:
        fea.append(tuple(row))
    return tuple(fea)
#int, int, int->listof loc
def getCrossShape(x, y, halfLen):
    locList = []
    locList.append((x + halfLen, y - halfLen))
    locList.append((x + halfLen, y + halfLen))
    locList.append((x - halfLen, y - halfLen))
    locList.append((x - halfLen, y + halfLen))
    #locList.append(x, y)
    #locList.append(x, y + 2*halfLen)
    #locList.append(x, y - 2*halfLen)
    #locList.append(x - 2*halfLen, y)
    #locList.append(x + 2*halfLen, y)
    return locList
        
def getGridFeatureList(obs):
    halfLen = 1
    map = getMonsterGridMap(obs)
    #sample with cross shape
    mario = getMario(obs)
    locList = getCrossShape(int(mario.x), int(mario.y), halfLen)
    feaList = []
    for loc in locList:
        fea = getGridFeature(map, loc[0], loc[1], halfLen)
        feaList.append(fea)

    return feaList
    
    
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
def getTileAt(xf, yf, obs):
    x = int(xf)
    if x < 0:
        return ord('7')
    y = 16 - int(yf)
    x =  x - obs.intArray[0]
    if x < 0 or x > 21 or y < 0 or y > 15:
        return ord('x')
    index = y*22+x;
    tile = obs.charArray[index]
    #print obs.charArray
    #print ord(tile)
    return ord(tile)
        
def getMario(obs):
    monList = getMonsterList(obs)
    for m in monList:
        if isMario(m):
            #print "type: ", m.type
            return m
    assert(False)

def isMario(m):
    if m.type == MonType.Mario or m.type == MonType.BigMario or m.type == MonType.FieryMario:
        #print "type: ", m.type
        return True
    return False
def isGood(m):
    if m.type == MonType.Mario or m.type == MonType.BigMario or m.type == MonType.FieryMario or m.type == MonType.Mushroom or m.type == MonType.FireFlower or m.type == MonType.Fireball:
        return True
    return False
def removeMario(monList):
    newList = []
    for m in monList:
        if not isMario(m):
           newList.append(m) 
    return newList
def removeGoodMonster(monList):
    newList = []
    for m in monList:
        if isGood(m):
            continue
        newList.append(m)
    return newList
        
def getMonsterNoMario(obs):
    monList = getMonsterList(obs)
    return removeMario(monList)
def getBadMonster(obs):
    monList = getMonsterList(obs)                    
    return removeGoodMonster(monList)
def getMonsterList(obs):
    monList = []
    for i in range(0, len(obs.intArray)):
        if i % 2 == 0:
           continue 

        id = i / 2
        type = obs.intArray[i]
        winged = obs.intArray[i+1]
        m = Monster()
        m.type = type
        m.winged = False
        if winged != 0:
            m.winged = True    

        #print "index ", i
        #print "len ", len(obs.doubleArray)
        m.x = obs.doubleArray[4*id];
        m.y = obs.doubleArray[4*id+1];
        m.sx = obs.doubleArray[4*id+2];
        m.sy = obs.doubleArray[4*id+3];
        monList.append(m)

    return monList
def getTileList(obs):
    
    tileList = []
    mario = getMario(obs)
    mario.x = int(mario.x)
    mario.y = int(mario.y)
    offset = -(MaxY - mario.y)
    #for dy in range(offset, 5):
        #for dx in range(0, 7):
    for dy in range(-2, 3):
        for dx in range(0, 3):
            tile = getTileAt(mario.x + dx, mario.y + dy, obs) 		
            tileList.append((dx, dy, tile)) #use absolute location for y to detect pit (always at (x, 0))
    return tileList
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
def getMonsterQ(obs, agent):
    feaList = getMonsterFeatureList(obs)
    Q = agent.getAllQ(feaList)
    return Q
def getConstantFeature(obs):
    mario = getMario(obs)
    feaList = []
    feaList.append(1) #add a constant term
    #add a dummy term to indicate the location of mario
    feaList.append((int(0), int(mario.y + 0.5), int(mario.sx+0.5), int(mario.sy+0.5), 0, 2))
    return feaList

def getMonsterFeatureList(obs):
    feaList = []
    monList = getBadMonster(obs) 
    mario = getMario(obs)
    for m in monList:
        #a general one to let mario "fear" the monster
        fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), MonType.GeneralObj, m.winged)
        feaList.append(fea)
    for m in monList:
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sx - mario.sx + 0.5), int(m.sy - mario.sy + 0.5), m.type, m.winged)
        fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5), int(m.sx + 0.5), int(m.sy + 0.5), m.type, m.winged)
        #fea = (int(m.x - mario.x + 0.5), int(m.y - mario.y + 0.5),  m.type, m.winged)
        feaList.append(fea)
    return feaList
    
    
def getSarsaFeature(obs):
    feaList = []
    #feaList.append((int(0), int(mario.y + 0.5), int(mario.sx), int(mario.sy), 0, mario.winged))
    fea = getConstantFeature(obs)
    feaList.extend(fea)
    fea = getMonsterFeatureList(obs)
    feaList.extend(fea)
    #fea = getTileList(obs)
    fea = getGridFeatureList(obs)
    feaList.extend(fea)
    return feaList
#def getMonsterList(obs):
    #monList = []
    #for i in range(0, len(obs.intArray)):
        #if i % 2 == 0:
           #continue 

        #id = i / 2
        #type = obs.intArray[i]
        #winged = obs.intArray[i+1]
        #m = Monster()
        #m.type = type
        #m.winged = False
        #if winged != 0:
            #m.winged = True    

        ##print "index ", i
        ##print "len ", len(obs.doubleArray)
        #m.x = obs.doubleArray[4*id];
        #m.y = obs.doubleArray[4*id+1];
        #m.sx = obs.doubleArray[4*id+2];
        #m.sy = obs.doubleArray[4*id+3];
        #monList.append(m)
#------------unit test function------------------
def getObservation():
    monNum = 2
    obs.charArray = []
    for y in range(0, MaxY+1):
        for x in range(0, MaxX+1):
            obs.charArray.append('7')
if __name__ == '__main__':
    pass 
    
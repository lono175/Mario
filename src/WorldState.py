MaxY = 16
MaxX = 22
class WorldState():
    #mario
    #monsterList (no mario)
    #gridMap (no mario loc)
    #expected reward for the current world state (real reward and A* reward)
    def __init__(obs):
        self.mario = getMario(obs)
        self.origin = getOrigin(obs)
        self.gridMap = getMonsterGridMap(obs)
        self.monsterList = getMonsterNoMario(obs)


def getOrigin(obs):
    return obs.intArray[0]

def getMario(obs):
    monList = getMonsterList(obs)
    for m in monList:
        if isMario(m):
            #print "type: ", m.type
            return m
    assert(False)

def getMonsterList(obs):
    monList = []
    for i in range(0, len(obs.intArray)):
        if i % 2 == 0:
           continue 

        id = i / 2
        type = obs.intArray[i]
        winged = obs.intArray[i+1]
        m = Monster()
        typeList = getMonsterTypeList()
        m.type = typeList[type]

        if winged != 0:
            if m.type == MonType.RedKoopa:
                m.type = MonType.FlyRedKoopa

            elif m.type == MonType.GreenKoopa:
                m.type = MonType.FlyGreenKoopa

            elif m.type == MonType.Goomba:
                m.type == MonType.FlyGoomba

            elif m.type == MonType.Spikey:
                m.type == MonType.FlySpikey
            else:
                assert(False)

        m.x = obs.doubleArray[4*id]
        m.y = MaxY - obs.doubleArray[4*id+1] #use left-top corner as the origin
        m.sx = obs.doubleArray[4*id+2]
        m.sy = -obs.doubleArray[4*id+3]       #use left-top corner as the origin;
        monList.append(m)

    return monList

def getMonsterGridMap(obs):

    map = zeros( (MaxY, MaxX), dtype=int )     
    for y in range(0, MaxY):
        for x in range(0, MaxX):
            map[y, x] = getTileAt(x, y, obs)

    #TODO: adjust coordinate here
    originX = getOrigin(obs)

    #remove mario
    mario = getMario(obs)
    x = int(mario.x - originX)
    y = int(mario.y)
    map[y, x] = ord(' ')

    #add monster
    monList = getMonsterNoMario(obs)

    for m in monList:
        #print "x:", m.x
        x = int(m.x - originX)
        y = int(m.y)
        if x >= MaxX:
            continue
        if y >= MaxY:
            continue
        map[y, x] = m.type
    return map

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

def getMonsterTypeList():
    monTypeList = [MonType.Mario, MonType.RedKoopa, MonType.GreenKoopa, MonType.Goomba, MonType.Spikey, MonType.PiranhaPlant, MonType.Mushroom, MonType.FireFlower, MonType.Fireball, MonType.Shall, MonType.BigMario, MonType.FieryMario, MonType.FlyRedKoopa, MonType.FlyGreenKoopa, MonType.FlyGoomba, MonType.FlySpikey]
    return monTypeList

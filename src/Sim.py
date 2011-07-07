#gridMap should remove mario
#return the location of mario

#class WorldState():
    ##mario
    ##monsterList
    ##gridMap (no mario loc)
    ##expected reward for the current world state (real reward and A* reward)
    #def __init__(self):
        #pass

class ActionState():
    #action
    #the list of WorldState (len: MaxState)
    #the real reward from all WorldState
    #the A* reward from all WorldState
    def __init__(self):
        pass

def Optimize(mario, monsterList, gridMap, rewardTree, treeList, MaxNode):
    MaxState = 10
    MaxDepth = 6
    MaxDist = MaxDepth * 2
    nodeList = {}
    #create the initial nodes for 12 actions, each node has 10 world states
    
    #do A* here
    #choose a node with highest average reward which does not exceed MaxDepth

    #remove a node and expand it

    #stop when MaxNode reached or find the optimal path (the average reward > MaxDist) 

#WorldState, listof decision trees -> listof ActionState
#treeList includes the reward tree
#sample the effect of all actions for the mario state
def Expand(state, treeList, domainList):
    ActionRange = range(12)
    for actionId in ActionRange:
        fea = getModelFeature(actionId, state)
        m = state.mario
        sx, sy, dx, dy, reward = classify(fea, treeList, domainList) #TODO: add randomness here

        newMario = copy.copy(m)
        newMario.x = m.x + m.sx + dx
        newMario.y = m.y + m.sy + dy
        newMario.sx = sx
        newMario.sy = sy

        newState = state #with static assumption, everything other than mario stays the same
        newState.mario = newMario
        newState
        
def classify(data, treeList, domainList):
    classNum = len(domainList)
    partData = [orange.Example(domainList[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(classNum)]
    res = [treeList[i](partData[i]).value for i in range(classNum)]
    return res


    pass
    
#-------------------UNIT TEST--------------------------
def getDummyRewardTree():
        modelFea = [str(lastActionId), round(lastMario.sx, 1), round(lastMario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))] + [round(mario.sx, 1), round(mario.sy, 1), round(deltaX, 1), round(deltaY, 1), 0] #don't learn the pseudo reward
        rewardFea = toRewardFea(modelFea, len(self.domainList))
def getDummyTree():
        
def getDummyMario():
    m = Monster()
    m.type = MonType.Mario 

    m.x = 11
    m.y = 13
    m.sx = 0
    m.sy = 0
    return m
    
def getDummyMonsterList():
    monList = []
    m = Monster()
    m.type = MonType.RedKoopa 

    m.x = 15
    m.y = 13
    m.sx = 0
    m.sy = 0
    monList.append(m)
    return monList

if __name__ == '__main__':
    MaxY = 16
    MaxX = 22
    map = numpy.array([[ord(' ') for x in range(MaxX)] for y in range(MaxY))
    monList = getDummyMonsterList() 
    mario = getDummyMario()

    s = WorldState()
    s.mario = mario
    s.monsterList = monList
    s.gridMap = map

    

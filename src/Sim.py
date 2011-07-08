from WorldState import WorldState
from heapq import heappush, heappop

def Optimize(initState, rewardTree, treeList, MaxNode):
    MaxState = 10
    MaxDepth = 5
    MaxDist = MaxDepth * 1.8
    nodeList = [] #use priority queue here
    
    curState = initState
    curState.path = [] #keep track of action path

    #create the initial nodes for 12 actions, each node has 10 world states
    #TODO: add 10 initial states
    while len(nodeList) < MaxNode:
        stateList =  Expand(curState, treeList, domainList)
        #compute the expected A* reward
        if curState != initState:
            for state in stateList:
                AStarReward = state.reward + state.mario.x - curState.mario.x
                if AStarReward >= MaxDist:
                    #stop when MaxNode reached or find the optimal path (the average reward > MaxDist) 
                    return state.path
                else:
                    heappush(nodeList, (-AStarReward, state)) #heappop returns the smallest item

        #remove a node and expand it
        curState = heappop(nodeList)
    
#WorldState, listof decision trees -> listof ActionState
#treeList includes the reward tree
#sample the effect of all actions for the mario state
def Expand(state, dynaLearner, rewardLearner):
    newStateList = []
    ActionRange = range(12)
    for actionId in ActionRange:
        fea = getModelFeature(actionId, state)
        m = state.mario
        sx, sy, dx, dy = dynaLearner.getClass(fea) #TODO: add randomness here
        reward = rewardLearner.getClass(fea)

        newMario = copy.copy(m)
        newMario.x = m.x + m.sx + dx
        newMario.y = m.y + m.sy + dy
        newMario.sx = sx
        newMario.sy = sy

        newState = state #with static assumption, everything other than mario stays the same
        newState.mario = newMario
        newState.reward = newMario.x - m.x + reward + state.reward
        newState.path.append(actionId)
        newStateList.append(newState)
    return newStateList
        
#def classify(data, treeList, domainList):
    #classNum = len(domainList)
    #partData = [orange.Example(domainList[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(classNum)]
    #res = [treeList[i](partData[i]).value for i in range(classNum)]
    #return res


    
#-------------------UNIT TEST--------------------------
from Test import getDummyObservation
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

if __name__ == '__main__':
    MaxY = 16
    MaxX = 22
    #map = numpy.array([[ord(' ') for x in range(MaxX)] for y in range(MaxY))
    #monList = getDummyMonsterList() 
    #mario = getDummyMario()

    obs = getDummyObservation()
    s = WorldState(obs)

    

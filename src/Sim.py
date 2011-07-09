from WorldState import WorldState
from heapq import heappush, heappop
from Def import *
from FeatureMario import BlockLen
import copy


def Optimize(initState, dynaLearner, rewardLearner, MaxNode):
    print "--------------------"
    #initState.dump()

    MaxState = 10
    MaxDepth = 5
    MaxDist = MaxDepth * 1.8
    nodeList = [] #use priority queue here
    outOfBoundList = []
    
    curState = copy.copy(initState)
    curState.path = [] #keep track of action path
    curState.reward = 0
    AStarReward = 1000
    heappush(nodeList, (AStarReward, curState)) #heappop returns the smallest item


    #create the initial nodes for 12 actions, each node has 10 world states
    #TODO: add 10 initial states
    while ((len(nodeList) + len(outOfBoundList)) < MaxNode):
        #remove a node and expand it
        isOutOfBound = True
        while isOutOfBound and len(nodeList) > 0:
            negAStarReward, curState = heappop(nodeList)
            mario = curState.mario
            x = int(mario.x - curState.origin)
            y = int(mario.y)
            if not x in range(MaxX - BlockLen) or not y in range(MaxY):
                isOutOfBound = True
            else:
                isOutOfBound = False
            if isOutOfBound:
                outOfBoundList.append((negAStarReward, curState))
        if isOutOfBound and len(nodeList) == 0:
            #all nodes are out of bound
            break
        if negAStarReward <= -MaxDist:
            #stop when MaxNode reached or find the optimal path (the average reward > MaxDist) 
            heappush(nodeList, (negAStarReward, curState)) #push the best node back
            break

        stateList =  Expand(curState, dynaLearner, rewardLearner)
        #compute the expected A* reward
        for state in stateList:
            AStarReward = state.reward + state.mario.x - initState.mario.x
            heappush(nodeList, (-AStarReward, state)) #heappop returns the smallest item

        #print "expand ", curState.path
    for node in outOfBoundList:
        heappush(nodeList, node) #heappop returns the smallest item
    negAStarReward, curState = heappop(nodeList)
    print "path", curState.path
    print "a star", -negAStarReward
    #curState.dump()
    if curState.path == []:
        assert(len(outOfBoundList) == 1)
        assert(len(nodeList) == 0) #a special case when mario is out of bound at the init state
        curState.path = [0]
    return curState.path

#WorldState, listof decision trees -> listof ActionState
#treeList includes the reward tree
#sample the effect of all actions for the mario state
def Expand(state, dynaLearner, rewardLearner):
    newStateList = []
    ActionRange = range(12)
    for actionId in ActionRange:
        fea = getTestFeature(state, actionId)
        m = state.mario
        sx, sy, dx, dy = dynaLearner.getClass(fea) #TODO: add randomness here
        reward, = rewardLearner.getClass(fea)

        newMario = copy.deepcopy(m)
        
        newMario.x = m.x + m.sx + dx
        newMario.y = m.y + m.sy + dy
        newMario.sx = sx
        newMario.sy = sy

        newState = copy.copy(state) #with static assumption, everything other than mario stays the same
        newState.path = copy.copy(state.path)
        newState.mario = newMario
        newState.reward = reward + state.reward
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
from ML import getCommonVar, getClassVar, Learner
import orange
from FeatureMario import getTrainFeature, getTestFeature
import tool

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

def TestSim(obs):
    MaxY = 16
    MaxX = 22
    state = WorldState(obs)
    print "mario loc ", state.mario.x, " ", state.mario.y


    commonVar = getCommonVar()
    classVarList = getClassVar()
    rewardVar = orange.FloatVariable("reward")
    isSeparateAction = True
    DynamicLearner = Learner(commonVar, classVarList, isSeparateAction)
    isSeparateAction = False
    RewardLearner = Learner(commonVar, [rewardVar],isSeparateAction)

    lastActionId = 7
    modelFea = getTrainFeature(state, [2.0, 1.0, 0.0, 0.0], lastActionId)
    rewardFea = getTrainFeature(state, [0.0], lastActionId) #don't learn the pseudo reward

    DynamicLearner.add([modelFea])
    RewardLearner.add([rewardFea])
   
    print Optimize(state, DynamicLearner, RewardLearner, 100)
    
if __name__ == '__main__':


    #map = numpy.array([[ord(' ') for x in range(MaxX)] for y in range(MaxY))
    #monList = getDummyMonsterList() 
    #mario = getDummyMario()

    obs = getDummyObservation(10, 16)
    TestSim(obs)
    obsList = tool.Load('obs.db')
    TestSim(obsList[len(obsList)-1])

        
    

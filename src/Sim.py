from WorldState import WorldState
from heapq import heappush, heappop
from Def import *
import copy


def Optimize(initState, dynaLearner, rewardLearner, MaxNode):
    MaxState = 10
    MaxDepth = 5
    MaxDist = MaxDepth * 1.8
    nodeList = [] #use priority queue here
    
    curState = copy.copy(initState)
    curState.path = [] #keep track of action path
    curState.reward = 0

    #create the initial nodes for 12 actions, each node has 10 world states
    #TODO: add 10 initial states
    while len(nodeList) < MaxNode:
        stateList =  Expand(curState, dynaLearner, rewardLearner)
        #compute the expected A* reward
        for state in stateList:
            AStarReward = state.reward + state.mario.x - initState.mario.x
            heappush(nodeList, (-AStarReward, state)) #heappop returns the smallest item

        #remove a node and expand it
        AStarReward, curState = heappop(nodeList)
        if AStarReward >= MaxDist:
            #stop when MaxNode reached or find the optimal path (the average reward > MaxDist) 
            break
        #print "expand ", curState.path
    print "path", curState.path
    print "a star", -AStarReward
    curState.dump()
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
    state = WorldState(obs)


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

        
    

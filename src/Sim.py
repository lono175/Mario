from WorldState import WorldState
from heapq import heappush, heappop
from Def import *
from FeatureMario import BlockLen
import copy
import random

def Optimize(initState, dynaLearner, rewardLearner, MaxNode, PrevPlan):
    print "--------------------"
    #initState.dump()

    MaxState = 10
    MaxDepth = 5
    MinDepth = 3
    MaxDist = 7# usually we can get 8.5 without any barrier
    nodeList = [] #use priority queue here
    outOfBoundList = []
    
    curState = copy.copy(initState)
    curState.path = [] #keep track of action path
    curState.reward = 0
    AStarReward = 1000
    heappush(nodeList, (AStarReward, curState)) #heappop returns the smallest item

    defaultPath = [[9 for x in range(3)], [9, 11, 11], [11, 9, 11], [11, 11, 9], [9, 11, 9], [9, 9, 11]] #right speed and right jump speed

    if PrevPlan != []:
       PrevPlan.pop(0) 
    if PrevPlan != [] and (not PrevPlan in defaultPath):
        defaultPath.append(PrevPlan)
    #TODO: check if default path is valid or not (can jump and same state)

    for path in defaultPath:
        state, isValid =  ExpandPath(path, curState, dynaLearner, rewardLearner)
        if not isValid:
            continue
        #compute the expected A* reward
        AStarReward = state.reward + state.mario.x - initState.mario.x
        heappush(nodeList, (-AStarReward, state)) #heappop returns the smallest item

    #create the initial nodes for 12 actions, each node has 10 world states
    #TODO: add 10 initial states
    while (len(curState.path) < MinDepth) or ((len(nodeList) + len(outOfBoundList)) < MaxNode):
        #remove a node and expand it
        isOutOfBound = True
        while isOutOfBound and len(nodeList) > 0:
            negAStarReward, curState = heappop(nodeList)
            mario = curState.mario
            x = int(mario.x - curState.origin)
            y = int(mario.y)
            #if not x in range(MaxX - BlockLen) or not y in range(MaxY) or len(curState.path) > MaxDepth:
            if len(curState.path) > MaxDepth:
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

        stateList = []
        for actionId in ActionRange:
            newState, isValid =  ExpandPath([actionId], curState, dynaLearner, rewardLearner)
            if isValid:
                 stateList.append(newState)

        #compute the expected A* reward
        for state in stateList:
            if not state.path in defaultPath:
                #don't search the same path again
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
        #assert(len(outOfBoundList) == 1)
        print len(nodeList)
        assert(len(nodeList) == 0) #a special case when mario is out of bound at the init state
        curState.path = [int(random.random()*MaxActionId)]

    PrevPlan = copy.copy(curState.path)
    return curState.path

    
def ExpandPath(path, state, dynaLearner, rewardLearner):
    for actionId in path:
        fea = getTestFeature(state, actionId)
        m = state.mario
        sx, sy, dx, dy = dynaLearner.getClass(fea) #TODO: add randomness here
        sx = round(sx, 1) 
        sy = round(sy, 1)
        dx = round(dx, 1)
        dy = round(dy, 1)
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

        dir, isJump, isSpeed = getActionType(actionId)
        if (not (newState.mario.sy >= 0 and isJump)) and (newState.mario != state.mario): #Jump does not increase y-speed, do not need to search anymore
            state = newState
            isValid = True
        else:
            isValid = False
            break #not a valid action
    return state, isValid

#WorldState, listof decision trees -> listof ActionState
#treeList includes the reward tree
#sample the effect of all actions for the mario state
def Expand(state, dynaLearner, rewardLearner):
    newStateList = []
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

    lastActionId = 9
    modelFea = getTrainFeature(state, [2.0, 1.0, 0.0, 0.0], lastActionId)
    rewardFea = getTrainFeature(state, [0.0], lastActionId) #don't learn the pseudo reward

    DynamicLearner.add([modelFea])
    RewardLearner.add([rewardFea])
   
    print Optimize(state, DynamicLearner, RewardLearner, 100)
def TestSimPath(path, state, dynaLearner, rewardLearner):
    for actionId in path:
        fea = getTestFeature(state, actionId)
        m = state.mario
        sx, sy, dx, dy = dynaLearner.getClass(fea) #TODO: add randomness here
        reward, = rewardLearner.getClass(fea)
        state.dump()
        print "mario: ", m.x, " ", m.y, " ", reward

        newMario = copy.deepcopy(m)
        
        newMario.x = m.x + m.sx + dx
        newMario.y = m.y + m.sy + dy
        newMario.sx = sx
        newMario.sy = sy

        newState = copy.copy(state) #with static assumption, everything other than mario stays the same
        newState.mario = newMario
        state = newState


def TestSimRealAgent():
    MaxY = 16
    MaxX = 22
    agent = tool.Load('mario.db')
    obsList = agent.obsList
    print len(obsList)
    obs = obsList[len(obsList) - 2]
    state = WorldState(obs)
    print "mario loc ", state.mario.x, " ", state.mario.y


    DynamicLearner = agent.DynamicLearner
    RewardLearner = agent.RewardLearner
   
    path = Optimize(state, DynamicLearner, RewardLearner, 100)
    print path
    TestSimPath(path, state, DynamicLearner, RewardLearner)
        
if __name__ == '__main__':



    obs = getDummyObservation(10, 16)
    TestSim(obs)
    #obsList = tool.Load('obs.db')
    #TestSim(obsList[len(obsList)-1])

    #TestSimRealAgent()
   
        
    

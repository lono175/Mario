from WorldState import WorldState
from heapq import heappush, heappop
from Def import *
from FeatureMario import BlockLen
from math import log
import copy
import random
import tool #for debug

#TODO: check id here, no need to have multiple monsterList or gridMap
#TODO: remove x offset and y offset
class SimState(object):
    #listof WorldState (contains all possible outcome of certain path)
    #listof log-likelihood (the probability for each WorldState)
    #listof reward      (the reward for each WorldState)
    #listof int (path)
    def __init__(self):
        self.worldList = []
        #self.probList = []
        self.rewardList = []
        self.path = []
        pass

    def __init__(self, state = None):
        if state == None:
            self.worldList = []
            #self.probList = []
            self.rewardList = []
            self.path = []
        else:
            self.worldList = copy.copy(state.worldList)
            #self.probList = copy.copy(state.probList)
            self.rewardList = copy.copy(state.rewardList)
            self.path = copy.copy(state.path)
    #return the expected reward for all possible path (times probability)
    def reward(self):
        assert(not self.empty())
        #n = max(self.probList)
        #probList = [exp(prob - n) for prob in self.probList]

        #normalize
        #probList = probList / sum(probList)
        return sum(self.rewardList)/len(self.rewardList) #use empirical probability

    def avgX(self):
        x = [world.mario.x for world in self.worldList]

        return sum(x)/len(x)
    def empty(self):
        return self.worldList == []
def MakeSimState(world, MaxState):
    state = SimState()
    state.worldList = [world for i in range(MaxState)] #no need to use copy.copy, since no one will modify it
    state.rewardList = [0 for i in range(MaxState)]
    state.path = [] #keep track of action path
    return state
    
    
#ContDistribution -> val, probability
def GetSample(contDist):
    probList = contDist.values()
    disc = orange.DiscDistribution(probList) 
    index = int(disc.random())
    #prob = probList[index]
    val = contDist.keys()[index]
    return val

#listof int, SimState, Learner, Learner, int -> lisof SimState       
def ExpandPath(path, state, dynaLearner, rewardLearner):
    for actionId in path:
       nextState = SimState()
       for i, world in enumerate(state.worldList):
           fea = getTestFeature(world, actionId)

           #WARNING!! Don't change the order
           reward, = rewardLearner.getClass(fea)
           fea.pop(0)
           distList = dynaLearner[actionId].getClass(fea, orange.GetProbabilities) #TODO: add randomness here
           sampleValue = [GetSample(dist) for dist in distList]
           ax, ay, dx, dy = [round(value, 1) for value in sampleValue]
           #ll = [log(pair[1]) for pair in sampleValue] #loglikelihood

           m = world.mario
           sx = round(ax + m.sx)
           sy = round(ay + m.sy)

           newMario = copy.deepcopy(m)
           newMario.x = m.x + m.sx + dx
           newMario.y = m.y + m.sy + dy
           newMario.sx = sx
           newMario.sy = sy

           newWorld = copy.copy(world) #with static assumption, everything other than mario stays the same
           newWorld.mario = newMario

           dir, isJump, isSpeed = getActionType(actionId)
           if (not (newWorld.mario.sy >= 0 and isJump)) and not (sx == 0.0 and sy == 0.0 and dx == 0.0 and dy == 0.0): #Jump does not increase y-speed, do not need to search anymore
               nextState.worldList.append(newWorld)
               nextState.rewardList.append( state.rewardList[i] + reward)
               #nextState.probList.append(state.probList[i] + sum(ll))

       nextState.path = state.path + [actionId]
       state = nextState
    return state
def getNegAStarReward(state, initWorld):
    return -(state.reward() + state.avgX() - initWorld.mario.x)
    
def Optimize(initWorld, dynaLearner, rewardLearner, MaxNode, PrevPlan, initActionRange):
    print "--------------------"
    #initState.dump()

    MaxState = 3
    MaxDepth = 4
    MinDepth = 3
    MaxDist = 6# usually we can get 8.5 without any barrier
    nodeList = [] #use priority queue here
    outOfBoundList = []

    #create the initial state
    curState = MakeSimState(initWorld, MaxState)

    #for actionId in initActionRange:
        #state =  ExpandPath([actionId], curState, dynaLearner, rewardLearner)
        #if not state.empty():
            #negAStarReward = getNegAStarReward(state, initWorld)
            #heappush(nodeList, (negAStarReward, state)) #heappop returns the smallest item


    #the predefined paths to search
    #right speed(9) and right jump speed(11)
    #only search for the action which is consistent with model-free agent
    defaultPath = [[9 for x in range(3)], [9, 11, 11], [11, 9, 11], [11, 11, 9], [9, 11, 9], [9, 9, 11]] + [[actionId] for actionId in initActionRange] 

    if PrevPlan != []:
        PrevPlan.pop(0) #the first action has been executed

    #heuristic: search for the previous plan first 
    if PrevPlan != [] and (not PrevPlan in defaultPath):
        defaultPath.append(PrevPlan)

    for path in defaultPath:
        if not path[0] in initActionRange:
            continue
        state =  ExpandPath(path, curState, dynaLearner, rewardLearner)
        if not state.empty():
            #compute the expected A* reward
            negAStarReward = getNegAStarReward(state, initWorld)
            heappush(nodeList, (negAStarReward, state)) #heappop returns the smallest item

    #it is possible that nothing left here (all states are not valid)
    if (len(nodeList) > 0):
        negAStarReward, curState = heappop(nodeList)
    else:
        return [initActionRange[random.randint(0, len(initActionRange)-1)]] #nothing we can do, just return a random action

    while (len(curState.path) < MinDepth) or ((len(nodeList) + len(outOfBoundList)) < MaxNode):

        heappush(nodeList, (negAStarReward, curState))

        #remove a node and expand it
        isOutOfBound = False
        while len(nodeList) > 0:
            negAStarReward, curState = heappop(nodeList)
            if len(curState.path) > MaxDepth or curState.reward <= InPitPenalty*0.5: #half of the probability dead is bad enough
                outOfBoundList.append((negAStarReward, curState))
                isOutOfBound = True
            else:
                isOutOfBound = False
                break
        if isOutOfBound and len(nodeList) == 0:
            #all nodes are out of bound or not valid
            break

        if negAStarReward <= -MaxDist:
            #stop when MaxNode reached or find the optimal path (the average reward > MaxDist) 
            heappush(nodeList, (negAStarReward, curState)) #push the best node back
            break

        stateList = []
        for actionId in ActionRange:
            newState =  ExpandPath([actionId], curState, dynaLearner, rewardLearner)
            if not newState.empty():
                stateList.append(newState)

        #compute the expected A* reward
        for state in stateList:

            #don't search the same path again
            if not state.path in defaultPath:
                negAStarReward = getNegAStarReward(state, initWorld)
                heappush(nodeList, (negAStarReward, state)) #heappop returns the smallest item

        negAStarReward, curState = heappop(nodeList)

        #print "expand ", curState.path
    for node in outOfBoundList:
        heappush(nodeList, node) #heappop returns the smallest item

    if len(nodeList) <= 0:
        #impossible
        print "out of bound: ", outOfBoundList
        print initActionRange
        print initWorld.mario.x, " ", initWorld.mario.y
        initWorld.dump()
        tool.Save(initWorld, "dumpWorld.db")
        tool.Save(dynaLearner, "dumpDyna.db")
        tool.Save(rewardLearner, "dumpReward.db")
        tool.Save(initActionRange, "dumpActionRange.db")
        tool.Save(PrevPlan, "dumpPrevPlan.db")
        
    negAStarReward, curState = heappop(nodeList)
    print "path", curState.path
    print "a star", -negAStarReward

    #if curState.path == []:
        #assert(len(outOfBoundList) == 1)
        #print len(nodeList)
        #assert(len(nodeList) == 0) #a special case when mario is out of bound at the init state
        #curState.path = [int(random.random()*MaxActionId)]

    return curState.path


#def ExpandPath(path, state, dynaLearner, rewardLearner):

    #for actionId in path:
        #fea = getTestFeature(state, actionId)

        ##WARNING!! Don't change the order
        #reward, = rewardLearner.getClass(fea)

        #actionId = int(fea[0])
        #fea.pop(0)
        #ax, ay, dx, dy = dynaLearner[actionId].getClass(fea) #TODO: add randomness here
        #ax = round(ax, 1) 
        #ay = round(ay, 1)
        #dx = round(dx, 1)
        #dy = round(dy, 1)

        #m = state.mario

        #sx = round(ax + m.sx, 1)
        #sy = round(ay + m.sy, 1)
        #newMario = copy.deepcopy(m)

        #newMario.x = m.x + m.sx + dx
        #newMario.y = m.y + m.sy + dy
        #newMario.sx = sx
        #newMario.sy = sy

        #newState = copy.copy(state) #with static assumption, everything other than mario stays the same
        #newState.path = copy.copy(state.path)
        #newState.mario = newMario
        #newState.reward = reward + state.reward
        #newState.path.append(actionId)

        #dir, isJump, isSpeed = getActionType(actionId)
        #if (not (newState.mario.sy >= 0 and isJump)) and not (sx == 0.0 and sy == 0.0 and dx == 0.0 and dy == 0.0): #Jump does not increase y-speed, do not need to search anymore
            #if newState.mario.sx == 0.0 and newState.mario.sy == 0.0 and dx == 0.0 and dy == 0.0:
                #print "Mario Warning: ", newState.mario.sx, " ", newState.mario.sy, " ", newState.mario.x, " ", newState.mario.y
            #state = newState
            #isValid = True
        #else:
            #isValid = False
            #break #not a valid action
    #return state, isValid

#WorldState, listof decision trees -> listof ActionState
#treeList includes the reward tree
#sample the effect of all actions for the mario state
#def Expand(state, dynaLearner, rewardLearner):
    #newStateList = []
    #for actionId in ActionRange:
        #fea = getTestFeature(state, actionId)
        #m = state.mario
        #sx, sy, dx, dy = dynaLearner.getClass(fea) #TODO: add randomness here
        #reward, = rewardLearner.getClass(fea)

        #newMario = copy.deepcopy(m)
        #
        #newMario.x = m.x + m.sx + dx
        #newMario.y = m.y + m.sy + dy
        #newMario.sx = sx
        #newMario.sy = sy

        #newState = copy.copy(state) #with static assumption, everything other than mario stays the same
        #newState.path = copy.copy(state.path)
        #newState.mario = newMario
        #newState.reward = reward + state.reward
        #newState.path.append(actionId)
        #newStateList.append(newState)
    #return newStateList

#def classify(data, treeList, domainList):
    #classNum = len(domainList)
    #partData = [orange.Example(domainList[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(classNum)]
    #res = [treeList[i](partData[i]).value for i in range(classNum)]
    #return res



#-------------------UNIT TEST--------------------------
from Test import getDummyObservation
from ML import getCommonVar, getClassVar, Learner
import orange
from FeatureMario import getTrainFeature, getTestFeature, getModelFeature
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
    RewardLearner = Learner(commonVar, [rewardVar],3000)
    commonVar.pop(0)
    DynamicLearner = Learner(commonVar, classVarList, 3000)

    lastActionId = 9
    modelFea = getModelFeature(state, [2.0, 1.0, 0.0, 0.0])
    rewardFea = getTrainFeature(state, [0.0], lastActionId) #don't learn the pseudo reward

    DynamicLearner.add([modelFea])
    RewardLearner.add([rewardFea])

    dynaLearner = [DynamicLearner for action in range(12)]
    path =  Optimize(state, dynaLearner, RewardLearner, 100, [], ActionRange)
    newState =  ExpandPath(path, MakeSimState(state, 10), dynaLearner, RewardLearner)
    print type(newState)
    print "hello"
    for world in newState.worldList:
        print "loc: ", world.mario.x
    
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

    path = Optimize(state, DynamicLearner, RewardLearner, 100, [], ActionRange)
    print path
    TestSimPath(path, state, DynamicLearner, RewardLearner)

if __name__ == '__main__':



    obs = getDummyObservation(10, 16)
    TestSim(obs)
    #obsList = tool.Load('obs.db')
    #TestSim(obsList[len(obsList)-1])

    #TestSimRealAgent()




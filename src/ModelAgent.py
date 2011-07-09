import random
import orange
from rlglue.agent.Agent import Agent
from Def import getAllAction, makeAction, getActionId, dumpAction
from rlglue.types import Action
from LinearSARSA import LinearSARSA
from ML import getCommonVar, getClassVar, Learner
from WorldState import WorldState
from FeatureMario import getSarsaFeature, getTrainFeature, getTestFeature
from Sim import Optimize

class ModelAgent(Agent):
    def __init__(self):
        print "init"
        random.seed(0)
        actionList = getAllAction()
        initialQ = 0
        dumpCount = 100000
        self.agent = LinearSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
        #self.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
        self.totalStep = 0
        self.rewardList = []
        self.distList = []
        self.feaList = []
        self.rewardFeaList = []
        self.episodeNum = 0

        commonVar = getCommonVar()
        classVarList = getClassVar()
        rewardVar = orange.FloatVariable("reward")
        isSeparateAction = True
        self.DynamicLearner = Learner(commonVar, classVarList, isSeparateAction)
        isSeparateAction = False
        self.RewardLearner = Learner(commonVar, [rewardVar],isSeparateAction)
        
    def planning(self, state):
        MaxNode = 100
        path = Optimize(state, self.DynamicLearner, self.RewardLearner, MaxNode)
        return makeAction(path[0])

    def agent_init(self, taskSpecString):

        #parse action
        print "begin: ", self.totalStep
        print "feaNum", len(self.feaList)
        
        if self.DynamicLearner == []:
            commonVar = getCommonVar()
            classVarList = getClassVar()
            rewardVar = orange.FloatVariable("reward")
            isSeparateAction = True
            self.DynamicLearner = Learner(commonVar, classVarList, isSeparateAction)
            isSeparateAction = False
            self.RewardLearner = Learner(commonVar, [rewardVar],isSeparateAction)

        #retrain the classifier for each different run
        self.DynamicLearner.add(self.feaList)
        self.RewardLearner.add(self.rewardFeaList)

    def agent_start(self, obs):
        state = WorldState(obs)
        self.lastState = state
        if self.DynamicLearner.empty() or self.RewardLearner.empty():
            fea = getSarsaFeature(obs)
            action = self.agent.start(fea)
        else:
            action = self.planning(state)
        self.stepNum = 0
        self.lastAction = action
        return action

    def agent_step(self, reward, obs):
        #if reward < -0.01 + episilon and reward > -0.01 - episilon:
            #reward = -1

        state = WorldState(obs)
        lastMario = self.lastState.mario
        mario = state.mario #for internal reward system
        #print "loc:", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
        dx = mario.x - lastMario.x

        reward = reward + dx
        if self.DynamicLearner.empty() or self.RewardLearner.empty():
            fea = getSarsaFeature(obs)
            action = self.agent.step(reward, fea)
        else:
            action = self.planning(state)
            print "planning", dumpAction(action)

        lastActionId = getActionId(self.lastAction)

        deltaX = mario.x - (lastMario.x + lastMario.sx)
        deltaY = mario.y - (lastMario.y + lastMario.sy)
        
        modelFea = getTrainFeature(self.lastState, [round(mario.sx, 1), round(mario.sy, 1), round(deltaX, 1), round(deltaY, 1)], lastActionId)
        rewardFea = getTrainFeature(self.lastState, [0], lastActionId) #don't learn the pseudo reward

        if not self.DynamicLearner.empty():
            print "feature: ", modelFea
            print "predict: ", self.DynamicLearner.getClass(modelFea)
        if not self.RewardLearner.empty():
            print "reward: ", reward
            preReward, = self.RewardLearner.getClass(rewardFea)
            print "pre reward: ", preReward

        #assert(self.treeList != [])
        #if self.treeList != []:
            #pass
            #print self.treeList
            #print "feature: ", modelFea
            #print "predict: ", classify(modelFea, self.treeList, self.domainList)
            #print "reward: ", reward
        #if self.rewardTreeList != []:
            #print "predict reward: ",  classifyRewardDomain(rewardFea, self.rewardTreeList[0], self.rewardDomain)

            #print "test feaL ", self.feaList[0]
            #print "test predict: ", classify(self.feaList[0], self.treeList, self.domainList)
        self.feaList.append(modelFea)
        self.rewardFeaList.append(rewardFea)

        self.lastState = state
        self.lastAction = action

        self.stepNum = self.stepNum + 1

        return action

    def agent_end(self,reward):
        if reward == -10.0:
            reward = -50.0

        lastActionId = getActionId(self.lastAction)
        rewardFea = getTrainFeature(self.lastState, [round(reward, 1)], lastActionId) #don't learn the pseudo reward

        self.rewardFeaList.append(rewardFea)

        if not self.RewardLearner.empty():
            preReward, = self.RewardLearner.getClass(rewardFea)
            print "pre reward: ", reward

        print "end: ", reward, " step: ", self.stepNum, " dist:", self.lastState.mario.x
        self.totalStep = self.totalStep + self.stepNum

        if self.DynamicLearner.empty() or self.RewardLearner.empty():
            self.agent.end(reward)

        self.rewardList.append(reward)
        self.distList.append(self.lastState.mario.x)
        self.episodeNum = self.episodeNum + 1

        #print the decision tree
        #treeList = getClassifier(self.feaList)
        #for tree in treeList:
        #printTree(treeList[2])
        #res =  classify(data, treeList)
        
        if self.episodeNum % 10000 == 0:
            print "dump:", self.episodeNum
            tool.Save(self, "mario" + str(self.episodeNum) + ".db")
            
    def agent_cleanup(self):
        pass

    def agent_freeze(self):
        pass

    def agent_message(self,inMessage):
        return None


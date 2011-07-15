import random
import orange
from rlglue.agent.Agent import Agent
from Def import getAllAction, makeAction, dumpAction, InPitPenalty, DeathPenalty
from rlglue.types import Action
#from LinearSARSA import LinearSARSA
#from LinearHORDQ import LinearHORDQ
from LambdaHORDQ import LambdaHORDQ
from ML import getCommonVar, getClassVar, Learner, ActionLearner
from WorldState import WorldState
from FeatureMario import getSarsaFeature, getTrainFeature, getTestFeature, isMarioInPit
from Sim import Optimize

NoTask = -1
MaxStepReward = 2.0 
class ModelAgent(Agent):
    def __init__(self):
        print "init"
        random.seed(0)
        self.actionList = getAllAction()
        pseudoReward = 5
        self.initPseudoReward = pseudoReward
        gamma = 0.8
        episilon = 0.00 #disable exploration for HORDQ
        alpha = 0.05
        #initialQ = MaxStepReward/(1-gamma)
        initialQ = 0
        dumpCount = 100000
        #self.agent = LinearHORDQ(0.05, 0.1, 0.8, self.actionList, initialQ, dumpCount, pseudoReward)
        self.agent = LambdaHORDQ(alpha, episilon, gamma, self.actionList, initialQ, dumpCount, pseudoReward)
        #self.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
        self.totalStep = 0
        self.rewardList = []
        self.distList = []
        self.feaList = []
        self.rewardFeaList = []
        self.episodeNum = 0
        self.epsilon = 0.05 #TODO: disable the exploration here

        commonVar = getCommonVar()
        classVarList = getClassVar()
        rewardVar = orange.FloatVariable("reward")
        self.RewardLearner = Learner(commonVar, [rewardVar])
        commonVar.pop(0)
        self.DynamicLearner = ActionLearner(commonVar, classVarList)

        self.lastPlan = []

        #self.obsList = [] #TODO: remove me
        
    def planning(self, state, initActionRange):
        MaxNode = 2000
        path = Optimize(state, self.DynamicLearner, self.RewardLearner, MaxNode, self.lastPlan, initActionRange)
        self.lastPlan = path
        return path[0]

    def agent_init(self, taskSpecString):

        #parse action
        print "begin: ", self.totalStep
        print "feaNum", len(self.feaList)
        
        if self.DynamicLearner == []:
            commonVar = getCommonVar()
            classVarList = getClassVar()
            rewardVar = orange.FloatVariable("reward")
            self.RewardLearner = Learner(commonVar, [rewardVar])
            commonVar.pop(0)
            self.DynamicLearner = ActionLearner(commonVar, classVarList)

        #retrain the classifier for each different run
        self.DynamicLearner.add(self.feaList)
        self.RewardLearner.add(self.rewardFeaList)

    def agent_start(self, obs):
        state = WorldState(obs)
        self.lastState = state
        fea = getSarsaFeature(state, NoTask)
        if self.DynamicLearner.empty() or self.RewardLearner.empty():
            action = self.agent.start(fea, NoTask)
        else:
            possibleAction = self.agent.getPossibleAction(fea)
            action = self.planning(state, possibleAction)
            action = self.agent.start(fea, action)
        self.stepNum = 0
        self.lastAction = action
        return makeAction(action)

    def agent_step(self, reward, obs):
        #self.obsList.append(obs)
        #if reward < -0.01 + episilon and reward > -0.01 - episilon:
            #reward = -1

        state = WorldState(obs)
        fea = getSarsaFeature(state, self.lastAction)
        lastMario = self.lastState.mario
        mario = state.mario #for internal reward system
        #print "loc:", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
        dx = mario.x - lastMario.x

        reward = reward + dx
        modelReward = 0
        if isMarioInPit(state):
            print "in pit !!!!!!!"
            #reward = reward + InPitPenalty #no pit penalty for HORDQ
            modelReward = InPitPenalty
        if self.DynamicLearner.empty() or self.RewardLearner.empty():
            #fea = getSarsaFeature(obs)
            action = self.agent.step(reward, fea, NoTask)
        else:
            #episilon greey policy
            if random.random() < self.epsilon:
                #select randomly
                action = self.actionList[int(random.random()*len(self.actionList))]
            else:
                possibleAction = self.agent.getPossibleAction(fea)
                if fea[0] == ():
                    possibleAction == self.actionList
                action = self.planning(state, possibleAction)

            print "planning", action
            self.agent.pseudoReward = 10000
            action = self.agent.step(reward, fea, action)
            self.agent.pseudoReward = self.initPseudoReward
            print "HORDQ", action

        lastActionId = self.lastAction

        deltaX = mario.x - (lastMario.x + lastMario.sx)
        deltaY = mario.y - (lastMario.y + lastMario.sy)
        
        classVar = [round(mario.sx, 1), round(mario.sy, 1), round(deltaX, 1), round(deltaY, 1)]
        rewardClassVar = [round(modelReward, 0)]
        modelFea = getTrainFeature(self.lastState, classVar, lastActionId)
        rewardFea = getTrainFeature(self.lastState, rewardClassVar, lastActionId) #don't learn the pseudo reward

        if not self.DynamicLearner.empty():
            predictModelClass = self.DynamicLearner.getClass(modelFea)
            predictModelClass = [round(v, 1) for v in predictModelClass]
            print "feature: ", modelFea
            print "predict: ", predictModelClass
            if not classVar == predictModelClass:
                self.feaList.append(modelFea)
            else:
                print "pass model-------------"
        else:
            self.feaList.append(modelFea)


        if not self.RewardLearner.empty():
            predictRewardClass = self.RewardLearner.getClass(rewardFea)
            predictRewardClass = [round(v, 1) for v in predictRewardClass]
            print "reward: ", modelReward
            print "pre reward: ", predictRewardClass
            if not rewardClassVar == predictRewardClass:
                self.rewardFeaList.append(rewardFea)
            else:
                print "pass reward-------------"
        else:
            self.rewardFeaList.append(rewardFea)

        self.lastState = state
        self.lastAction = action

        self.stepNum = self.stepNum + 1


        return makeAction(action)

    def agent_end(self,reward):
        modelReward = reward
        if reward == -10.0:
            reward = DeathPenalty
            modelReward = InPitPenalty

        lastActionId = self.lastAction
        rewardFea = getTrainFeature(self.lastState, [round(modelReward, 1)], lastActionId) #don't learn the pseudo reward

        self.rewardFeaList.append(rewardFea)

        if not self.RewardLearner.empty():
            preReward, = self.RewardLearner.getClass(rewardFea)
            print "pre reward: ", reward

        print "end: ", reward, " step: ", self.stepNum, " dist:", self.lastState.mario.x
        self.totalStep = self.totalStep + self.stepNum

        #if self.DynamicLearner.empty() or self.RewardLearner.empty():
        self.agent.end(reward)
        #else:
            #self.agent.end(reward)
            

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


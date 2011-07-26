import random
import orange
from rlglue.agent.Agent import Agent
from Def import getAllAction, makeAction, dumpAction, InPitPenalty, DeathPenalty, Precision
from rlglue.types import Action
#from LinearSARSA import LinearSARSA
#from LinearHORDQ import LinearHORDQ
from LambdaHORDQ import LambdaHORDQ
from RewardSarsa import RewardSarsa
from ML import getCommonVar, getClassVar, Learner
from WorldState import WorldState
from FeatureMario import getSarsaFeature, getTrainFeature, getTestFeature, isMarioInPit, getModelFeature, getRewardFeature
from Sim import Optimize, ExpandPath
from numpy import array 
import tool
import orngTree
import pickle #for agent_message
NoTask = -1
MaxStepReward = 2.0 

#TODO: only add features before the agent's death???
#TODO: test the power of HORDQ with complex pits
#TODO: use Q value of HORDQ as the reward
#TODO: systematically test the agents performance of certain features (to spikey: do we need to add monsters speed into concern?)
#TODO: gradually reduce the epsilon, otherwise the model agent will be stucked, (or hard-coded some random policy??)(or retrain after certain steps)

HybridAgent = 0
SarsaAgent = 1
ModelAgent = 2
class ModelAgent(Agent):
    def __init__(self):
        self.actionList = getAllAction()
        gamma = 0.8

        alpha = 0.05
        #initialQ = MaxStepReward/(1-gamma)
        initialQ = 0
        dumpCount = 100000
        #self.agent = LinearHORDQ(0.05, 0.1, 0.8, self.actionList, initialQ, dumpCount, pseudoReward)
        self.agent = LambdaHORDQ(alpha, 0.05, gamma, self.actionList, initialQ, dumpCount, 0)
        self.rewardAgent = RewardSarsa(alpha, 0.05, 0, self.actionList, initialQ, dumpCount)
        #self.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
        self.totalStep = 0
        self.rewardList = []
        self.distList = []

        self.feaList = {}
        for action in self.actionList:
            self.feaList[action] = []

        self.rewardFeaList = []
        self.episodeNum = 0


        self.lastPlan = []
        self.DynamicLearner = {}

        self.obsList = [] #TODO: remove me
        
    def agent_message(self, inMessage):
        #if at the very begining, init everything
        
        print "heelo"
        print inMessage
        print "type: ", type(inMessage)
        print pickle.loads(inMessage)
        #print inMessage
        return "yes"
    
    def AgentType(self):
        return self.agentType

    #return True when we can start using our model
    def isModelReady(self):
        if self.AgentType() == SarsaAgent:
            return False
        if self.DynamicLearner == {} or self.DynamicLearner[0].empty():
            return False
        return True

    #prune both dynamic and reward data
    def prune(self):
        for action in self.actionList:
            self.feaList[action], self.DynamicLearner[action].treeList = self.DynamicLearner[action].prune(self.feaList[action])
            print "action learner ", action, "  nodes: ", orngTree.countNodes(self.DynamicLearner[action].treeList[0])
            print "action learner leaves: ", self.DynamicLearner[action].treeList[0].count_leaves()
        #self.rewardFeaList, self.RewardLearner.treeList = self.RewardLearner.prune(self.rewardFeaList)
        #print "reward learner nodes: ", orngTree.countNodes(self.RewardLearner.treeList[0])
        #print "reward learner leaves: ", self.RewardLearner.treeList[0].count_leaves()

        
    def planning(self, state, initActionRange):
        if len(initActionRange) == 1:
            #nothing to choose
            return initActionRange[0]

        MaxNode = 300
        path = Optimize(state, self.DynamicLearner, self.rewardAgent, MaxNode, self.lastPlan, initActionRange)
        self.lastPlan = path
        return path[0]

    def initLearner(self):
        if self.DynamicLearner == {}:
            commonVar = getCommonVar()
            classVarList = getClassVar()
            #rewardVar = orange.FloatVariable("reward")
            #self.RewardLearner = Learner(commonVar, [rewardVar], 6000)
            commonVar.pop(0)
            for action in self.actionList:
                if action == 9:
                    maxFeature = 6000
                else:
                    maxFeature = 3000
                self.DynamicLearner[action] = Learner(commonVar, classVarList, maxFeature)

    def agent_init(self, taskSpecString):

        random.seed()
        #self.agentType = SarsaAgent
        self.agentType = ModelAgent
        print "init"
        print "type", self.agentType

        #too hacky

        if self.agentType == SarsaAgent:
            self.HORDQ_episilon = 0.01 #disable exploration for HORDQ
        else:
            self.HORDQ_episilon = 0.00 #disable exploration for HORDQ
        
        self.epsilon = 0.01 #TODO: disable the exploration here
        pseudoReward = 5
        print "pseudo reward: ", pseudoReward
        self.initPseudoReward = pseudoReward
        self.agent.pseudoReward = pseudoReward

        #parse action
        print "begin: ", self.totalStep
        feaNum = len(self.feaList[9])
        print "feaNum", feaNum

        print "SARSA Num:", len(self.agent.Q)

        self.initLearner()
        if feaNum == 0:
            return
        
        if not self.AgentType() == SarsaAgent:
            self.prune()

        #retrain the classifier for each different run
        #for action in self.actionList:
            #self.DynamicLearner[action].add(self.feaList[action])
        #self.RewardLearner.add(self.rewardFeaList)

    def agent_start(self, obs):
        state = WorldState(obs)
        self.lastState = state
        fea = getSarsaFeature(state, NoTask)
        if not self.isModelReady():
            if not self.AgentType() == SarsaAgent:
                self.agent.epsilon = 0.05 #encourage exploration

            action = self.agent.start(fea, NoTask)
        else:
            print self.isModelReady()
            self.agent.epsilon = self.HORDQ_episilon
            possibleAction = self.agent.getPossibleAction(fea)
            action = self.planning(state, possibleAction)
            action = self.agent.start(fea, action)
        rewardFea = getRewardFeature(state, NoTask)
        self.rewardAgent.start(rewardFea, action)
        self.stepNum = 0
        self.lastAction = action
        return makeAction(action)

    def agent_step(self, reward, obs):
        #self.obsList.append(obs)
        #if reward < -0.01 + epsilon and reward > -0.01 - epsilon:
            #reward = -1

        state = WorldState(obs)

        fea = getSarsaFeature(state, self.lastAction)
        lastMario = self.lastState.mario
        mario = state.mario #for internal reward system
        dx = mario.x - lastMario.x

        reward = reward + dx
        modelReward = 0
        if isMarioInPit(state):
            print "in pit !!!!!!!"
            #reward = reward + InPitPenalty #no pit penalty for HORDQ
            modelReward = InPitPenalty
        if not self.isModelReady():
            #fea = getSarsaFeature(obs)
            action = self.agent.step(reward, fea, NoTask)
        else:
            #episilon greey policy
            if random.random() < self.epsilon:
                #select randomly
                action = self.actionList[int(random.random()*len(self.actionList))]
                print "random!!"
            else:
                possibleAction = self.agent.getPossibleAction(fea)
                #if fea[0] == (): #if not monster around, pass control to the planner
                    #possibleAction = self.actionList
                action = self.planning(state, possibleAction)

            print "planning", action
            self.agent.pseudoReward = 10000
            action = self.agent.step(reward, fea, action)
            self.agent.pseudoReward = self.initPseudoReward
        #state.dump()
        print "step loc:",  self.stepNum, " ", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
        #state.path = []
        #state.reward = 0

        #nextState, isValid =  ExpandPath([0], state, self.DynamicLearner, self.RewardLearner)

        #nextState.dump()
        #print "pred loc:", nextState.mario.x , " ", nextState.mario.y, " ", nextState.mario.sx, " ", nextState.mario.sy
        #print "backoff reward: ", nextState.reward

        #nextState, isValid =  ExpandPath([action], state, self.DynamicLearner, self.RewardLearner)
        #nextState.dump()
        #print "pred loc:", nextState.mario.x , " ", nextState.mario.y, " ", nextState.mario.sx, " ", nextState.mario.sy
        #print "pred rewar:", action, " ", nextState.reward



        lastActionId = self.lastAction

        deltaX = mario.x - (lastMario.x + lastMario.sx)
        deltaY = mario.y - (lastMario.y + lastMario.sy)
        aX = mario.sx - lastMario.sx 
        aY = mario.sy - lastMario.sy 
        
        classVar = [round(aX, Precision), round(aY, Precision), round(deltaX, Precision), round(deltaY, Precision)]
        rewardClassVar = [round(modelReward, 0)]
        modelFea = getModelFeature(self.lastState, classVar)
        #rewardFea = getTrainFeature(self.lastState, rewardClassVar, lastActionId) #don't learn the pseudo reward

        if self.isModelReady(): #TODO: too dirty

            #predictModelClass = self.DynamicLearner[lastActionId].getClass(modelFea)
            #predictModelClass = [round(v, 1) for v in predictModelClass]
            #print "feature: ", lastActionId, " ", modelFea
            #print "predict: ", predictModelClass
            predictModelClass = self.DynamicLearner[lastActionId].getClass(modelFea)
            predictModelClass = [round(v, 1) for v in predictModelClass]
            roundClassVar = [round(v, 1) for v in classVar]
            print "feature: ", lastActionId, " ", modelFea
            print "predict: ", predictModelClass
            if not roundClassVar == predictModelClass:
                self.feaList[lastActionId].append(modelFea)
            else:
                print "pass model-------------"
        else:
            if not self.AgentType() == SarsaAgent:
                self.feaList[lastActionId].append(modelFea)


        rewardFea = getRewardFeature(state, self.lastAction)
        print "before pre reward: ", self.rewardAgent.getQ(rewardFea, action)
        self.rewardAgent.step(rewardFea, modelReward, action)
        print "pre reward: ", self.rewardAgent.getQ(rewardFea, action)
        print "reward: ", modelReward
        #if self.isModelReady():
            #predictRewardClass = self.RewardLearner.getClass(rewardFea)
            #predictRewardClass = [round(v, 0) for v in predictRewardClass]
            #print "reward: ", modelReward
            #print "pre reward: ", predictRewardClass
            #if not rewardClassVar == predictRewardClass:
                #self.rewardFeaList.append(rewardFea)
            #else:
                #print "pass reward-------------"
        #else:
            #if not self.AgentType() == SarsaAgent:
                #self.rewardFeaList.append(rewardFea)

        self.lastState = state
        self.lastLastAction = self.lastAction
        self.lastAction = action

        self.stepNum = self.stepNum + 1


        return makeAction(action)

    def agent_end(self, reward):
        modelReward = reward
        if reward == -10.0:
            reward = DeathPenalty
            modelReward = InPitPenalty

        lastActionId = self.lastAction
        #rewardFea = getTrainFeature(self.lastState, [round(modelReward, 0)], lastActionId) #don't learn the pseudo reward

        #if not self.AgentType() == SarsaAgent:
            #self.rewardFeaList.append(rewardFea)

        #if self.isModelReady():
            #preReward, = self.RewardLearner.getClass(rewardFea)
            #print "pre reward: ", reward

        rewardFea = getRewardFeature(self.lastState, self.lastLastAction)
        print "before pre reward: ", self.rewardAgent.getQ(rewardFea, self.lastAction)
        self.agent.end(reward)
        self.rewardAgent.end(round(modelReward, 0))
        print "pre reward: ", self.rewardAgent.getQ(rewardFea, self.lastAction)

        print "end: ", reward, " step: ", self.stepNum, " dist:", self.lastState.mario.x
        self.episodeNum = self.episodeNum + 1
        self.totalStep = self.totalStep + self.stepNum

        #if self.DynamicLearner.empty() or self.RewardLearner.empty():
        #else:
            #self.agent.end(reward)
            

        self.rewardList.append(reward)
        self.distList.append((self.totalStep, self.lastState.mario.x, self.episodeNum))

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



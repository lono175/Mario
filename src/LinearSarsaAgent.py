
class LinearSarsaAgent(Agent):

    def __init__(self):
        print "init"
        random.seed(0)
        actionList = getAllAction()
        initialQ = 0
        dumpCount = 100000
        #self.agent = LinearSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
        self.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
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
        
    def agent_init(self, taskSpecString):

        #parse action
        print "begin: ", self.totalStep
        print "Q", len(self.agent.Q)

        #retrain the classifier for each different run
        self.DynamicLearner.Add(self.feaList)
        self.RewardLearner.Add(self.rewardFeaList)

    def agent_start(self, obs):
        state = WorldState(obs)
        fea = getSarsaFeature(obs)
        self.lastState = state
        action = self.agent.start(fea)
        self.stepNum = 0
        self.lastAction = action
        return action

    def agent_step(self, reward, obs):
        if reward < -0.01 + episilon and reward > -0.01 - episilon:
            reward = -1

        state = WorldState(obs)
        lastMario = self.lastState.mario
        #print obs.intArray
        #print reward
        #mario = self.getMario(obs)
        fea = getSarsaFeature(obs)
        mario = state.mario #for internal reward system
        #print "loc:", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
        dx = mario.x - lastMario.x

        #let mario finish the level as fast as possible
        #reward = reward + dx*0.5
        #if dx < 0:
            #dx = dx/2
        reward = reward + dx
        #print "reward: ", reward
        #print fea
        action = self.agent.step(reward, fea)

        #print self.agent.actionList
        #print self.totalStep, "---------------"
        #dumpActionList(self.agent.actionList)
        #print "Q: ", self.agent.getQ(fea, action)
        #print "action:", dumpAction(action)
        #print "Constant Q: ", dumpList(getConstantQ(obs, self.agent))
        #print "monst fea: ", getMonsterFeatureList(obs)
        #print "Monster Q: ", dumpList(getMonsterQ(obs, self.agent))
        #print "TileQ: ", dumpList(getGridQ(obs, self.agent))
        #ind = 0
        #halfLen = 1
        #locList = getReducedRegularGridShape(int(mario.x - getOrigin(obs)), int(mario.y), halfLen)
        #map = getMonsterGridMap(obs)
        #print "marioLoc: ", (mario.x, mario.y)
        #for loc in locList:
            #fea = getGridFeature(map, loc[0], loc[1], halfLen)
            #print fea
            #print "TileQ: ", loc, " ",dumpList(getGridQInd(obs, self.agent, ind))
            #ind = ind + 1


                #print "TileQ: ", ind, " ",dumpList(getGridQInd(obs, self.agent, ind))
        #for ind in range(0, 7):
            #print "TileQ: ", ind, " ",dumpList(getGridQInd(obs, self.agent, ind))


        #dumpAction(action)

        #get feature for classifier here

        lastActionId = getActionId(self.lastAction)

        deltaX = mario.x - (lastMario.x + lastMario.sx)
        deltaY = mario.y - (lastMario.y + lastMario.sy)
        
        modelFea = getTrainFeature(self.lastState, [round(mario.sx, 1), round(mario.sy, 1), round(deltaX, 1), round(deltaY, 1)], lastActionId)
        rewardFea = getTrainFeature(self.lastState, [0], lastActionId) #don't learn the pseudo reward

        if not self.dynaLearner.empty():
            print "feature: ", modelFea
            print "predict: ", self.dynaLearner.getClass(modelFea)
        if not self.rewardLearner.empty():
            print "reward: ", reward
            preReward, = self.rewardLearner.getClass(rewardFea)

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
        #if self.rewardTreeList != []:
            #print "predict reward: ",  classifyRewardDomain(rewardFea, self.rewardTreeList[0], self.rewardDomain)

        print "end: ", reward, " step: ", self.stepNum, " dist:", self.lastState.x
        self.totalStep = self.totalStep + self.stepNum
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

    def randomify(self):
        self.action.intArray = []
        self.action.doubleArray = []


        for min_action,max_action in self.int_action_ranges:                    
            act = random.randrange(min_action,max_action+1)
            self.action.intArray.append(act)

        for min_action,max_action in self.double_action_ranges:                    
            act = random.uniform(min_action,max_action)
            self.action.doubleArray.append(act)

        self.action.charArray = GenPasswd2(self.action.numChars)
        #print self.action.intArray
        #print self.action.doubleArray
        #print self.action.charArray

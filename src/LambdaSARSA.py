import random
import copy
#TODO: check if my implementation is correct or not
#TODO: add dynamic episilon
#TODO: optimistic exploration with reduce epislon?
class LambdaSARSA:
    def __init__(self, alpha, epsilon, gamma, actionList, initialQ, dumpCount ):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.actionList = actionList
        self.initialQ = initialQ
        self.Q = {}
        self.dumpCount = dumpCount
        self.episodeNum = 0
        self.isUpdate = True
        self.lam = 0.9
        self.smallLambda = 0.1
    def touchAll(self, observation):
        for action in self.actionList:
            self.touch(observation, action)

    #listof feature -> void
    def touch(self, observation, action):
        for fea in observation:
            key = (fea, action)
            if not key in self.Q:
                self.Q[key] = self.initialQ #may use optimistic exploration

    def selectAction(self, observation):
        #use epsilon-greedy
        if random.random() < self.epsilon:
            #select randomly
            action = self.actionList[int(random.random()*len(self.actionList))]
            return action
        else:
            #select the best action
            v = []
            for action in self.actionList:
                v.append(self.getQ(observation, action))
            assert len(v) > 0
            m = max(v)
            select = int(random.random()*v.count(m))

            i = 0
            maxCount = 0
            for value in v:
                if value == m:
                    if maxCount == select:
                        action = self.actionList[i]
                        break
                    maxCount = maxCount + 1
                i = i + 1
            return action

    def getAllQ(self, ob):
        Q = []
        for action in self.actionList:
            Q.append(self.getQ(ob, action))
        return Q

    def getQ(self, ob, action):
        self.touch(ob, action)
        Q = 0
        for fea in ob:
            Q = Q + self.Q[(fea, action)]
        return Q
        
    def update(self, lastObservation, lastAction, reward, observation, action):
        newQ = self.getQ(observation, action)
        oldQ = self.getQ(lastObservation, lastAction)
        delta = reward + self.gamma * newQ - oldQ
        #print "newQ: ", newQ, " ", (action.intArray[0], action.intArray[1], action.intArray[2])
        #print "oldQ: ", oldQ, " ", (lastAction.intArray[0], lastAction.intArray[1], lastAction.intArray[2])
        self.updateQ(lastObservation, lastAction, delta)

    def updateQ(self, lastObservation, lastAction, delta):
        self.touch(lastObservation, lastAction)
        numOfFeature = len(lastObservation)
        assert (numOfFeature >= 1)
        deltaPerFeature = delta/numOfFeature

        #print "delta: ", deltaPerFeature
        for fea in lastObservation:
            key = (fea, lastAction)
            self.Q[key] = self.Q[key] + self.alpha*deltaPerFeature*self.trace[key]
            #self.Q[key] = self.Q[key] + self.alpha*deltaPerFeature
        
    def clearTrace(self):
        self.trace = {}

    def addTrace(self, ob, action):
        for fea in ob:
            key = (fea, action)
            self.trace[key] = 1
            #set all other actions to 0
            for otherAction in self.actionList:
                if otherAction == action:
                    continue
                otherKey = (fea, otherAction)
                if otherKey in self.trace:
                    del self.trace[otherKey]
                    #self.trace[otherKey] = 0
    def updateTrace(self):
        toRemove = []
        for key in self.trace:
            val = self.lam*self.trace[key] 
            if val < self.smallLambda:
                toRemove.append(key)
            else:
                self.trace[key] = val
        for key in toRemove:
            del self.trace[key]
                
    def start(self, observation):
        self.clearTrace()

        ob = observation
        self.lastObservation = ob
        self.touchAll(ob)
        self.lastAction = self.selectAction(ob)
        self.episodeNum = self.episodeNum + 1
        self.addTrace(ob, self.lastAction)
        return self.lastAction

    #listof feature -> action
    def setUpdate(self, isUpdate):
        self.isUpdate = isUpdate

    def step(self, reward, observation):
        ob = observation
        self.touchAll(ob)
        newAction = self.selectAction(ob)
        if self.isUpdate:
            self.update(self.lastObservation, self.lastAction, reward, ob, newAction)
            self.updateTrace()
            self.addTrace(ob, newAction)
        self.lastObservation = ob
        self.lastAction = newAction
        return newAction

    def end(self, reward):
        if self.isUpdate:
            oldQ = self.getQ(self.lastObservation, self.lastAction)
            delta = reward - oldQ
            self.updateQ(self.lastObservation, self.lastAction, delta)
        if self.episodeNum % self.dumpCount == 0:
            self.dump()
    def dump(self):
        for varType in range(1,3):
            for varVal in range (-2, 3):
                ob = (3, varType, varVal)
                for action in self.actionList:
                    key = (ob, action)
                    self.touch([ob], action)
                    print key, " ", self.Q[key]


if __name__ == "__main__":

    isUpdate = True
    initialQ = 0
    controller = LinearSARSA(0.5, 0, 0.8, (-1, 1), initialQ, 50)
    ob = ((1,1), (2,2), (3, 3))
    print controller.start(ob)
    print controller.Q
    print controller.step(10, ob)
    print controller.Q
    print controller.step(10, ob)
    print controller.Q
    print controller.step(10, ob)
    print controller.Q
    print controller.step(10, ob)
    print controller.Q
    for i in range(0,100):
        print controller.step(10, ob)

    print controller.Q
    print controller.trace
    #print controller.end(10, isUpdate)
    #print controller.Q
    #import pickle
    #output = open('data.pkl', 'wb')
    #pickle.dump(controller, output)
    #output.close()
    #input = open('data.pkl', 'rb')
    #ctrl2 = pickle.load(input)
    #print "after load"
    #print controller.Q
    #pickle.loads(xp)
    #y


import random
from Def import getActionId

#TODO: make it LambdaHORDQ, and add m=5 heuristic to init all table values, lambda does not propagate for 3 steps before
class LinearHORDQ:
    def __init__(self, alpha, epsilon, gamma, actionList, initialQ, dumpCount, pseudoReward):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.actionList = actionList
        self.initialQ = initialQ
        self.Q = {}
        self.m = {}
        self.minM = 3
        self.dumpCount = dumpCount
        self.episodeNum = 0
        self.isUpdate = True
        self.pseudoReward = pseudoReward

    def touchAll(self, observation):
        for action in self.actionList:
            self.touch(observation, action)

    #listof feature -> void
    def touch(self, observation, action):
        for fea in observation:
            key = (fea, action)
            if not key in self.Q:
                self.Q[key] = self.initialQ #may use optimistic exploration
                self.m[key] = 0

    def selectAction(self, observation, task):
        #use epsilon-greedy
        if random.random() < self.epsilon:
            #select randomly
            action = self.actionList[int(random.random()*len(self.actionList))]
            print "random"
            return action
        else:
            #select the best action
            v = []
            for action in self.actionList:
                q = self.getQ(observation, action)
                if action == task:
                    #print task
                    #print action
                    q = q + self.pseudoReward
                v.append(q)
            assert len(v) > 0

            m = max(v)
            print v
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
            key = (fea, action)
            if self.m[key] >= self.minM:  #RMAX assumption
                val = self.Q[(fea, action)]
            else:
                val = self.initialQ
            Q = Q + val
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

            alpha = self.alpha
            n = self.m[key] + 1
            self.m[key] = n
            if n <= self.minM:
                alpha = 1.0/n
            self.Q[key] = self.Q[key] + alpha*deltaPerFeature
        
    def start(self, observation, task):
        ob = observation
        self.lastObservation = ob
        self.touchAll(ob)
        self.lastAction = self.selectAction(ob, task)
        self.episodeNum = self.episodeNum + 1
        return self.lastAction

    #listof feature -> action
    def setUpdate(self, isUpdate):
        self.isUpdate = isUpdate

    def step(self, reward, observation, task):
        ob = observation
        self.touchAll(ob)
        newAction = self.selectAction(ob, task)
        print "feature", observation
        if self.isUpdate:
            self.update(self.lastObservation, self.lastAction, reward, ob, newAction)
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
    controller = LinearHORDQ(0.5, 0, 0.8, (-1, 1), initialQ, 10)
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


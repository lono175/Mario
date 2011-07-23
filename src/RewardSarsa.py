import random

class RewardSarsa:
    def __init__(self, alpha, epsilon, gamma, actionList, initialQ, dumpCount ):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.actionList = actionList
        self.initialQ = initialQ
        self.Q = {}
        self.m = {}
        self.minM = 1
        self.fastUpdateM = 10
        assert(self.fastUpdateM >= self.minM)
        self.dumpCount = dumpCount
        self.episodeNum = 0

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
            if n <= self.fastUpdateM:
                alpha = 1.0/n
            self.Q[key] = self.Q[key] + alpha*deltaPerFeature
    def start(self, ob, action):
        self.lastObservation = ob
        self.lastAction = action

    def step(self, ob, reward, action):
        oldQ = self.getQ(self.lastObservation, self.lastAction)
        delta = reward - oldQ
        self.updateQ(self.lastObservation, self.lastAction, delta)
        self.lastObservation = ob
        self.lastAction = action

    def end(self, reward):
        oldQ = self.getQ(self.lastObservation, self.lastAction)
        delta = reward - oldQ
        self.updateQ(self.lastObservation, self.lastAction, delta)

if __name__ == "__main__":

    isUpdate = True
    initialQ = 0
    controller = LinearSARSA(0.5, 0, 0.8, (-1, 1), initialQ, 10)
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


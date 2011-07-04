# 
# Copyright (C) 2007, Mark Lee
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#TODO: add location to tile feature
#TODO: add speed to feature
import random
import sys
from rlglue.agent.Agent import Agent
from rlglue.types import Action
from rlglue.types import Observation
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.utils.TaskSpecVRLGLUE3 import TaskSpecParser
from LinearSARSA import LinearSARSA
from LambdaSARSA import LambdaSARSA
from FeatureMario import *
from ML import *
import tool


from random import choice
import string

MaxY = 15
episilon = 0.005
def saveObj(obj):
    print "descructing...."
    actionList = getAllAction()
    initialQ = 0
    dumpCount = 100000
    #self.agent = LinearSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
    obj.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
    tool.Save(obj, "mario.db")

def GenPasswd():
    chars = string.letters + string.digits
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

def GenPasswd2(length=8, chars=string.letters + string.digits):
    return [choice(chars) for i in range(length)]

	
def getAction(dir, isJump, isSpeed):
    #-1, 0, 1 for direction, 1 is to the right
    #0, 1 for jump
    #0, 1 for speed
    action = Action()
    action.numInts = 3
    action.numDoubles = 0
    action.numChars = 0
    action.intArray = []
    action.doubleArray = []
    action.charArray = []
    action.intArray.append(dir)
    action.intArray.append(isJump)
    action.intArray.append(isSpeed)
    return action

def dumpAction(action):
    print action.intArray[0], " ", action.intArray[1], " ", action.intArray[2]

def dumpActionList(actionList):
    for action in actionList:
        print (action.intArray[0], action.intArray[1], action.intArray[2]),
    print ""

def dumpList(list):
    for item in list:
        print '%02.3f'%item, " ",
    print " "

def dumpObj(obj):
    print "dump4...."
    print dir(obj) 
    print "dump4...."
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))

def getAllAction():
    actionList = []
    for dir in [-1, 0, 1]:
        for isJump in [0, 1]:
            for isSpeed in [0, 1]:
                action = getAction(dir, isJump, isSpeed)
                actionList.append(action)
    #actionList = [getAction(1, 1, 1)]
    return actionList

def getActionId(action):
    id = ((action.intArray[0] + 1) << 2) + ((action.intArray[1]) << 1) + (action.intArray[2])
    return id

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
        self.episodeNum = 0
        
    def agent_init(self, taskSpecString):
        ##parse action
        print "begin: ", self.totalStep
        print "Q", len(self.agent.Q)
        self.treeList = []
        if self.feaList != []:
            self.treeList = getClassifier(self.feaList)


    def agent_start(self,obs):
        fea = getSarsaFeature(obs)
        self.lastMario = getMario(obs) #for internal reward system
        self.lastObs = obs
        action = self.agent.start(fea)
        self.stepNum = 0
        self.lastAction = action
        return action

    def agent_step(self, reward, obs):
        if reward < -0.01 + episilon and reward > -0.01 - episilon:
            reward = -1
        #print obs.intArray
        #print reward
        #mario = self.getMario(obs)
        fea = getSarsaFeature(obs)
        mario = getMario(obs) #for internal reward system
        #print "loc:", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
        dx = mario.x - self.lastMario.x
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


        lastObs = self.lastObs
        lastAction = self.lastAction
        lastMario = self.lastMario
        lastActionId = getActionId(lastAction)
        tileList = getTileAroundMario(lastObs, 2)
        assert(len(tileList) == 25)

        deltaX = mario.x - (lastMario.x + lastMario.sx)
        deltaY = mario.y - (lastMario.y + lastMario.sy)
        
        modelFea = [str(lastActionId), round(lastMario.sx, 1), round(lastMario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))] + [round(mario.sx, 1), round(mario.sy, 1), round(deltaX, 1), round(deltaY, 1)]

        #assert(self.treeList != [])
        if self.treeList != []:
            pass
            #print self.treeList
            #print "feature: ", modelFea
            #print "predict: ", classify(modelFea, self.treeList)

            #print "test feaL ", self.feaList[0]
            #print "test predict: ", classify(self.feaList[0], self.treeList)
        self.feaList.append(modelFea)

        self.lastObs = obs
        self.lastAction = action

        self.lastMario = mario
        self.stepNum = self.stepNum + 1

        return action

    def agent_end(self,reward):
        if reward == -10.0:
            reward = -50.0
        print "end: ", reward, " step: ", self.stepNum, " dist:", self.lastMario.x
        self.totalStep = self.totalStep + self.stepNum
        self.agent.end(reward)
        self.rewardList.append(reward)
        self.distList.append(self.lastMario.x)
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

        self.action.charArray   = GenPasswd2(self.action.numChars)
        #print self.action.intArray
        #print self.action.doubleArray
        #print self.action.charArray





if __name__=="__main__":        
    import atexit
    #agent = tool.Load("mario.db")
    agent = LinearSarsaAgent()
    atexit.register(lambda: saveObj(agent)) #workaround to the NoneType error in hte descructorn
    #agent = tool.Load("Speed.db")
    #AgentLoader.loadAgent(agent)
    
    AgentLoader.loadAgent(agent)

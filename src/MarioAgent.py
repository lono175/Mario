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
import tool


from random import choice
import string
MaxY = 15
episilon = 0.005

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
    action.intArry = []
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
def getAllAction():
    actionList = []
    for dir in [-1, 0, 1]:
        for isJump in [0, 1]:
            for isSpeed in [0, 1]:
                action = getAction(dir, isJump, isSpeed)
                actionList.append(action)
    #actionList = [getAction(1, 1, 1)]
    return actionList
class LinearSarsaAgent(Agent):

    def __init__(self):
        print "init"
        random.seed(0)
        actionList = getAllAction()
        initialQ = 0
        dumpCount = 100000
        #self.agent = LinearSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
        self.agent = LambdaSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
        self.totalStep = 0
        self.rewardList = []
        self.distList = []
        
    def agent_init(self,taskSpecString):

        #print taskSpecString
        #TaskSpec = TaskSpecParser(taskSpecString);
        #if TaskSpec.valid:
            #print "Task spec was valid";
        #else:
            #print "Task Spec could not be parsed: "+taskSpecString;
            #exit()

        ##parse action
        print "begin: ", self.totalStep
        print "Q", len(self.agent.Q)
        #self.int_action_ranges    = TaskSpec.getIntActions()
        #self.double_action_ranges = TaskSpec.getDoubleActions()
        #self.action.numInts       = len(self.int_action_ranges)
        #self.action.numDoubles    = len(self.double_action_ranges)
        #self.action.numChars      = TaskSpec.getCharCountActions()

        #print "int",self.int_action_ranges,self.action.numInts 
        #print "doubles",self.double_action_ranges,self.action.numDoubles
        #print "chars",self.action.numChars 
    def __del__(self):
        print "descructing...."
        tool.Save(self, "mario.db")
    def agent_start(self,obs):
        fea = getSarsaFeature(obs)
        self.lastMarioLoc = getMario(obs) #for internal reward system
        action = self.agent.start(fea)
        self.stepNum = 0
        return action

    def agent_step(self, reward, obs):
        if reward < -0.01 + episilon and reward > -0.01 - episilon:
            reward = -0.2
        #print obs.intArray
        #print reward
        #mario = self.getMario(obs)
        #print "loc:", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
        fea = getSarsaFeature(obs)
        mario = getMario(obs) #for internal reward system
        dx = mario.x - self.lastMarioLoc.x
        #let mario finish the level as fast as possible
        #reward = reward + dx*0.5
        reward = reward + dx
        print "reward: ", reward
        #print fea
        action = self.agent.step(reward, fea)
        #print "Q: ", self.agent.getQ(fea, action)

        #print self.agent.actionList
        #print self.totalStep, "---------------"
        #dumpActionList(self.agent.actionList)
        print "Constant Q: ", dumpList(getConstantQ(obs, self.agent))
        print "monst fea: ", getMonsterFeatureList(obs)
        print "Monster Q: ", dumpList(getMonsterQ(obs, self.agent))
        print "TileQ: ", dumpList(getGridQ(obs, self.agent))


        #dumpAction(action)
        self.lastMarioLoc = mario
        self.stepNum = self.stepNum + 1

        return action

    def agent_end(self,reward):
        if reward == -10.0:
            reward = -30.0
        print "end: ", reward, " step: ", self.stepNum, " dist:", self.lastMarioLoc.x
        self.totalStep = self.totalStep + self.stepNum
        self.agent.end(reward)
        self.rewardList.append(reward)
        self.distList.append(self.lastMarioLoc.x)
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
    #agent = tool.Load("mario.db")
    #agent = tool.Load("Speed.db")
    #AgentLoader.loadAgent(agent)
    AgentLoader.loadAgent(LinearSarsaAgent())

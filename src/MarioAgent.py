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
import sys
from rlglue.types import Observation
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.agent.Agent import Agent
from rlglue.utils.TaskSpecVRLGLUE3 import TaskSpecParser
#from LambdaSARSA import LambdaSARSA
#from FeatureMario import *
#from ML import *
from Def import *
import tool
import pickle
import time
import random


#statistics
#begin:  284797
#feaNum 137793
#action id:  0  data size:  7721
#action id:  1  data size:  6263
#action id:  2  data size:  2764
#action id:  3  data size:  1916
#action id:  6  data size:  4222
#action id:  8  data size:  15260
#action id:  9  data size:  66449      
#action id:  10  data size:  7250
#action id:  11  data size:  25948


from random import choice
import string
episilon = 0.005

MaxY = 15
def saveObj(obj, filename):
    print "descructing...."
    #actionList = getAllAction()
    #initialQ = 0
    #dumpCount = 100000
    #self.agent = LinearSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
    #obj.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
    obj.DynamicLearner = {}
    obj.RewardLearner = []
    tool.Save(obj, filename)
    print "done"

def GenPasswd():
    chars = string.letters + string.digits
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

def GenPasswd2(length=8, chars=string.letters + string.digits):
    return [choice(chars) for i in range(length)]

	
#INIT, init -> new agent with parameter, RUN
#RUN, any action -> keep the original agent, RUN
#RUN, stop -> save the reward, INIT

def GetFileName(agent):
    name = 'mario_'
    if agent.agentType == AgentType.HybridAgent:
        name = name + 'hybrid_' 
    elif agent.agentType == AgentType.SarsaAgent:
        name = name + 'sarsa_' 
    elif agent.agentType == AgentType.ModelAgent:
        name = name + 'model_' 

    name = name + str(agent.episodeNum) + '_'
    name = name + str(agent.epsilon) + '_'
    name = name + str(agent.initPseudoReward)

    name = name + '.db'
    return name
    
    
class MarioAgent(Agent):
    def __init__(self):
        self.state = INIT
        
    def agent_message(self, inMessage):
        msg = pickle.loads(inMessage)
        action = msg['cmd']

        if self.state == INIT and action == ActionInit:
            #if at the very begining, init everything
            self.agent = ModelAgent()
            self.agent.setParam(epsilon = msg['epsilon'], pseudoReward = msg['pseudoReward'], type = msg['type'])
            self.state = RUN
            print "init"
        elif self.state == RUN and action == ActionStop:
            filename = GetFileName(self.agent)
            saveObj(self.agent, filename)
            self.state = INIT
            print "run"
        elif action == ActionKill:
            filename = GetFileName(self.agent)
            filename = filename + '.bak'
            saveObj(self.agent, filename)
            exit()
        else:
            print "current state: ", self.state
            print "action: ", action
            assert(0)
    
    def agent_init(self, taskSpecString):
        return self.agent.agent_init(taskSpecString)

    def agent_start(self, obs):
        return self.agent.agent_start(obs)

    def agent_step(self, reward, obs):
        return self.agent.agent_step(reward, obs)

    def agent_end(self, reward):
        return self.agent.agent_end(reward)
            
    def agent_cleanup(self):
        pass

    def agent_freeze(self):
        pass




from ModelAgent import ModelAgent
if __name__=="__main__":        
    import atexit
    #agent = LinearSarsaAgent()
    #atexit.register(lambda: saveObj(agent)) #workaround to the NoneType error in hte descructorn
    #agent = tool.Load("Speed.db")
    #AgentLoader.loadAgent(agent)

    #while True:
    print 'loading agent...'
    #agent = tool.Load("mario_sarsa_49_0.01_0.db")
    agent = MarioAgent()
    
    AgentLoader.loadAgent(agent)
    print 'agent done'
    filename = GetFileName(agent.agent)
    filename = filename + '.bak2'
    saveObj(agent.agent, filename)
    
    #time.sleep(2)

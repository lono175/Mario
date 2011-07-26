# console Trainer for RL Competition
# Copyright (C) 2007, Brian Tanner brian@tannerpages.com (http://brian.tannerpages.com/)
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

import rlglue.RLGlue as RLGlue
from consoleTrainerHelper import *
import random
import pickle
episodeList = []


def main():
    whichTrainingMDP = 0
    # Uncomment ONE of the following lines to choose your experiment
    #loadTetris(whichTrainingMDP); #put the desired parameter set in where MDP is in [0,19]
    #loadHelicopter(whichTrainingMDP); #put the desired parameter set in where MDP is in [0,9]
     #loadAcrobot(whichTrainingMDP); #put the desired parameter set in where MDP is in [1,49] #0 is standard acrobot
     #loadPolyathlon(whichTrainingMDP); #put the desired parameter set in where MDP is in [0,5]
    #typeList = [121, 122, 123, 124, 125, 41, 42, 43, 44, 45, 46, 47, 48 , 49, 50, 51, 52, 53] + range(126, 170)
    #typeList = [121, 122, 123, 41, 42, 43]
    #typeList = [121 for x in range(50)]
    #typeList = [121 for x in range(50)]
    #typeList = [4832 for x in range(20)]
    #typeList = [1247 for x in range(50)]
    
    typeList = [5657 for x in range(50)]
    #typeList = [142 for x in range(50)]
    #typeList = [42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42]
    #typeList = [4647 for x in range(50)]
    
#42 1, 121 3, 121 4, 42 7, 4647 2, 126 2, 142, 2, 121 6, 5156 3, 5657 3, 4832 3
#4832, 3-->very hard at 170
#5657, 3-->very hard at 193, 235
#3457, 3-->spikey fun
#1247, 3-->medium pit, no spikey good, a lot of pits
#1548, 3-->begin spikey
#5478, 3-->easy level
#1547, 3-->easy level, spikey and turtle
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


    conf = {}
    conf['epsilon'] = 0.01
    conf['pseudoReward'] = 5
    conf['type'] = SarsaAgent
    conf['save'] = 1
    conf[]
    for type in typeList:
    #while True:
        #for diff in range(6, 7):
        for diff in range(3, 4):
        #for diff in range(2, 3):
        #for diff in range(2, 3):
        #for diff in range(1, 2):
    #for numRun in range(0, 10):
            #type = int(random.random()*10000)
            episodeList.append((type, diff))
            print RLGlue.RL_agent_message(pickle.dumps(['Hello world']))
            loadMario(True, True, type, 0, diff, whichTrainingMDP);


            # and then,
            #		just run the experiment:
            RLGlue.RL_init()
            episodesToRun = 20
            totalSteps = 0
            for i in range(episodesToRun):
                RLGlue.RL_episode(20000)
                thisSteps = RLGlue.RL_num_steps()
                print "Total steps in episode %d is %d" %(i, thisSteps)
                totalSteps += thisSteps

            print "Total steps : %d\n" % (totalSteps)
            RLGlue.RL_cleanup()
def dumpEpisode():
    print episodeList
if __name__ == "__main__":
    import atexit
    atexit.register(dumpEpisode) #workaround to the NoneType error in hte descructorn
    main()

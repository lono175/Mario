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
import os
import time
import threading
import tool
from Def import *
episodeList = []


def main():
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
    
    maxLen = 50
    typeList = [1247 for x in range(100)]
    typeLen = len(typeList)
    partList = [typeList[i*maxLen : min(typeLen, (i+1)*maxLen)] for i in range(typeLen/maxLen)]
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


    for agentType in [AgentType.ModelAgent]:
    #for agentType in [AgentType.SarsaAgent, AgentType.ModelAgent]:
    #for agentType in [AgentType.SarsaAgent]:
        #for epsilon in [0.01, 0.02, 0.04]:
        for epsilon in [0.01]:
        #for epsilon in [0.02, 0.01, 0.04]:
        #for epsilon in [0.01, 0.02, 0.04]:
        #for epsilon in [0.02, 0.04]:
            #rewardList = [0, 2, 20, 5]
            rewardList = [20]
            #rewardList = [2]
            if agentType == AgentType.SarsaAgent:
                rewardList = [0]
            for pseudoReward in rewardList:
                t = threading.Thread(target = lambda : os.system('e:\\python26\\python.exe ./MarioAgent.py'))
                t.start()

                #conf = {}
                conf = {}
                conf['epsilon'] = epsilon
                conf['pseudoReward'] = pseudoReward
                conf['type'] = agentType
                conf['cmd'] = ActionInit
                conf['typeList'] = typeList
                tool.Save(conf, 'conf')
                trainer = threading.Thread(target = lambda : os.system('e:\\python26\\python.exe ./trainer.py'))
                trainer.start()
                #os.system('e:\\python26\\python.exe ./trainer.py')

                #print "---------1"
                #conf = {}
                #conf['cmd'] = ActionStop
                #RLGlue.RL_agent_message(pickle.dumps(conf))
                #print "---------2"
                #conf = {}
                #conf['cmd'] = ActionKill
                #RLGlue.RL_agent_message(pickle.dumps(conf))
#os.system('bash ./RLCleanup.bash')
                trainer.join()
                t.join()
                time.sleep(5)


if __name__ == "__main__":
    import atexit
    #atexit.register(dumpEpisode) #workaround to the NoneType error in hte descructorn
    main()

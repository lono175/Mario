import rlglue.RLGlue as RLGlue
from consoleTrainerHelper import *
import random
import pickle
import os
import time
import threading
import tool
from Def import *
if __name__ == '__main__':
   
    episodeList = []
    whichTrainingMDP = 0
    agentType = SarsaAgent
    epsilon = 0.01
    pseudoReward = 5

    conf = tool.Load('conf')
    #conf = {}
    #conf['epsilon'] = epsilon
    #conf['pseudoReward'] = pseudoReward
    #conf['type'] = agentType
    #conf['cmd'] = ActionInit

    t = threading.Thread(target = lambda : os.system('d:\\python26\\python.exe ./MarioAgent.py'))
    os.system('bash ./RLInit.bash')

    t.start()
    #time.sleep(5)
    RLGlue.RL_agent_message(pickle.dumps(conf))

    typeList = [5657 for x in range(3)]
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
            loadMario(True, True, type, 0, diff, whichTrainingMDP);

            RLGlue.RL_init()
            episodesToRun = 2
            totalSteps = 0
            for i in range(episodesToRun):
                RLGlue.RL_episode(400)
                thisSteps = RLGlue.RL_num_steps()
                print "Total steps in episode %d is %d" %(i, thisSteps)
                totalSteps += thisSteps

            print "Total steps : %d\n" % (totalSteps)
            RLGlue.RL_cleanup()
    conf = {}
    conf['cmd'] = ActionStop
    RLGlue.RL_agent_message(pickle.dumps(conf))
    conf = {}
    conf['cmd'] = ActionKill
    RLGlue.RL_agent_message(pickle.dumps(conf))
#os.system('bash ./RLCleanup.bash')
    t.join()
    #time.sleep(5)
    print "next agent............."

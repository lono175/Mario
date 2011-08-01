from Sim import *

#initWorld =         tool.Load("dumpWorld.db")
#dynaLearner=        tool.Load( "dumpDyna.db")
#rewardLearner=        tool.Load( "dumpReward.db")
#initActionRange=        tool.Load( "dumpActionRange.db")
#PrevPlan =         tool.Load( "dumpPrevPlan.db")

#Optimize(initWorld, dynaLearner, rewardLearner, 300, PrevPlan, initActionRange)

#from MarioAgent import *
#agent = tool.Load('mario.db')
##agent.prune()

#agent.initLearner()
#actionId = 9
#dataList = agent.feaList[actionId]
#print "len: ", len(dataList)
#learner = agent.DynamicLearner[actionId]
##tree = learner.getSVMClassifier(dataList, learner.domainList)
#tree = learner.getKnnClassifier(dataList, learner.domainList)


#print "begin test"
#correctNum = learner.TestPerformance(dataList[1:500], tree)

#print correctNum



from MarioAgent import *
from tool import *
agent = tool.Load('mario.db')
print agent.distList
SaveToCSVSingle(agent.distList, 'dist_sarsa.csv')
#agent.initLearner()
#agent.prune()

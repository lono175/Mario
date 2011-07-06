#gridMap should remove mario
#return the location of mario

class WorldState():
    #mario
    #monsterList
    #gridMap (no mario loc)
    #expected reward for the current world state (real reward + A* reward)
    def __init__(self):
        pass

class ActionState():
    #action
    #the list of WorldState (len: MaxState)
    #the average reward from all WorldState
    def __init__(self):
        pass

def Optimize(mario, monsterList, gridMap, rewardTree, treeList, MaxNode):
    MaxState = 10
    MaxDepth = 6
    MaxDist = MaxDepth * 2
    nodeList = {}
    #create the initial nodes for 12 actions, each node has 10 world states
    
    #do A* here
    #choose a node with highest average reward which does not exceed MaxDepth

    #remove a node and expand it

    #stop when MaxNode reached or find the optimal path (the average reward > MaxDist) 

#sample the effect of all actions for the mario state
#return the list of ActionState 
def Expand(mario, monsterList, gridMap, rewardTree, treeList):
    

    

#desired action, x-speed, y-speed(-2~2), observation around mario (5 by 5) -> new x-speed (-2~2), new y-speed (-2~2), delta x, delta y
#0~12((0, 1, 1),     1.1,       -1.1,          , 32,                              , new_x = x + x-speed + delta x

import orange, random
import orngWrap, orngTree
from FeatureMario import MonType

class Learner:
    """A wrapper object to all machine learner"""
    def __init__(self, commonVar, classVar, isSeparateAction):
        #self.domain = orange.Domain(commonDomain, classDomain)
        self.domainList = []
        for classVar in classVarList:
            domain = orange.Domain(commonVar, classVar)
            self.domainList.append(domain)
        self.classNum = len(classDomain)
        self.treeList = []

    def add(self, dataList):
        if self.feaList != []:
            self.treeList = getClassifier(dataList, self.domainList)

    def getClass(self, data):
        assert(self.treeList != [])
        FeatureNum = len(data[0]) - self.classNum
        partData = [orange.Example(domainList[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(self.classNum)]
        res = [treeList[i](partData[i]).value for i in range(self.classNum)]
        return res

    def empty(self):
        return self.treeList == []

def getTestFeature(state, actionId):
    mario = state.mario
    tileList = getTileAroundMario(state, 2)
    assert(len(tileList) == 25)
    fea = [str(actionId), round(mario.sx, 1), round(mario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))] 

def getTrainFeature(state, classValueList, actionId):
    mario = state.mario
    tileList = getTileAroundMario(state, 2)
    assert(len(tileList) == 25)
    fea = [str(actionId), round(mario.sx, 1), round(mario.sy, 1)] + [chr(tileList[x]) for x in range(len(tileList))]  + [classValueList]
     
        
#def classifyRewardDomain(data, rewardTree, rewardDomain):
    #partData = orange.Example(rewardDomain, data)
    #res = rewardTree(partData).value
    #return res

#def classify(data, treeList, domainList):
    #classNum = len(domainList)
    #partData = [orange.Example(domainList[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(classNum)]
    #res = [treeList[i](partData[i]).value for i in range(classNum)]
    #return res
        

def treeSize(node):
    if not node:
        return 0

    size = 1
    if node.branchSelector:
        for branch in node.branches:
            size += treeSize(branch)

    return size


def printTree0(node, level):
    if not node:
        #print " "*level + "<null node>"
        return

    if node.branchSelector:
        nodeDesc = node.branchSelector.classVar.name
        nodeCont = node.distribution
        print "\n" + "   "*level + "%s (%s)" % (nodeDesc, nodeCont),
        for i in range(len(node.branches)):
            print "\n" + "   "*level + ": %s" % node.branchDescriptions[i],
            printTree0(node.branches[i], level+1)
    else:
        nodeCont = node.distribution
        majorClass = node.nodeClassifier.defaultValue
        print "--> %s (%s) " % (majorClass, nodeCont),

def printTree(x):
    if type(x) == orange.TreeClassifier:
        printTree0(x.tree, 0)
    elif type(x) == orange.TreeNode:
        printTree0(x, 0)
    else:
        raise TypeError, "invalid parameter"
ActionRange = range(12)
#SpeedRange = range(-2, 3)
#DeltaRange = range(-4, 5)

FeatureNum = 28

#[-1, 1, 1] + [ord(' ') for x in range(25)] + [1, 1, 1, 1]
#def convertData(data):
    #newData = []
    #for entry in data:
        #newFormat = [str(entry[x]) for x in range(len(entry))] 
        #newData.append(newFormat)
    #return newData

def getClassVar():
    classVarList = []
    var = orange.FloatVariable("new-x-speed")
    classVarList.append(var)
    var = orange.FloatVariable("new-y-speed")
    classVarList.append(var)
    var = orange.FloatVariable("delta-x")
    classVarList.append(var)
    var = orange.FloatVariable("delta-y")
    classVarList.append(var)
    #var = orange.FloatVariable("reward")
    #classVarList.append(var)
    return classVarList

#def getDomainList():
    #commonDomain = getCommonDomain()
    #classVarList = getClassVar()
    #domainList = []
    #for classVar in classVarList:
        #domain = orange.Domain(commonDomain, classVar)
        #domainList.append(domain)
    #reward = orange.FloatVariable("reward")
    #rewardDomain = orange.Domain(commonDomain, reward)
    #return domainList, rewardDomain

#def getRewardClassifier(data, rewardDomain):
    #partData = [(data[x]) for x in range(len(data))]
    #table = orange.ExampleTable(rewardDomain, partData)
    #classifier = orngTree.TreeLearner(table)
    #return classifier


# 3 + 25 + 4 classes= 32 
#[1, 1, 1] + [' ' for x in range(25)] + [1, 1, 1, 1]
def getClassifier(data, domainList):
    dataList = []
    i = 0
    for domain in domainList:
        partData = [(data[x][:FeatureNum] + [data[x][FeatureNum+i]]) for x in range(len(data))]
        table = orange.ExampleTable(domain, partData)
        dataList.append(table)
        i = i + 1

        #tree = orange.TreeLearner(table)
        #treeList.append(tree)

    treeList = []
    for data in dataList:
        #tree = orngTree.TreeLearner()
        #tunedTree = orngWrap.Tune1Parameter(object=tree, parameter='m_pruning', \
        #values=[0, 0.1, 0.2, 1, 2, 5, 10], verbose=2, \
        #values=[0], verbose=2, \
        #returnWhat=orngWrap.TuneParameters.returnClassifier)

        #classifier = tunedTree(data)
        classifier = orngTree.TreeLearner(data)
        treeList.append(classifier)
    return treeList
    
def getCommonVar():
    tileList = [' ', '$', 'b', '?', '|', '!', 'M', '1', '2', '3', '4', '5', '6', '7', 'w']
    monTypeList = [ chr(type) for type in [MonType.RedKoopa, MonType.GreenKoopa, MonType.Goomba, MonType.Spikey, MonType.PiranhaPlant, MonType.Mushroom, MonType.FireFlower, MonType.Fireball, MonType.Shall, MonType.FlyRedKoopa, MonType.FlyGreenKoopa, MonType.FlyGoomba, MonType.FlySpikey]]

    tileList = tileList + monTypeList

    domain = []
    var = orange.EnumVariable("action", values = ['%i'%x for x in ActionRange])
    domain.append(var)
    var = orange.FloatVariable("x-speed")
    domain.append(var)
    var = orange.FloatVariable("y-speed")
    domain.append(var)
    for x in range(25):
        var = orange.EnumVariable("obs%i"%x, values = tileList)
        domain.append(var)
    return domain

def toExample(data, i):
    commonDomain = getDomain()
    domain = orange.Domain(commonDomain)
    print domain
    example = orange.Example(domain, data)
    return example
#def toRewardFea(data, loc):
    #partData = data[:FeatureNum] + [data[FeatureNum+loc]]
    #return partData
        

import numpy
if __name__ == '__main__':

    dataListOri = [['9', 0.0, -1.8, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 0.69999999999999996, -2.7999999999999998, 0.5, -9.3000000000000002],
            ['3', 0.69999999999999996, -2.7999999999999998, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', -0.20000000000000001, -3.1000000000000001, -0.20000000000000001, -100]]
    dataList = [['9', 0.0, -1.8, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',  -2.3000000000000002],
            ['3', 0.69999999999999996, -2.7999999999999998, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',  2]]
    #treeList = getClassifier(dataList)
    #data = dataList[0]
    #res =  classify(data, treeList)
    #printTree(treeList[3])
    #print res

    #partData = ['10', -1000, -1.800, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    #print "len", len(partData)
    #ex = toExample(partData, 3)
    #print treeList[3](ex)
    
    
    domain = []
    var = orange.EnumVariable("action", values = ['9', '3'])
    domain.append(var)
    var = orange.FloatVariable("x-speed")
    domain.append(var)
    var = orange.FloatVariable("y-speed")
    domain.append(var)
    tileList = [' ', '$', 'b', '?', '|', '!', 'M', '1', '2', '3', '4', '5', '6', '7']
    for x in range(25):
        var = orange.EnumVariable("obs%i"%x, values = tileList)
        domain.append(var)
    var = orange.FloatVariable("cls")
    domain.append(var)

    commonDomain = orange.Domain(domain)
    domain = orange.Domain(commonDomain)
    table = orange.ExampleTable(domain, dataList)
    tree = orange.TreeLearner(table)
    print type(tree)
    print tree(orange.Example(domain, dataList[0]))

    print "---------------"
    data = ['9', 0.0, -1.8, -9.3000000000000002] 
    data2 = ['2', 0.69999999999999996, -2.7999999999999998, -100]
    domain = []
    var = orange.EnumVariable("action", values = ['9', '3', '2'])
    domain.append(var)
    var = orange.FloatVariable("x-speed")
    domain.append(var)
    var = orange.FloatVariable("y-speed")
    domain.append(var)
    for x in range(25):
     var = orange.EnumVariable("obs%i"%x, values = tileList)
     domain.append(var)
    var = orange.FloatVariable("cls")
    domain.append(var)

    commonDomain = orange.Domain(domain)
    domain = orange.Domain(commonDomain)
    table = orange.ExampleTable(domain, dataList)
    tree = orngTree.TreeLearner(table)
    print tree
    print tree(orange.Example(domain, dataList[0]))
    print "---------------"
    treeList = getClassifier(dataListOri)
    print classify(dataListOri[0], treeList)

    print "---------------"



    #data3 = ['2', 2.1, 2.1] + [' ' for x in range(25)] + [1.5, 1, 1, 1]
    #data4 = ['2', 2.1, 2.1] + [' ' for x in range(25)] + [1.6, 1, 1, 1]
    #data5 = ['2', 2.1, 2.1] + [' ' for x in range(25)] + [1.7, 1, 1, 1]
    #dataList = [data]
    #for x in range(50):
        #dataList.append(data2) 
    #for x in range(50):
        #dataList.append(data3)
    #for x in range(50):
        #dataList.append(data4)
    #dataList.append(data5)
    #treeList = getClassifier(dataList)
    #res =  classify(data, treeList)
    #print res
    #printTree(treeList[0])



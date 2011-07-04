#desired action, x-speed, y-speed(-2~2), observation around mario (5 by 5) -> new x-speed (-2~2), new y-speed (-2~2), delta x, delta y
#0~12((0, 1, 1),     1.1,       -1.1,          , 32,                              , new_x = x + x-speed + delta x

import orange, random
import orngWrap, orngTree
from FeatureMario import MonType

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
    return classVarList
    
# 3 + 25 + 4 classes= 32 
#[1, 1, 1] + [' ' for x in range(25)] + [1, 1, 1, 1]
def getClassifier(data):
    assert(len(data) > 0)
    inputNum = len(data[0])
    classNum = inputNum - FeatureNum
    classVarList = getClassVar()
    assert(classNum == len(classVarList))

    commonDomain = getDomain()
    dataList = []
    for i in range(classNum):
        domain = orange.Domain(commonDomain, classVarList[i])
        partData = [(data[x][:FeatureNum] + [data[x][FeatureNum+i]]) for x in range(len(data))]
        table = orange.ExampleTable(domain, partData)
        dataList.append(table)

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
    
def getDomainList():
    FeatureNum = 28

    tileList = [' ', '$', 'b', '?', '|', '!', 'M', '1', '2', '3', '4', '5', '6', '7']
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
    commonDomain = orange.Domain(domain)

    classVarList = getClassVar()
    classNum = len(classVarList)

    domainList = []
    for i in range(classNum):
        domain = orange.Domain(commonDomain, classVarList[i])
        domainList.append(domain)

    return domainList

def toExample(data, i):
    commonDomain = getDomain()
    domain = orange.Domain(commonDomain)
    print domain
    example = orange.Example(domain, data)
    return example
    
def classify(data, treeList):
    inputNum = len(data)
    classNum = inputNum - FeatureNum
    classVarList = getClassVar()
    commonDomain = getDomain()
    domain = [orange.Domain(commonDomain, classVarList[i] ) for i in range(classNum)]
    partData = [orange.Example(domain[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(classNum)]
    res = [treeList[i](partData[i]).value for i in range(classNum)]
    return res

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



#desired action, x-speed, y-speed(-2~2), observation around mario (5 by 5) -> new x-speed (-2~2), new y-speed (-2~2), (delta x ( , delta y
#0~7((0, 1, 1),     1,       -1,          , 32,                              , x + x-speed + delta x

import orange, random

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
        print " "*level + "<null node>"
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

SpeedRange = range(-2, 3)
DeltaRange = range(-4, 5)
FeatureNum = 28

#[1, 1, 1] + [ord(' ') for x in range(25)] + [1, 1, 1, 1]
def convertData(data):
    newData = []
    for entry in data:
        newFormat = [str(entry[x]) for x in range(len(entry))] 
        newData.append(newFormat)
    return newData


def getClassVar():
    classVarList = []
    var = orange.EnumVariable("new x-speed", values = ['%i'%x for x in SpeedRange])
    classVarList.append(var)
    var = orange.EnumVariable("new y-speed", values = ['%i'%x for x in SpeedRange])
    classVarList.append(var)
    var = orange.EnumVariable("delta-x", values = ['%i'%x for x in DeltaRange])
    classVarList.append(var)
    var = orange.EnumVariable("delta-y", values = ['%i'%x for x in DeltaRange])
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
    treeList = []
    for i in range(classNum):
        domain = orange.Domain(commonDomain, classVarList[i])
        partData = [(data[x][:FeatureNum] + [data[x][FeatureNum+i]]) for x in range(len(data))]
        table = orange.ExampleTable(domain, partData)
        tree = orange.TreeLearner(table)
        treeList.append(tree)

    return treeList
    
def getDomain():
    tileList = [' ', '$', 'b', '?', '|', '!', 'M', '1', '2', '3', '4', '5', '6', '7']
    domain = []
    var = orange.EnumVariable("action", values = ['%i'%x for x in range(8)])
    domain.append(var)
    var = orange.EnumVariable("x-speed", values = ['%i'%x for x in SpeedRange])
    domain.append(var)
    var = orange.EnumVariable("y-speed", values = ['%i'%x for x in SpeedRange])
    domain.append(var)
    for x in range(25):
        var = orange.EnumVariable("obs%i"%x, values = tileList)
        domain.append(var)
    d = orange.Domain(domain)
    return d

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
    data = ['1', '1', '1'] + [' ' for x in range(25)] + ['1', '1', '1', '1']
    data2 = ['2', '1', '1'] + [' ' for x in range(25)] + ['2', '1', '1', '1']
    data3 = ['1', '1', '1'] + [' ' for x in range(25)] + ['1', '1', '1', '1']
    data4 = ['1', '1', '0'] + [' ' for x in range(25)] + ['2', '1', '1', '1']
    data5 = ['2', '1', '0'] + [' ' for x in range(25)] + ['2', '1', '1', '1']
    dataList = [data]
    for x in range(50):
        dataList.append(data2) 
    for x in range(50):
        dataList.append(data3)
    for x in range(50):
        dataList.append(data4)
    dataList.append(data5)
    treeList = getClassifier(dataList)
    res =  classify(data, treeList)
    print res
    #print int(res[0].value) == 2
    printTree(treeList[0])



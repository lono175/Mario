#desired action, x-speed, y-speed(-2~2), observation around mario (5 by 5) -> new x-speed (-2~2), new y-speed (-2~2), delta x, delta y
#0~12((0, 1, 1),     1.1,       -1.1,          , 32,                              , new_x = x + x-speed + delta x

import orange, random
import orngWrap, orngTree
from Orange.classification.svm import SVMLearner, SVMLearnerEasy

from FeatureMario import MonType
from Def import ActionRange
from tool import SampleData
from numpy import array

class Learner:
    """A wrapper object to all machine learner"""
    def __init__(self, commonVar, classVarList, maxFeature):
        #self.domain = orange.Domain(commonDomain, classDomain)
        self.domainList = []
        self.commonDomain = orange.Domain(commonVar)
        for classVar in classVarList:
            domain = orange.Domain(commonVar, classVar)
            self.domainList.append(domain)
        self.classNum = len(classVarList)
        self.treeList = []
        self.FeatureNum = len(commonVar)
        self.maxFeature = maxFeature

    def add(self, dataList):
        if dataList != []:
            self.treeList = self.getClassifier(dataList, self.domainList)

    def getClass(self, data, param = None):
        assert(self.treeList != [])
        partData = orange.Example(self.commonDomain, data[:self.FeatureNum])
        if param == None:
            res = [self.treeList[i](partData).value for i in range(self.classNum)]
        else:
            res = [self.treeList[i](partData, param) for i in range(self.classNum)]
        return res

    def getClassTree(self, data, treeList):
        partData = orange.Example(self.commonDomain, data[:self.FeatureNum])
        res = [treeList[i](partData).value for i in range(self.classNum)]
        return res

    def empty(self):
        return self.treeList == []

    def TestPerformance(self, dataList, treeList):
        #now test it
        correctNum = 0
        errNum = 0
        avgError = numpy.array([0 for i in range(self.classNum)])

        for data in dataList:
            classVar = data[self.FeatureNum:]
            classVar = [round(v, 1) for v in classVar]
            predict = self.getClassTree(data, treeList) 
            predict = [round(v, 1) for v in predict]
            avgError = avgError + abs(array(predict) - array(classVar))
            #print "---"
            #print classVar
            #print predict
            if predict == classVar:
                correctNum = correctNum + 1
            else:
                errNum = errNum + 1
                #print data
                #print classVar
                #print predict
                #print "----"
        #else:

        print "correct: ", correctNum
        print "incorrect: ", errNum
        avgError = avgError / (correctNum + errNum)
        print avgError
        return correctNum

    def getNewData(self, newDataList, dataList, bestTree, minFeature):
        i = len(newDataList)
        corNum = 0
        for data in dataList:
            if i >= minFeature:
                break

            classVar = data[self.FeatureNum:]
            predict = self.getClassTree(data, bestTree) 
            predict = [round(v, 1) for v in predict]
            if predict != classVar:
                newDataList.append(data)
                i = i + 1
            #else:
                #corNum = corNum + 1
        #print "correct ", corNum
        return newDataList

    #prune the dataList and return a new one
    def prune(self, dataList):

        sampleRatio = 1.0
        minFeature = self.maxFeature
        #maxFeature = 2000

        feaLen = len(dataList)
        if feaLen < 2*minFeature:
            tree = self.getClassifier(dataList, self.domainList)
            return dataList, tree

        maxCorrect = -1
        #do it 5 times, choose the best one
        for i in range(5):

            #randomly build a tree from 5% data
            sample = SampleData(dataList, int(sampleRatio*minFeature))
            tree = self.getClassifier(sample, self.domainList)

            correctNum = self.TestPerformance(dataList, tree)
            if correctNum > maxCorrect:
                bestTree = tree
                maxCorrect = correctNum
                bestSample = sample
        print "best: ", maxCorrect               
        print "sample size: ", len(bestSample)
        print "ori len ", len(dataList)

        #random.shuffle(dataList)
        #newDataList = bestSample
        #self.getNewData(newDataList, dataList, bestTree, minFeature)

        ##add data up minFeature
        #print "ori len ", len(dataList)
        #print "new len ", len(newDataList)

        #tree = self.getClassifier(newDataList, self.domainList)
        #corNum = self.TestPerformance(dataList, tree)
        #print "first refit correct ", corNum

        #random.shuffle(dataList)
        #newDataList = self.getNewData(newDataList, dataList, tree, minFeature + 1000)
        #tree = self.getClassifier(newDataList, self.domainList)
        #corNum = self.TestPerformance(dataList, tree)
        #print "refit new len ", len(newDataList)
        #print "refit correct ", corNum

        #tree = self.getClassifier(dataList, self.domainList)
        #corNum = self.TestPerformance(dataList, tree)
        #print "ori correct ", corNum
        
        return bestSample, bestTree

    def getKnnClassifier(self, data, domainList):
        dataList = []
        i = 0
        for domain in domainList:
            partData = [(data[x][:self.FeatureNum] + [data[x][self.FeatureNum+i]]) for x in range(len(data))]
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
            print "begin training...."
            knn = orange.kNNLearner(data, k=1)
            print "finish training"
            treeList.append(knn)
        return treeList
    def getSVMClassifier(self, data, domainList):
        dataList = []
        i = 0
        for domain in domainList:
            partData = [(data[x][:self.FeatureNum] + [data[x][self.FeatureNum+i]]) for x in range(len(data))]
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
            svr = SVMLearnerEasy(svm_type=SVMLearner.Epsilon_SVR)
            print "begin training...."
            classifier = svr(data)
            print "finish training"
            treeList.append(classifier)
        return treeList
        
    # 3 + 25 + 4 classes= 32 
    #[1, 1, 1] + [' ' for x in range(25)] + [1, 1, 1, 1]
    def getClassifier(self, data, domainList):
        dataList = []
        i = 0
        for domain in domainList:
            partData = [(data[x][:self.FeatureNum] + [data[x][self.FeatureNum+i]]) for x in range(len(data))]
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
#class ActionLearner:
    #"""A wrapper object to all machine learner"""
    #def __init__(self, commonVar, classVarList):
        ##self.domain = orange.Domain(commonDomain, classDomain)
        #self.domainList = []
        ##assume the first variable is action

        #self.commonDomain = orange.Domain(commonVar)
        #for classVar in classVarList:
            #domain = orange.Domain(commonVar, classVar)
            #self.domainList.append(domain)
        #self.classNum = len(classVarList)
        #self.feaNum = len(commonVar)
        #self.treeList = {}
        #self.FeatureNum = 27

    #def add(self, dataList):
        #newDataList = getActionData(dataList)

        ##for debugging
        #for actionId in newDataList:
            #print "action id: ", actionId, " data size: ", len(newDataList[actionId])
        #for actionId in ActionRange:
            #actionData = newDataList[actionId]
            #if actionData != []:
                #self.treeList[actionId] = self.getClassifier(actionData, self.domainList)


    #def getActionClass(self, data, actionId, treeList):
        #assert(actionId in self.treeList)
        #partData = orange.Example(self.commonDomain, data[:self.FeatureNum])
        #res = [treeList[actionId][i](partData).value for i in range(self.classNum)]
        #return res

    #def getClass(self, data, treeList):
        #actionId = int(data[0])
        #data = data[1:]
        #self.getActionClass(data, actionId, treeList)
        #return res

    #def empty(self):
        #return len(self.treeList) == 0

    #def TestPerformance(self, actionDataList, treeList):
        ##now test it
        #correctNum = 0
        #correctAction = {}
        #incAction = {}
        #avgError = {}
        #for actionId in ActionRange:
            #correctAction[actionId] = 0
            #incAction[actionId] = 0
            #avgError[actionId] = array([0, 0, 0, 0])

            #actionData = actionDataList[actionId] 
            #for data in actionData:
                #classVar = data[self.FeatureNum:]
                #predict = self.getActionClass(data, actionId, treeList) 
                #predict = [round(v, 1) for v in predict]
                #avgError[actionId] = avgError[actionId] + abs(array(predict) - array(classVar))
                ##print "---"
                ##print classVar
                ##print predict
                #if predict == classVar:
                    #correctNum = correctNum + 1
                    #correctAction[actionId] = correctAction[actionId] + 1
                #else:
                    #incAction[actionId] = incAction[actionId] + 1
            ##else:

                ##print classVar
                ##print predict
                ##print "----"
        #print "correct: ", correctNum
        #print correctAction
        #print incAction
        #for actionId in ActionRange:
            #avgError[actionId] = avgError[actionId] / (correctAction[actionId] + incAction[actionId])
        #print avgError
        #return correctNum
        #
    ##prune the dataList and return a new one
    ##the current classifier will be replaced by one with the new data set
    #def prune(self, dataList):

        #feaLen = len(dataList)
        #if feaLen < maxFeature:
            #return 

        #sampleRatio = 0.10
        #minFeature = 10000
        #maxFeature = 20000
        #ratioPerAction = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.1, 0.15]

        #samplePerAction = {}
        #for i, actionId in enumerate(ActionRange):
            #samplePerAction[actionId] = int(minFeature*sampleRatio*ratioPerAction[i]) 

        #dataPerAction = {}
        #for i, actionId in enumerate(ActionRange):
            #dataPerAction[actionId] = int(minFeature*ratioPerAction[i]) 

        #actionDataList = GetActionData(dataList)



        #maxCorrect = -1
        ##do it 5 times, choose the best one
        #for i in range(5):

            #actionSample = {}
            #actionTree = {}

            ##randomly build a tree from 5% data
            #for actionId in actionDataList:
                #sample = SampleData(actionDataList[actionId], samplePerAction[actionId])
                #actionSample[actionId] = sample
                #tree = self.getClassifier(sample, self.domainList)
                #actionTree[actionId] = tree 

            #correctNum = self.TestPerformance(actionDataList, actionTree)
            #if correctNum > maxCorrect:
                #bestTree = actionTree
        #print "best: ", maxCorrect               

        #newActionDataList = {}
        ##add data up minFeature
        #for actionId in actionDataList:
            #actionData = []
            #i = 0
            #random.shuffle(actionDataList[actionId])
            #for data in actionDataList[actionId]
                #if i >= dataPerAction[actionId]:
                    #break

                #classVar = data[self.FeatureNum:]
                #predict = self.getActionClass(data, actionId, bestTree) 
                #predict = [round(v, 1) for v in predict]jkkkkk
                #if predict != classVar:
                    #actionData.append
        #
    ## 2 + 25 + 4 classes= 31 
    ##[1, 1] + [' ' for x in range(25)] + [1, 1, 1, 1]
    #def getClassifier(self, data, domainList):
        #dataList = []
        #i = 0
        #for domain in domainList:
            #partData = [(data[x][:self.FeatureNum] + [data[x][self.FeatureNum+i]]) for x in range(len(data))]
            #table = orange.ExampleTable(domain, partData)
            #dataList.append(table)
            #i = i + 1

            ##tree = orange.TreeLearner(table)
            ##treeList.append(tree)

        #treeList = []
        #for data in dataList:
            ##tree = orngTree.TreeLearner()
            ##tunedTree = orngWrap.Tune1Parameter(object=tree, parameter='m_pruning', \
            ##values=[0, 0.1, 0.2, 1, 2, 5, 10], verbose=2, \
            ##values=[0], verbose=2, \
            ##returnWhat=orngWrap.TuneParameters.returnClassifier)

            ##classifier = tunedTree(data)
            #classifier = orngTree.TreeLearner(data)
            #treeList.append(classifier)
        #return treeList

     
        
#def classifyRewardDomain(data, rewardTree, rewardDomain):
    #partData = orange.Example(rewardDomain, data)
    #res = rewardTree(partData).value
    #return res

#def classify(data, treeList, domainList):
    #classNum = len(domainList)
    #partData = [orange.Example(domainList[i], data[:FeatureNum] + [data[FeatureNum+i]]) for i in range(classNum)]
    #res = [treeList[i](partData[i]).value for i in range(classNum)]
    #return res
        

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


    
def getCommonVar():
    tileList = [' ', '$', 'b', '?', '|', '!', 'M', '1', '2', '3', '4', '5', '6', '7', 'w', '\n']
    monTypeList = [ chr(type) for type in [MonType.RedKoopa, MonType.GreenKoopa, MonType.Goomba, MonType.Spikey, MonType.PiranhaPlant, MonType.Mushroom, MonType.FireFlower, MonType.Fireball, MonType.Shall, MonType.FlyRedKoopa, MonType.FlyGreenKoopa, MonType.FlyGoomba, MonType.FlySpikey]]

    tileList = tileList + monTypeList

    domain = []
    var = orange.EnumVariable("action", values = ['%i'%x for x in ActionRange])
    domain.append(var)
    var = orange.FloatVariable("x-offset")
    domain.append(var)
    var = orange.FloatVariable("y-offset")
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
            ['3', 0.69999999999999996, -2.7999999999999998, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',  2],
            ['3', 0.69999999999999996, -2.7999999999999998, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',  2.3],
['3', 0.69999999999999996, -2.7999999999999998, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'M', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',  2.5]
            ]
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
    v, p = tree(orange.Example(domain, dataList[0]), orange.GetBoth)
    print v
    print type(p)
    print p
    p2 = tree(orange.Example(domain, dataList[0]), orange.GetProbabilities)
    print type(p2)
    print p2.var()
    print p2.average()
    for d in p2:
        print "val: ", d

    #print "---------------"
    #data = ['9', 0.0, -1.8, -9.3000000000000002] 
    #data2 = ['2', 0.69999999999999996, -2.7999999999999998, -100]
    #domain = []
    #var = orange.EnumVariable("action", values = ['9', '3', '2'])
    #domain.append(var)
    #var = orange.FloatVariable("x-speed")
    #domain.append(var)
    #var = orange.FloatVariable("y-speed")
    #domain.append(var)
    #for x in range(25):
     #var = orange.EnumVariable("obs%i"%x, values = tileList)
     #domain.append(var)
    #var = orange.FloatVariable("cls")
    #domain.append(var)

    #commonDomain = orange.Domain(domain)
    #domain = orange.Domain(commonDomain)
    #table = orange.ExampleTable(domain, dataList)
    #tree = orngTree.TreeLearner(table)
    #print tree
    #print tree(orange.Example(domain, dataList[0]))
    #print "---------------"
    #treeList = getClassifier(dataListOri)
    #print classify(dataListOri[0], treeList)

    #print "---------------"



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



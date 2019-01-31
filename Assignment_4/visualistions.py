#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 16:33:29 2018

@author: nithish k
"""


import pandas as pd
import numpy as np
import itertools as itr
import random
import collections as col
import math
import tqdm
from forest import forest
from adaboost import AdaBoost
import matplotlib.pyplot as plt






if __name__ == '__main__':
    
    
    
    def sampleit(train,train_Y,k):
        whole_train = np.column_stack((train, train_Y))
        r = random.sample([i for i in range(train.shape[0])],k)       
        whole_sample = whole_train[r,:]
        train_sample = whole_sample[:,0:train.shape[1]]        
        train_y_sample = whole_sample[:,train.shape[1]]
        return train_sample, train_y_sample
    
    
    
    ####num trees
    numTreeAccu = []
    numTrees = list(range(5,35,5))
    for numtree in numTrees:
        myForest = forest(maxDepth=5,numTrees= numtree,verbose = True)
        TrainX,TrainY,TrainXID = myForest.getDataFromFile('train-data.txt')
        myForest.trainForest(TrainX,TrainY)
        Xtest,yTest = myForest.getDataFromFile('test-data.txt')
        finalPredictions = myForest.predict(Xtest)
        numTreeAccu.append(sum(finalPredictions==yTest)/len(yTest))
    #    myForest._getDecisionFromTree(rootNode,X[60,:])
    #    myForest.exploreTree(rootNode)
  
    plt.plot(numTrees,numTreeAccu)
    plt.xlabel("Number of Trees")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs No of Trees")
    
    
    ##max depth
    maxDepthsAcc = []
    maxDepths = list(range(5,20,5))
    for maxDeptha in maxDepths:
        myForest = forest(maxDepth=maxDeptha,numTrees= 20,verbose = True)
        TrainX,TrainY,TrainXID = myForest.getDataFromFile('train-data.txt')
        
        myForest.trainForest(TrainX,TrainY)
        Xtest,yTest,XtestID = myForest.getDataFromFile('test-data.txt')
        finalPredictions = myForest.predict(Xtest)
        maxDepthsAcc.append(sum(finalPredictions==yTest)/len(yTest))
        
    plt.plot(maxDepths,maxDepthsAcc)
    plt.xlabel("Variation Of Depths")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Maximum Depth")
    

    
    ##num features
    numFeaturesAcc = []
    numFeatur = list(range(5,20,5))
    for numFea in numFeatur:
        myForest = forest(maxDepth=5,numTrees= 20,verbose = True, numFeaturesInAtree = numFea)
        TrainX,TrainY,TrainXID = myForest.getDataFromFile('train-data.txt')
        
        myForest.trainForest(TrainX,TrainY)
        Xtest,yTest,XtestID = myForest.getDataFromFile('test-data.txt')
        finalPredictions = myForest.predict(Xtest)
        numFeaturesAcc.append(sum(finalPredictions==yTest)/len(yTest))
        
        
        
    baggpropAccu = []
    bagprop = [i*0.1 for i in range(5,10,1)]
    for bag in bagprop:
        myForest = forest(maxDepth=5,numTrees= 10,verbose = True, baggingProportions = bag)
        TrainX,TrainY,TrainXID = myForest.getDataFromFile('train-data.txt')
        
        myForest.trainForest(TrainX,TrainY)
        Xtest,yTest,XtestID = myForest.getDataFromFile('test-data.txt')
        finalPredictions = myForest.predict(Xtest)
        baggpropAccu.append(sum(finalPredictions==yTest)/len(yTest))
        
    plt.plot(bagprop,baggpropAccu)
    plt.xlabel("Variation Of Bagging Proportion")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs Bagging Proportion")
    
    
    
    #########################Adaboost################################################
    numTreeAccu = []
    numTrees = list(range(5,200,5))
    for numtree in numTrees:
        myBoost = AdaBoost(nTrees = numtree)
        TrainX,TrainY,TrainXID = myBoost.getDataFromFile('train-data.txt')
        
        myBoost.train(TrainX,TrainY)
        Xtest,yTest,XtestID = myBoost.getDataFromFile('test-data.txt')
        finalPredictions = myBoost.predict(Xtest)
        numTreeAccu.append(sum(finalPredictions==yTest)/len(yTest))
        
    plt.plot(numTrees,numTreeAccu)
    
    
    
    
    
    
    ############################################################################
    
    
    numTreeAccu = []
    samples = []
    for i in range(5000,36000,5000):
        myBoost = AdaBoost(nTrees = 200)
        TrainX,TrainY,TrainXID = myBoost.getDataFromFile('train-data.txt')
        TrainX,TrainY = sampleit(TrainX,TrainY,i)
        myBoost.train(TrainX,TrainY)
        Xtest,yTest,XtestID = myBoost.getDataFromFile('test-data.txt')
        finalPredictions = myBoost.predict(Xtest)
        numTreeAccu.append(sum(finalPredictions==yTest)/len(yTest))
        samples.append(i)
        
    plt.plot(samples,numTreeAccu)
    plt.xlabel("Number of samples")
    plt.ylabel("Accuracy")
    plt.title("Accuracy vs No of Samples")
    
    
        ####num trees
    numTreeAccu = []
    samples = []
    for i in range(5000,36000,5000):
        myForest = forest(maxDepth=5,numTrees= 20,verbose = True)
        TrainX,TrainY,TrainXID = myForest.getDataFromFile('train-data.txt')
        TrainX,TrainY = sampleit(TrainX,TrainY,i)
        myForest.trainForest(TrainX,TrainY)
        Xtest,yTest,Xtestid = myForest.getDataFromFile('test-data.txt')
        finalPredictions = myForest.predict(Xtest)
        numTreeAccu.append(sum(finalPredictions==yTest)/len(yTest))
        samples.append(i)
    #    myForest._getDecisionFromTree(rootNode,X[60,:])
    #    myForest.exploreTree(rootNode)
        plt.plot(samples,numTreeAccu)
        plt.xlabel("Number of samples")
        plt.ylabel("Accuracy")
        plt.title("Accuracy vs No of Samples")
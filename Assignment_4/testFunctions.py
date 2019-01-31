# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 01:45:39 2018

@author: nithish k
"""
import pandas as pd
import numpy as np
import itertools as itr



data = pd.read_csv('train-data.txt', header = None, sep = ' ' )


data.columns = ['a','b'] + data.columns[2:].tolist()
data['']

list(itr.combinations([1,2,3,4],2))
data[data[1] == 270][data[3] == data[27] ]

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=20, max_depth=7,
                             random_state=0)

clf.fit(TrainX,TrainY)
skPredictions = clf.predict(Xtest)
print(sum(skPredictions==yTest)/len(yTest))
importances = clf.feature_importances_




indices = np.argsort(importances)[::-1]
impFeatures = indices[:50]
myDistt = {1:2,3:5}

    trainSquared = Xtest**2
    colSums = np.zeros(trainSquared.shape[0])
    addedColumns = []
    len(addedColumns)
    for colNum,column in enumerate(trainSquared.T):
        
        if colNum %3 == 0 and colNum != 0 :
            addedColumns.append(colSums)
            colSums = np.zeros(len(column))
            
        
        if colNum % 3 <= 2:
            
            
            colSums = colSums+column
    addedColumnsTest = np.array(addedColumns).T  
    addedColumnsTrain

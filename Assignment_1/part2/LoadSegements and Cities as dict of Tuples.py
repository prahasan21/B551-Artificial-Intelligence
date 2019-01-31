# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 18:39:18 2018

@author: nithish k
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 11:06:07 2018

@author: nithish k
"""
import pandas as pd
import pickle as p
import os 

# change the directory to your local folder here 
try: 
    dirname =  os.path.dirname(os.path.abspath(__file__))
 
    os.chdir(dirname)
except: 
    os.chdir("C:/Users/ntihish/Documents/IUB/Elem of AI/assignment 1/prgadugu-skandag-chhshar-a1/part2/")



pd.set_option('display.max_columns', 7)

segmentsDF = pd.read_csv("road-segments.txt",
                          sep = " ",header = None)



segmentsDF.head()
segmentsDF.columns = ['City1','City2','Dist_Miles','Speed_Limit','HighwayName']
len(segmentsDF) # 12057 rows
segmentsDF[segmentsDF['Speed_Limit']==0].loc[:,:] # city segments with 0 speed limits
segmentsDF[segmentsDF['Speed_Limit']!=0].loc[:,['Speed_Limit']].min() #25 is the minimum speed limit apart from zero
segmentsDF['Speed_Limit'].max() # 65 is the max speed limit
segmentsDF['Speed_Limit'].mean() # 49.14 is the mean speed limit
segmentsDF['Dist_Miles'].max() # max segement length 923
segmentsDF['Dist_Miles'].min()
segmentsDF.fillna(segmentsDF['Speed_Limit'].mean(),inplace = True)#filling missing speeds by  mean of speeds
any(pd.isna(segmentsDF['Speed_Limit'])) #checking if missing values are filled
segmentsDF[pd.isna(segmentsDF['Speed_Limit'])]



"""
class road_segments():
    
    def __init__(self):
        self.data = {} # dictionary1(city1 as key, value : dictionry(city2 as key, Dictinory : (attributes as key and their values )
    
    def addData(City1,City2,Dist,SpeedLimit,HighwayName):
        if City1 not in data:
            data[City1] = {City2: {Dist_Miles : Dist, Speed_Limit: SpeedLimit , Highway: HighwayName}}
        else:
            data[City1][City2] = {Dist_Miles : Dist, Speed_Limit: SpeedLimit , Highway: HighwayName}
        
    def addCity2():
        
        
    def getCity2(City1):
    
    
    def get
"""


road_segments = {} # dictionary1(city1 as key, diectiories(city2 as key, Dictinory )

"""
Load CIty1 in road_segments as dict of dict of dict 
"""
segmentsDF.shape
for i in range(len(segmentsDF)):
    City1,City2,Dist, SpeedLimit ,HighwayName = segmentsDF.loc[i,['City1','City2','Dist_Miles','Speed_Limit','HighwayName']]
    if City1 not in road_segments:
        road_segments[City1] = [(City2 , Dist, SpeedLimit , HighwayName)]

    else:
        road_segments[City1].append((City2,Dist, SpeedLimit , HighwayName))

#segmentsDF.loc[1,['City1','City2','Dist_Miles','Speed_Limit','HighwayName']]
#
#Warning duplicate city2 in row :  4193
#Warning duplicate city2 in row :  9863
#Warning duplicate city2 in row :  10839
#        :6263
        
"""
Load City2 in roadSegments as dict of dict of dict
for bidirectional search
"""
for i in range(len(segmentsDF)):
    City2,City1,Dist, SpeedLimit ,HighwayName = segmentsDF.loc[i,['City1','City2','Dist_Miles','Speed_Limit','HighwayName']]
    if City1 not in road_segments:
        road_segments[City1] = [(City2 , Dist, SpeedLimit , HighwayName)]

    else:
        road_segments[City1].append((City2,Dist, SpeedLimit , HighwayName))




###dumping road_segemts object
p.dump(road_segments,open("road_segments.p",'wb'))


"""
This code block below is for loading and verifying gps file
loading for gps
"""



city_gpsDF = pd.read_csv("city-gps.txt",
                          sep = " ",header = None)

city_gpsDF.columns =  ['City','Latitude','Longitude']
city_gpsDF.head()
city_gpsDF.describe()
any(pd.isna(city_gpsDF['Latitude']))


#segmentsDF.loc[6263,:]
city_gpsDF.head()
city_gps = {}
for i in range(len(city_gpsDF)):
    city,lat,long = city_gpsDF.loc[i,:]
    if city not in city_gps:
        city_gps[city] = {'Latitude': lat,'Longitude': long}
    else :
        print("Warnig duplicate cities at row: " ,i)
        

#Warnig duplicate cities at row:  4792


p.dump(city_gps,open("city_gps.p",'wb'))

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 11:06:07 2018

@author: nithish k
"""
import pandas as pd
import pickle as p
import os 

# change the directory to your local folder here 
os.chdir("C:/Users/ntihish/Documents/IUB/Elem of AI/assignment 1/prgadugu-skandag-chhshar-a1/part2/")





segmentsDF = pd.read_csv("C:/Users/ntihish/Documents/IUB/Elem of AI/assignment 1/prgadugu-skandag-chhshar-a1/part2/road-segments.txt",
                          sep = " ",header = None)



segmentsDF.head()
segmentsDF.columns = ['City1','City2','Dist_Miles','Speed_Limit','HighwayName']
len(segmentsDF) # 12057 rows
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
        road_segments[City1] = {City2: {'Dist_Miles' : Dist, 'Speed_Limit': SpeedLimit , 'Highway': HighwayName}}
    elif City2 in road_segments[City1]:
        print("Warning duplicate city2 in row : ", i)
    else:
        road_segments[City1][City2] = {'Dist_Miles' : Dist, 'Speed_Limit': SpeedLimit , 'Highway': HighwayName}

#segmentsDF.loc[1,['City1','City2','Dist_Miles','Speed_Limit','HighwayName']]
#
#Warning duplicate city2 in row :  4193
#Warning duplicate city2 in row :  9863
#Warning duplicate city2 in row :  10839
#        :6263

segmentsDF.loc[4193,['City1','City2','Dist_Miles','Speed_Limit','HighwayName']]


"""
Load City2 in roadSegments as dict of dict of dict

"""
for i in range(len(segmentsDF)):
    City2,City1,Dist, SpeedLimit ,HighwayName = segmentsDF.loc[i,['City1','City2','Dist_Miles','Speed_Limit','HighwayName']]
    if City1 not in road_segments:
        road_segments[City1] = {City2: {'Dist_Miles' : Dist, 'Speed_Limit': SpeedLimit , 'Highway': HighwayName}}
    elif City2 in road_segments[City1]:
        print("Warning duplicate city2 in row : ", i)
    else:
        road_segments[City1][City2] = {'Dist_Miles' : Dist, 'Speed_Limit': SpeedLimit , 'Highway': HighwayName}




road_segments['Durant,_Mississippi']
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
        
city_gpsDF.loc[4792,:]

p.dump(city_gps,open("city_gps.p",'wb'))

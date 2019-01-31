#!/usr/bin/env python3

# put your routing program here!

##Documentation For the route.py file goes as follows:
"""
Abstraction Steps for the route.py file:
    State space:
        All cities. 
    Successor:
        All cities connected to that city in consideration.
    Data Structure:
        Dictionary of Lists with tuples
        Bidirectional Cities:
            Since all of the routes are Bidirectional instead of searching inner lists, 
            We first loaded the city 1 (from city) as key of the dictionary and then reloaded the toCity (the inner cities of the segments)
            as the key of the dictopnary, such that both directional searches are faster.
    Goal State:
        End City(Destination)
    Initial State:
        Start City(Source)
    Cost Function:
        Here we defined the cost function in terms of Distance, Time and segements.
        For Distance the cost function is cumulative lengths of the segments till the successor.
        For time the cost function is cumulative addition of times calculated by the segment length divided ny the speed limit.
        For segments the cost function is the cumulative addition of # of cites explored.
    Heuristic Function:
        Distance:
            We use the euclidian distance calculated by the lat long provided.
            In case lat long for a city is not present in citygps file, we take the nearest cities lat long which could be the cities at the same
            level of the graph or if all of the lat longs are missing at a particular level of the graph we would consider the lat long of the 
            parent node. If the parent node is also missing, we would take the lat longs of the siblings of the parent node.
            This is implemented by keeping the global variable of the nearest city "nearestCityWithLatLong" and updating it,
            when the successors or when a node is popped from the fringe.
        Time:
            For time to estimate the time required to the goal state from the current state we consider the maximum speed() across the
            entire segments(all roads), such that the heuristic always under-estimates the time required 65.0
        Segments:
            For segments we are dividing the Euclidian distance (heuristic) by the maximum segment length across the entire file road segments
            such that we never overestimate the actual number of segments.
        Heuristic Admissibility:
            Euclidean Distance is the shortest path between two points and hence never overestimates the actual distance.
            Hence our Heuristic is admissible and is also consistent because because of the triangular inequality for line segments. 

Assumptions:
    When the speed limit is  zero for a particular segment,we are substituted the min non zero speed in the data; 
    min non zero speed is 25 hence we are substitiutinh by 24 (could be subsitituted by any other number less than 25),
    Highest Speed Considered = 65.0,
    For missing speed limits we have substitiued by the mean of the speed limits.
Code related :
    
   1.City segments are loaded as dictionary of list of tuples  {fromcity: [(tocity1 , Dist, SpeedLimit , HighwayName),
                                                                          (tocity2 , Dist, SpeedLimit , HighwayName)  ]}
   2.For the faster loading of the files we have pickled the dictionaries and loaded the data from the 
   road segments and citygps files. please refer to the file "LoadSegements and Cities as dict of Tuples" in the part 2 directory.
   3. City gps is loaded as dictionary of dictioariy {city:{lat: ,long:}}


"""
try:
    from queue import PriorityQueue
except:
    from Queue import PriorityQueue
    

from random import randrange, sample
import sys
import string
import time
import os
import pickle as p
from math import radians, sin, cos, acos

start_time = time.time()


#take the directoy the files is stored in if run externaly
try: 
    dirname =  os.path.dirname(os.path.abspath(__file__))
 
    os.chdir(dirname)
except: 
    os.chdir("C:/Users/ntihish/Documents/IUB/Elem of AI/assignment 1/prgadugu-skandag-chhshar-a1/part2/")

#tempTextFile = open("Segmentsdump.txt",'w+')
#load pickled objects so that they need not be prepared again
city_gps = p.load(open("city_gps.p",'rb'))
road_segments = p.load(open("road_segments.p",'rb'))

try:
    start_city = sys.argv[1]
    end_city = sys.argv[2]
    algorithmChoice = sys.argv[3]
    costFuncChoice = sys.argv[4]
    #change directory command here


except: 
    
    ##sapmple checking
    #start_city = sample(list(city_gps.keys()),1)[0]
    #start_city = 'Abbot_Village,_Maine'
#    start_city = "San_Jose,_California"
#    start_city = 'Aboite,_Indiana'
#    start_city = 'Muncie,_Indiana'
    start_city = 'Bloomington,_Indiana'
    
#    start_city = 'Vantage,_Washington'
    #end_city = sample(list(city_gps.keys()),1)[0]
    #end_city = "Sandy_Stream_Mountain,_Maine"
    #end_city = "Florida_City,_Florida"
    #end_city = 'Lagrange,_Maine'
#    end_city = 'Alton,_Illinois'
#    end_city = 'Bellevue,_Washington'
#    end_city = 'Ritzville,_Washington'
#    end_city = 'Chicago,_Illinois'
#    end_city = "Miami,_Florida"
#    end_city = "Seattle,_Washington"
    end_city = 'Indianapolis,_Indiana'
#    start_city = 'Vantage,_Washington'
    costFuncChoice = "segments"
    algorithmChoice = "ids"


globalMaxDepthLimitIDS = 1000000
globalCitySeperator = " ==> "
speedZeroSubs = 24.0 #minimum non zero speed 
heuTimeDivide = 65.0 #max speed across all the segments
heuSegLength = 923.0 #max segment length across the data
minSegmentDist = 1  #used for when lat long is not present 
nearestCityWithLatLong = start_city #used when lat long is not present 

def successors(city):
    #fetch city from raod segemnts
    return road_segments[city]
    
    

def is_goal(city):
    return city==end_city


def is_optimal(algorithmChoice,costFuncChoice):
    flag = "no"
    if algorithmChoice == "astar" or algorithmChoice == "uniform":
        flag = "yes"
    if (algorithmChoice == "bfs" or algorithmChoice == "ids")  and costFuncChoice == "segments":
        flag = "yes"
    
    return flag

"""
--------------------------Different cost functions-------------------------------
"""
#pathsoFar should be a dict of timetaken till now , distance traversed till now , string of cities visited
def getDistanceAlongSegments(attributes):
    #lets say each move costs a unit
    #split the path by space and count the total moves 
    return attributes["totalDist"]

def getNumSegmentsTraversed(attributes):
    
    return len(attributes['totalPath'].split(globalCitySeperator))-1

def getTimeTaken(attributes):
    return attributes['totalTime']



#chooses cost function

def chooseCostFunc(costFuncChoice):
   if costFuncChoice=="distance":
       return getDistanceAlongSegments
   elif costFuncChoice == "segments":
       return getNumSegmentsTraversed
   elif costFuncChoice == "time":
       return getTimeTaken
   
"""
-----------------Heuristic and F(n) = h(n)+ c(n) -----------------------------------
"""



def calculate_heuristic(city,end_city): #with lat long distance
    
    """
    code to calculate distance from latlong
    from : https://www.w3resource.com/python-exercises/math/python-math-exercise-27.php
    """
    #to do add kms to miles  converion
    
    try:
        slat = radians(city_gps[city]["Latitude"])
        slon = radians(city_gps[city]["Latitude"])
        elat = radians(city_gps[end_city]["Longitude"])
        elon = radians(city_gps[end_city]["Longitude"])
        
        dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))*0.621371
    

    except:
#        print("Warning no lat long")
        dist = minSegmentDist
#        print(city, " wasnt present and current nearestCity is , ", nearestCityWithLatLong)
        slat = radians(city_gps[nearestCityWithLatLong]["Latitude"])
        slon = radians(city_gps[nearestCityWithLatLong]["Latitude"])
        elat = radians(city_gps[end_city]["Longitude"])
        elon = radians(city_gps[end_city]["Longitude"])
        dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))*0.621371
        
#        
        
        
    """
    code ends here
    """        

    if costFuncChoice == "distance":
        return dist 
    elif costFuncChoice == "time":
        return dist / heuTimeDivide # max speed limit so that it is not over estimating time
    elif costFuncChoice == "segments":
        return dist/ heuSegLength #max segments length so that it is not overestimating the number of segments (minimising the depth being predicted)
    
    
    
 #define f(n) = h(n)+c(n)
def HplusCost(city,end_city,attributes,costFuncChoice):
    #define f(n) = h(n)+c(n)
    
    return chooseCostFunc(costFuncChoice)(attributes) + calculate_heuristic(city,end_city)


"""
---------------------------------------Different Algorithms----------------------------------
"""




def solveByBFS(start_city):
### SOlving the problem in dfs approach
    visited_cities = {}
    fringe = [] #(city, dist_so far,speed,time_so_far,path)
    fringe.append((start_city,0,0,0,str(start_city)))
    
    while(len(fringe) > 0):
        (city, dist_so_far,cur_speed,time_so_far,path_traversed)  = fringe.pop(0)
        visited_cities[city] = path_traversed
#        print("\nCity looking at" , successors( city ))
        for (nextCity,curSegLength,cur_speedNow,highwayName) in successors( city ):
#            print("\nCity looking at" +nextCity)
            
           
            if nextCity in visited_cities:
                continue
            totalDist = dist_so_far + curSegLength
            if cur_speedNow == 0:
                cur_speedNow = speedZeroSubs
            totalTime = time_so_far + curSegLength/cur_speedNow
            nextpath = str(path_traversed)+ globalCitySeperator +str(nextCity)
            
            if is_goal(nextCity):
                return(totalDist,cur_speedNow,totalTime,nextpath)
#            if( not search_in_fringe(city,fringe)):
            
            fringe.append((nextCity, totalDist ,cur_speedNow,totalTime,nextpath))
    return False
    
    
#could be used for searching in fringe for dfs so that we would avoid looping in bidirectional paths
def search_in_fringe(city,fringe):#[(city, attributes as dict)]
    for tuples in fringe:
        if tuples[0] == city:
            return True
    
    return False
            
    
def solveByDFS(start_city,depthLimit = None):
 
    visited_cities = {} #keeping track of all the visited states
    fringe = [] #(city, dist_so far,speed,time_so_far,path)
    fringe.append((start_city,0,0,0,str(start_city)))
    
    
    exploredDepth = 0
    while(len(fringe) > 0):
        (city, dist_so_far,cur_speed,time_so_far,path_traversed)  = fringe.pop()
#        print(("exp :" , exploredDepth, "depth limit :",depthLimit ))
#        input()
        
        
        #generalising for ids would not affect for dfs as default argument is none
        exploredDepth = len(path_traversed.split(globalCitySeperator))
#        print(("exp :" , path_traversed, "depth limit :",depthLimit ))
        if depthLimit != None and exploredDepth > depthLimit :
            continue
            
       
        
        visited_cities[city] = path_traversed
        for (nextCity,curSegLength,cur_speedNow,highwayName) in successors( city ):
            
            if nextCity in visited_cities:
                continue
            
            nextpath = str(path_traversed)+ globalCitySeperator + str(nextCity)
            
            
            
            totalDist = dist_so_far + curSegLength
            if cur_speedNow == 0:
                cur_speedNow = speedZeroSubs
            totalTime = time_so_far + curSegLength/cur_speedNow
            
            
            
            if is_goal(nextCity):
                return(totalDist,cur_speedNow,totalTime,nextpath)
            
         
            fringe.append((nextCity, totalDist ,cur_speedNow,totalTime,nextpath))
    return False

def solveByIDS(start_city):
    

    global globalMaxDepthLimitIDS
    for curDepthLimit in range(1,globalMaxDepthLimitIDS+1):
        
        route = solveByDFS(start_city,curDepthLimit)
        if route !=False:
            return route
    return False









def solveByUniformCostSearch(start_city):
    #nithish
    visited_cities = {} #
#    countofZerodivides = 0
    fringe = PriorityQueue()
    init_attributes = {'totalDist':0,'totalTime': 0,'totalPath': ""}
    init_priority = chooseCostFunc(costFuncChoice)(init_attributes)
    
    #put in fringe (city,dist,speed,time = dist/speed)
    # data to be put in fringe should be node level not consolidated 
    
    fringe.put((init_priority,(start_city,0,0,0,str(start_city)))) # (city,dist,speed,time = dist/speed,pathtraversed)
    
    while not fringe.empty():
        (priority,(city, dist_so_far,cur_speed,time_so_far,path_traversed)) = fringe.get()
        ###changed the precedece of the is_goal to choose optimal path.
        
        visited_cities[city] = priority # put other details 
        
        if is_goal(city):
            return(dist_so_far,cur_speed,time_so_far,path_traversed)
            
        # change here if data structure changes
        
        for (nextCity,curSegLength,cur_speedNow,highwayName) in successors(city):
            if nextCity not in visited_cities:
                totalDist = dist_so_far + curSegLength
                if cur_speedNow == 0:
                    cur_speedNow = speedZeroSubs
                    
                totalTime = time_so_far + curSegLength/cur_speedNow
                nextpath = str(path_traversed)+ globalCitySeperator +str(nextCity)
                # pass a dictionary as attirbutes
                attributes = {'totalDist':totalDist,'totalTime': totalTime,'totalPath': nextpath}
                
    #            isInFringe, priorityInFringe = get_priority_membership_fringe(succ,fringe)
                calculatedPriority = chooseCostFunc(costFuncChoice)(attributes)
            
#            if not isInFringe and tuple(succ) not in visited_states:
            
                fringe.put((calculatedPriority, (nextCity, totalDist ,cur_speedNow,totalTime,nextpath)))#(priority as func of path till,data)
            ###add code to check replace teh priority.
            
    
    
    
    
    return False



def solveByAStar(start_city):
    
    global nearestCityWithLatLong
    visited_cities = {} #
#    countofZerodivides = 0
    fringe = PriorityQueue()
    init_attributes = {'totalDist':0,'totalTime': 0,'totalPath': ""}
    init_priority = HplusCost(start_city,end_city,init_attributes,costFuncChoice)
    
    #put in fringe (city,dist,speed,time = dist/speed)
    # data to be put in fringe should be node level not consolidated 
    
    fringe.put((init_priority,(start_city,0,0,0,str(start_city)))) # (city,dist,speed,time = dist/speed,pathtraversed)
    
    while not fringe.empty():
        (priority,(city, dist_so_far,cur_speed,time_so_far,path_traversed)) = fringe.get()
        ###changed the precedece of the is_goal to choose optimal path.
        
        
        #updating the global variable with the most recent city that had lat long in case all the children do not have a lat long
        if city in city_gps:
            nearestCityWithLatLong  = city
        
        visited_cities[city] = priority # put other details 
#        print("number of explored cities : ",len(visited_cities))
        if is_goal(city):
            return(dist_so_far,cur_speed,time_so_far,path_traversed)
            
        # change here if data structure changes
        
        for (nextCity,curSegLength,cur_speedNow,highwayName) in successors(city):
            
            
            #updating neareset city again if the children had lat longs to get even better approximation
            if nextCity in city_gps:
                nearestCityWithLatLong  = nextCity
            if nextCity not in visited_cities:
                totalDist = dist_so_far + curSegLength
                
                if cur_speedNow == 0:
                    cur_speedNow = speedZeroSubs
    #                countofZerodivides =countofZerodivides + 1
    #                print("Warning of zero divide ", "count is : ",countofZerodivides)
                    
                totalTime = time_so_far + curSegLength/cur_speedNow
                nextpath = str(path_traversed)+ globalCitySeperator +str(nextCity)
                # pass a dictionary as attirbutes
                attributes = {'totalDist':totalDist,'totalTime': totalTime,'totalPath': nextpath}
                
    #            isInFringe, priorityInFringe = get_priority_membership_fringe(succ,fringe)
                calculatedPriority = HplusCost(nextCity,end_city,attributes,costFuncChoice)
                
    #            if not isInFringe and tuple(succ) not in visited_states:
                
                fringe.put((calculatedPriority, (nextCity, totalDist ,cur_speedNow,totalTime,nextpath)))#(priority as func of path till,data)
                    
            ###add code to check replace teh priority.
            
            
    return False
# test cases







def chooseAlgorithm(algorithmChoice):
    if algorithmChoice =="astar":
        return solveByAStar
    elif algorithmChoice == "uniform":
        return solveByUniformCostSearch
    elif algorithmChoice =="bfs":
        return solveByBFS
    elif algorithmChoice =="dfs":
        return solveByDFS
    elif algorithmChoice == "ids":
        return solveByIDS


"""
------------------------run the solve-------------------------------------------
"""


#print("\n\nSolving \n\n")

route = chooseAlgorithm(algorithmChoice)(start_city)

#if route != False:
#    print ("Path Taken is : \n" + route[3]+"\n\nsegments are : " + str(len(route[3].split(globalCitySeperator))) +  "\n\ndistance is : " + str(route[0]) +"\n\ntime is " + str(route[2]))
#end_time = time.time()
#
#print ("\ntime taken to run the script is : ",end_time - start_time)

#print ("\ntime taken to run the script is : ",end_time - start_time)

if route != False:
    print (str(is_optimal(algorithmChoice,costFuncChoice)) + " " + 
           str(route[0])+ " " +
           str(route[2])+ " "+
           str(route[3].replace(globalCitySeperator," ")))
else : 
    print("couldnt find route")

#dist_so_far,cur_speed,time_so_far,path_traverse1d

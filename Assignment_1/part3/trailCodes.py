# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:17:12 2018

@author: nithish k
"""
del fringe
fullClass_init_state = [[student] for student in students]
fringe = PriorityQueue()
init_priority = calculate_state_value(goalState)

costComparisionList = []
fringe.put((init_priority,fullClass_init_state)) # (priority, class as list)
while not fringe.empty():
    (parentPriority,fullClass) = fringe.get()
    print(fullClass,parentPriority)
    
#        visitedStates[tuple(fullClass)] = parentPriority
    
    if is_goal(costComparisionList,fullClass):
            return fullClass
            
    
    costComparisionList = [] #reinitialise list again
    succ = []
    for aPermutedClass in successors( fullClass ):
            
        
        
#            isInFringe, priorityInFringe = get_priority_membership_fringe(succ,fringe)
        calculatedPriority = calculate_state_value(aPermutedClass)
        costComparisionList.append(calculatedPriority>parentPriority)
        succ.append((aPermutedClass,calculatedPriority,
                     calculatedPriority>parentPriority))
        all(costComparisionList)
        
#            if not isInFringe and tuple(succ) not in visited_states:
#            if tuple(aPermutedClass) not in visitedStates :
        
        fringe.put((calculatedPriority, aPermutedClass))
        
        
goalState =  [['chen464', 'djcran','kapadia'], ['fan6','kapadia','zehzhang'],['steflee']]
set([1,2,3],4)
set(students['chen464']['work_with']+['chen464']) - set(['chen464', 'djcran'])
len(set(["bhghjg"])-set(['chen464', 'djcran']))
city_gps['Morton,_Indiana']



state = [15,16,6,8,13,2,3,12,5,1,7,14,4,9,11,10] #10
goal_state = [i for i in range(1,17)]
state = [16, 13, 14, 15,4, 1, 2, 3,8, 5, 6, 7,11, 12, 9, 10] #9
state = [5, 7, 8, 1,10, 2, 4, 3,6, 9, 11, 12,15, 13, 14, 16]

goalDiagElements = [1,6,11,16]
mapGoalDiagElems = [(0,0),(1,1),(2,2),(3,3)]

curPositionDiagElems = [state.index(i) for i in goalDiagElements]

cartIndexForCurDiagElems = [(int(index/4),index%4) for index in curPositionDiagElems]

movementsFwd = sum([abs(cartIndexCur[0]-cartIndexGoal[0])+abs(cartIndexCur[0]-cartIndexGoal[0])  
                for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)])

#repeat for backward diagonal
goalDiagElements = [4,7,10,13]

mapGoalDiagElems = [(0,3),(1,2),(2,1),(3,0)]

curPositionDiagElems = [state.index(i) for i in goalDiagElements]

cartIndexForCurDiagElems = [(4 - (int(index/4)),index%4) for index in curPositionDiagElems]

movementsBwd = sum([abs(cartIndexCur[0]-cartIndexGoal[0])+abs(cartIndexCur[0]-cartIndexGoal[0])  
                for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)])
    
    
    
"string".replace("i","n")

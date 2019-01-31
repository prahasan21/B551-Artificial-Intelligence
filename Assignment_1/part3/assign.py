#!/usr/bin/env python3
# put your group assignment problem here!
"""
State Space:
    List of class students divided into groups.
    
Data Structure:
    Lists of Groups' list. [[each student or a group],[each student or a group]]
    
Initial State:
    Each student in a seperate group.
    
Successor:
    Merge any two groups in order, and send it out as a successor.
    So let there be a list [[A],[B],[C]] such that, once we send it to the successor function it will generate different combinations
    of the list such as [[A,B],[C]] and [[A],[B,C]]...so on and send all of them out as the states from the successor function.
    
Cost Function:
    The path cost is uniform(unit wise across all paths), However each state is associated with a "statecost" 
    calculated from the complaints the members in the group and aggregated over the entire class.

Final State:
    Goal of the problem is to minimse the statecost by seraching through the states and picking up the states having the lowest cost
    Hence the final state is when we reach a leaf node and no more combinations can be produced 
    or when we arrive at a state where all its children are associated with a higher cost (local minima).
    
    
Approach:
    Takes the Greatest Descent based on the Greedy approach.
    We move from intial state to the final state by subsequently merging two groups generating different combinations. 
    k, m, n values are evaluated for each group in the state and aggregated to the full class (state) 
    The cost evaluated is used as the priority to pick the state and generate its successors
    By moving in this approach gradually we end up at a state with lowest cost in a particular branch and thus is the goal state


Limitations: 
    "Refer document for additional information regarding this particular section"
    





"""

#store responses as dictionart with userid as the key
try:
    from queue import PriorityQueue
except:
    from Queue import PriorityQueue
    
import pandas as pd
import itertools as itr
import os
import copy
import time
import sys



"""
-------------------taking in arguments---------------------------------------
"""

try:
    inputFile = sys.argv[1]
    k = int(sys.argv[2])
    m = int(sys.argv[3])
    n = int(sys.argv[4])
    groupSizeCostValue = 1
   
except:
    k = 160
    m = 31
    n = 10
    groupSizeCostValue = 1




"""
-------------------------------------Code for collecting data--------------------------
"""
##setting directroy path to run 
start_time = time.time()
try: 
    dirname =  os.path.dirname(os.path.abspath(__file__))
 
    os.chdir(dirname)
except: 
    os.chdir("C:/Users/ntihish/Documents/IUB/Elem of AI/assignment 1/prgadugu-skandag-chhshar-a1/part3/")


responseDf = pd.read_csv(inputFile,sep = " ",header = None )
#responseDf = pd.read_csv("input_large_50.txt",sep = " ",header = None )

responseDf.columns = ['student','team_size_pref','work_with', 'not_work_with']


students = {}# {gorupsize, work with preference, not work with prefenrece}


for i in range(len(responseDf)):
    student,group_size,work_with, not_work_with  = responseDf.loc[i,:]

    if student not in students:
        students[student] = {'group_size':group_size,
                            'work_with' : work_with.split(","),
                            'not_work_with': not_work_with.split(",")}
    else:
        print("Warning duplicate responses")


"""
--------------------end of code for fetching data for------------------------------------------------
"""
#allcombs = itr.combinations(range(300),3)
#len([i for i in allcombs])

#goalState =  [['chen464', 'djcran',], ['fan6','kapadia','zehzhang'],['steflee']]

#intitial state is list of list with each student in single list


initialState_Class = [[student] for student in students]

#initialState_Class = [['chen464', 'fan6','kapadia'], ['djcran','zehzhang','steflee']]



 #dict of state and cost


def successors(inputfullClass):#successor as generators
    
    
    
    combGenerator = itr.combinations(inputfullClass,2)
    for groupCombinations in combGenerator:
        fullClass_state = copy.deepcopy(inputfullClass)
        ##represmts the combination group as a single list
        collapsedGrp = [membersOfGrp for membersOfGrp in itr.chain.from_iterable(groupCombinations)] ##collapses innerlists
        if len(collapsedGrp)<=3: 
            fullClass_state.append(collapsedGrp)
            fullClass_state.remove(groupCombinations[0]) #first group
            fullClass_state.remove(groupCombinations[1]) #second group
    
    ##generating sorted lists such that states could be comapred and to avoid generating the input state again
        for groups in fullClass_state:
            groups.sort()
        
        fullClass_state.sort()  
            
        if fullClass_state != inputfullClass:
            yield fullClass_state # using generator expressions so that all coombinations dont take up memory
#            elif fullClass_state == inputfullClass:
#                return 'No more combinations'



##when all of the childs of the state have higher cost
def is_goal(costComparisionList,currentState): 
    ##when all the children have higher cost than the paarent 
    #or there are no morechildren return true
#    if (currentState == goalState):
#        return True
        return all(costComparisionList)

       



def calculate_state_value(fullClass_state):
    #calculate grading time
    gradingCost = k*len(fullClass_state)
#    print("grading cost ", gradingCost)
#    print("full class is ", fullClass_state)
    #calculate group size disagrement cost
    groupSizeCost = 0
    peoplePrefCost = 0
    notToWorkWithCost = 0
    for group in fullClass_state:
#        print("group is ", group)
        for student in group: #iterate in group for each student to calculate teh cost
#            print("student is ",student)
            #calculate people preferce cost  
            if (students[student]['work_with'] != ["_"] ):
#                print("work wiht preference ",students[student]['work_with'])
                peoplePrefCost = peoplePrefCost + n * len(set(students[student]['work_with']+[student]) - set(group)) 
#            print("pref cosst" , peoplePrefCost)
            #calculate not to work with cost
            notToWorkWithCost = notToWorkWithCost + m * len(set(students[student]['not_work_with']).intersection(group))
#            print("not working cost ", notToWorkWithCost)
            #calculate group size cost
            if students[student]['group_size'] != len(group) and students[student]['group_size'] != 0:
                groupSizeCost += groupSizeCostValue #change here if the cost value changes
#            print( "group size cost ", groupSizeCost)
#            input()
    return gradingCost + groupSizeCost + peoplePrefCost + notToWorkWithCost
    
 

# not used function needed to convert the list into tupes if needed to be nseterd into dictionary
def getTupleVersion(currentState_FullClass):
    currentState_FullClassTuple = copy.deepcopy(currentState_FullClass)
    for i, group  in enumerate(currentState_FullClassTuple):
        currentState_FullClassTuple[i]= tuple(group)
    currentState_FullClassTuple = tuple(currentState_FullClassTuple)
    return currentState_FullClassTuple


def solve(fullClass_init_state):
    countOfSolutions = 0 
    
    visitedStates = {} # not used
    fringe = PriorityQueue()
    init_priority = calculate_state_value(fullClass_init_state)
    minStateValue = init_priority
    costComparisionList = [] #used to track the costs of the childrens so that the local minima can be arrived at
    fringe.put((init_priority,fullClass_init_state)) # (priority, class as list)
    while not fringe.empty():
        (parentPriority,fullClass) = fringe.get()
#        print("parent is ",fullClass,parentPriority)
        
#        visitedStates[tuple(fullClass)] = parentPriority
        
       
#        visitedStates[getTupleVersion(fullClass)] = parentPriority
        costComparisionList = [] #reinitialise list again
        for aPermutedClass in successors( fullClass ):
            
            
            
#            isInFringe, priorityInFringe = get_priority_membership_fringe(succ,fringe)
            calculatedPriority = calculate_state_value(aPermutedClass)
            costComparisionList.append(calculatedPriority>=parentPriority) # add booleans evaluated for children priority > parent priority
            
#            print("children are ",aPermutedClass,calculatedPriority)
            
#            if not isInFringe and tuple(succ) not in visited_states:

#            if getTupleVersion(aPermutedClass) not in visitedStates and calculatedPriority < parentPriority :
            if calculatedPriority < parentPriority :
                fringe.put((calculatedPriority, aPermutedClass))
#        print("cost compaeri :" , costComparisionList)
            
        if is_goal(costComparisionList,fullClass):
            if parentPriority < minStateValue:
                minStateValue = parentPriority
            countOfSolutions +=1
            
            if  countOfSolutions >= 1: # this value could be increased to move to another branch
                
                return fullClass,minStateValue
#            input()
    return False



groups = solve(initialState_Class)
"""
print according 
"""
for group in groups[0]:
    for students in group:
        print(students, end=" ")
    print()

print(groups[1])
end_time = time.time()

#print (end_time - start_time)


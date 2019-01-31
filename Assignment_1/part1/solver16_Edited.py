#!/bin/python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#


# Exception Handling


""



""
try:
    from queue import PriorityQueue
except:
    from Queue import PriorityQueue
    
  
from random import randrange, sample
import sys
import string
import time
import os
try: 
    dirname =  os.path.dirname(os.path.abspath(__file__))
 
    os.chdir(dirname)
except: 
    os.chdir("C:/Users/ntihish/Documents/IUB/Elem of AI/assignment 1/prgadugu-skandag-chhshar-a1/part1/")
start_time = time.time()
goal_state = [i for i in range(1,17)]


# shift a specified row left (1) or right (-1)
#state does not have a component of moves so far
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print ('%3d %3d %3d %3d' % (row[j:(j+4)]))

# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)
    
# The solver! - using BFS right now
"""
def solve(initial_board):
    fringe = [ (initial_board, "") ]
    while len(fringe) > 0:
        (state, route_so_far) = fringe.pop()
        for (succ, move) in successors( state ):
            if is_goal(succ):
                return( route_so_far + " " + move )
            fringe.insert(0, (succ, route_so_far + " " + move ) )
    return False
"""



def calculate_heuristic(state,goal_state):
    #define an ingenius heuristic here!

#    count = 0
#    for i in range(0,16,5):
#        
#        if goal_state[i] != state[i]:
#            
#            count  = count + 1
#    
#    return count 
    """
    1st heuristic
    
    """

    return max([sum([1 for i in range(0,16,5) if goal_state[i] != state[i]]),
                sum([1 for i in range(3,13,3) if goal_state[i] != state[i]])])


    """
    2nd heuristic overestimating high
    """

#    return sum([1 for i in range(16) if goal_state[i] != state[i]])

    #prop
    #forward diag
    """
    3rd explain the below heuristic
    time taken to calculate is high
    """
   
#    goalDiagElements = [1,6,11,16]
#        
#    mapGoalDiagElems = [(0,0),(1,1),(2,2),(3,3)]
#
#    curPositionDiagElems = [state.index(i) for i in goalDiagElements]
#    
#    cartIndexForCurDiagElems = [(int(index/4),index%4) for index in curPositionDiagElems]
#    
#    movementsFwd = sum([abs(cartIndexCur[0]-cartIndexGoal[0])+abs(cartIndexCur[0]-cartIndexGoal[0])  
#                    for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)])
#    
#    #repeat for backward diagonal
#    goalDiagElements = [4,7,10,13]
#    
#    mapGoalDiagElems = [(0,3),(1,2),(2,1),(3,0)]
#
#    curPositionDiagElems = [state.index(i) for i in goalDiagElements]
#    
#    cartIndexForCurDiagElems = [(4 - (int(index/4)),index%4) for index in curPositionDiagElems]
#    
#    movementsBwd = sum([abs(cartIndexCur[0]-cartIndexGoal[0])+abs(cartIndexCur[0]-cartIndexGoal[0])  
#                    for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)])
#
#    
#    
#    
#    return int(sum([movementsFwd,movementsBwd])/2)
    """
    Heuristic 4 :
    """
    
#    goalDiagElements = [1,6,11,16]
#        
#    mapGoalDiagElems = [(0,0),(1,1),(2,2),(3,3)]
#
#    curPositionDiagElems = [state.index(i) for i in goalDiagElements]
#    
#    cartIndexForCurDiagElems = [(int(index/4),index%4) for index in curPositionDiagElems]
#    
#    movementsFwd = [(abs(cartIndexCur[0]-cartIndexGoal[0]), abs(cartIndexCur[0]-cartIndexGoal[0]))  
#                    for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)]
#    
#    
#    
#    #repeat for backward diagonal
#    goalDiagElements = [4,7,10,13]
#    
#    mapGoalDiagElems = [(0,3),(1,2),(2,1),(3,0)]
#
#    curPositionDiagElems = [state.index(i) for i in goalDiagElements]
#    
#    cartIndexForCurDiagElems = [(4 - (int(index/4)),index%4) for index in curPositionDiagElems]
#    
#    movementsBwd = [(abs(cartIndexCur[0]-cartIndexGoal[0]),abs(cartIndexCur[0]-cartIndexGoal[0]))  
#                    for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)]
#    
#    rowFwd = sum(i[0] for i in movementsFwd)
#    colFwd = sum(i[1] for i in movementsFwd)
#    rowBwd = sum(i[0] for i in movementsBwd)
#    colBwd = sum(i[1] for i in movementsBwd)
#    
#
#    return max([rowFwd,colFwd,rowBwd,colBwd])

## rabbed manhattan distance 



def calculate_cost_so_far(path):
    #lets say each move costs a unit
    #split the path by space and count the total moves 
    return len(path.split(" "))

def HplusCost(state,goal_state,path):
    #define f(n) = h(n)+c(n)
    return calculate_cost_so_far(path) + calculate_heuristic(state,goal_state)     


def get_priority_membership_fringe(check_state,fringe):
    for priority ,(state,path) in fringe.queue:
        if check_state == state:
            return True , priority
    
    return False, -1  




def solve(initial_board):
    visited_states = {} #
    
    fringe = PriorityQueue()
    init_priority = HplusCost(initial_board,goal_state,"")
    
    
    fringe.put((init_priority,(initial_board, ""))) # (priority, data)
    while not fringe.empty():
        (priority,(state, route_so_far)) = fringe.get()
        ###changed the precedece of the is_goal to choose optimal path.
        
        visited_states[tuple(state)] = priority
        
        if is_goal(state):
            return(route_so_far)
            
            
        for (succ, move) in successors( state ):
            
            path = str(route_so_far + " " + move)
            
#            isInFringe, priorityInFringe = get_priority_membership_fringe(succ,fringe)
            calculatedPriority = HplusCost(succ,goal_state,path)
            
#            if not isInFringe and tuple(succ) not in visited_states:
            if tuple(succ) not in visited_states:
                fringe.put((calculatedPriority, (succ, path)))#(priority as func of path till,data)
            ###add code to check replace teh priority.
            
            
    return False



# test cases
try:
    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
    
    if len(start_state) != 16:
        print ("Error: couldn't parse start state file")

except:
    start_state = [1,2,3,13,4,6,12,16,5,10,11,7,14,15,8,9]


print ("Start state: ")
print_board(tuple(start_state))

print ("Solving...")
route = solve(tuple(start_state))

print ("Solution found in " + str(len(route)/3) + " moves:" + "\n" + route)
end_time = time.time()

print (end_time - start_time)





import timeit
state =[6, 2, 3, 4, 5, 1, 7, 8, 9, 10, 16, 12, 13, 14, 15, 11]
goal_state = [i for i in range(1,17)]

def heu1():
    return max([sum([1 for i in range(0,16,5) if goal_state[i] != state[i]]),
                sum([1 for i in range(3,13,3) if goal_state[i] != state[i]])])


def heu2():
    state =[6, 2, 3, 4, 5, 1, 7, 8, 9, 10, 16, 12, 13, 14, 15, 11]
    goalDiagElements = [1,6,11,16]
    
    mapGoalDiagElems = [(0,0),(1,1),(2,2),(3,3)]
    curPositionDiagElems = [state.index(i) for i in goalDiagElements]
    cartIndexForCurDiagElems = [(int(index/4),index%4) for index in curPositionDiagElems]
    movements = sum([abs(cartIndexCur[0]-cartIndexGoal[0])+abs(cartIndexCur[0]-cartIndexGoal[0])  
                    for cartIndexCur,cartIndexGoal in zip(cartIndexForCurDiagElems,mapGoalDiagElems)])
    
    
timeit.timeit(heu1) #4.6172454739029485
timeit.timeit(heu2) #7.57951648469642

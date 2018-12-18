#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 14:18:30 2018

@author: 18123
"""
import sys

#Taking the necessary inputs from Commandline

problem_type = sys.argv[1]
N= int(sys.argv[2])
no_of_block = int(sys.argv[3])
placesofblocks = (sys.argv[4:])
listOfBlockedCoords = []

#Forming a list of coordinates where we need to add the blockers.
if(no_of_block):
    x = 0
    list1 = []
    list2 = []
    for i in placesofblocks:
            if x % 2 != 0:
                list1.append(int(i)-1)
            else:
                list2.append(int(i)-1)
            x += 1
    
    for (r,c) in zip(list2,list1):
        listOfBlockedCoords.append([r,c])
    print(listOfBlockedCoords)


#Slightly changed version of printable board to accomodate the blockers.
def printable_board(board,g):
    st = ""
    for row in range(0,N):
        for col in range(0,N):
            if [row,col] in listOfBlockedCoords:
                st+= "X "
            elif(board[row][col] == 1):
                st+= g
            elif(board[row][col] == 0):
                st+="_ "
        st+="\n"
    return(st)
    
# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] )

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Successor function for N rooks
def successors_3(board):
    lis = []
    if(count_pieces(board) < N):
        for r in range(0,N):
            if(count_on_row(board,r) < 1):
                for c in range(0,N):
                    if (count_on_col(board,c)<1) and (board[r][c]!=1)  and [r,c] not in listOfBlockedCoords:
                        lis.append(add_piece(board, r, c))
                        break
    return(lis)
 
# Successor function for N queens 
def successors_3_queens(board):
    lis = []
    if(count_pieces(board) < N):
        for r in range(0,N):
            if(count_on_row(board,r) < 1):
                for c in range(0,N):
                    if (count_on_col(board,c)<1) and (board[r][c]!=1) and (count_on_diagnol(board, r, c)<1 and  [r,c] not in listOfBlockedCoords):
                            lis.append(add_piece(board, r, c))
                            break
    return(lis)
# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Count the # of pieces on the intersecting diagnols at r,c
def count_on_diagnol(board, r, c):
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0
    for i in range(N):
        if (r-i) >= 0  and (c+i) < N:
            s1 = s1 + board[r-i][c+i]       
    for i in range(N):
        if (r+i) < N  and (c-i) >= 0:
            s2 = s2 + board[r+i][c-i]
    for i in range(N):
        if (r+i) < N and (c+i) < N:
            s3 = s3 + board[r+i][c+i]
    for i in range(N):
        if (r-i) >= 0 and (c-i) >= 0:
            s4 = s4 + board[r-i][c-i]
    return(s1+s2+s3+s4-(2*board[r][c]))

# Function to invoke n rooks
def nrook():
    initial_board = [[0]*N]*N
    print ("Starting from initial board:\n" + printable_board(initial_board,"R ") + "\n\nLooking for solution...\n")
    def solve_nrooks(initial_board):
        fringe = [initial_board]
        while len(fringe) > 0:
            for s in successors_3( fringe.pop() ):
                if is_goal(s):
                    return(s)
                fringe.append(s)
        return False
    solution = solve_nrooks(initial_board)
    print (printable_board(solution,"R ") if solution else "Sorry, no solution found. :(")

# Function to invoke n queens

def nqueen():
    initial_board_1 = [[0]*N]*N
    print ("Starting from initial board:\n" + printable_board(initial_board_1,"Q ") + "\n\nLooking for solution...\n")
    def solve_nqueens(initial_board_1):
        fringe = [initial_board_1]
        while len(fringe) > 0:
            for s in successors_3_queens( fringe.pop() ):
                if is_goal(s):
                    return(s)
                fringe.append(s)
        return False
    solution = solve_nqueens(initial_board_1)
    print (printable_board(solution,"Q ") if solution else "Sorry, no solution found. :(")

# To run the required problem.

if problem_type == "nrook":
    nrook()
elif problem_type == "nqueen":
    nqueen()


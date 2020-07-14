import sys
import numpy as np
import time
import random

total_number_of_assignments = -1                            # Global Assignment Varriable

#################################################################  Question 1  ###################################################################

def under_attack(point, queens):                            # Update to check for point in a list of tuples
    flag1 = False
    for i in queens:
        if (point[0] == i[0] or point[1] == i[1]):
            flag1 = True
    return any(abs(point[1] - x) == abs(point[0]-i) for i,x in queens) or flag1

def rsolve(queens):                                         # Old Backtracking Implementation
    global total_number_of_assignments                      # Everytime method is called, something is assigned (starts at -1 to get rid of first assignment)
    total_number_of_assignments += 1                        # Increment assignment each time method is called
    if BOARD_SIZE == len(queens):
        return queens
    else:
        for i in range(BOARD_SIZE): 
            if not under_attack((len(queens),i),queens):
                newqueens = rsolve(queens+[(len(queens),i)])
                if newqueens != []:
                    return newqueens
        return [] # FAIL

#################################################################  Question 2  ###################################################################

def lcv(queens):                                            # Least Constraint Implementation (Uses List of Tuples for Queens)
    global total_number_of_assignments                      # Everytime method is called, something is assigned (starts at -1 to get rid of first assignment)
    total_number_of_assignments += 1                        # Increment assignment each time method is called
    if BOARD_SIZE == len(queens):                           # Check if all the Queens are assigned
        return queens
    else:
        choice = optimal_points(queens)                     # If a Queen is placed, calculates the impact on the board and returns the least impactful points (low to high)
        for j in choice:                                    # Loops through points in the least constraining row
            newqueens = lcv(queens+[(j[1],j[2])])           # Assigns point and recurses
            if newqueens != []:                             # Checks for deadend
                return newqueens
        return []                                           # FAIL

#################################################################  Question 3  ###################################################################

def lcv_ac3(queens):                                        # Least Constraint Implementation (Uses List of Tuples for Queens)
    global total_number_of_assignments                      # Everytime method is called, something is assigned (starts at -1 to get rid of first assignment)
    total_number_of_assignments += 1                        # Increment assignment each time method is called 
    if BOARD_SIZE == len(queens):                           # Check if all the Queens are assigned
        return queens
    else:
        choice = optimal_points(queens)                     # If a Queen is placed, calculates the impact on the board and returns the least impactful points (low to high)                           
        for j in choice:                                    # Loops through points in the least constraining row
            upDateMap(j[1],j[2],1)                          # Adds newest Queen test
            if not check_arc_consistency():                 # Checks for arc consistency
                newqueens = []                              # DOES NOT ASSIGN IF LEADS TO INCONSISTENCY
            else:  
                newqueens = lcv_ac3(queens+[(j[1],j[2])])   # Assigns point and recurses
            if newqueens != []:                             # Checks for deadend
                return newqueens
            upDateMap(j[1],j[2],0)                          # Removes newest Queen test
    return []                                               # FAIL

def upDateMap(row,column,flag):                             # Adds or Substracts Queen depending on flag
    global bitMap
    global arc_List
    arc_List = []                                           # Clears Arc Consistency List
    for i in range(BOARD_SIZE):                             
        arc_List+=[[]]
    if(flag):                                               # Points are added
        add = 1.0    
        queen = -1.0   
    else:                                                   # Points are removes
        add = -1.0
        queen = 0.0    
    for i in range (BOARD_SIZE):                            # Loop through Board
        bitMap[row][i] += add                               # Updates for row impact 
        bitMap[i][column] += add                            # Updates for column impact 
    bitMap[row][column] = queen                             # Updates 1 for double counting
                                                            # Updates for right upper diagonal impact
    i = row + 1
    j = column + 1
    while(i < BOARD_SIZE and j < BOARD_SIZE):
        bitMap[i][j] += add
        i += 1
        j += 1
                                                            # Updates for right lower diagonal impact
    i = row + 1
    j = column - 1
    while(i < BOARD_SIZE and j > -1):
        bitMap[i][j] += add
        i += 1
        j -= 1
                                                            # Updates for left upper diagonal impact
    i = row - 1
    j = column + 1
    while(i > -1 and j < BOARD_SIZE):
        bitMap[i][j] += add
        i -= 1
        j += 1
                                                            # Updates for left lower diagonal impact
    i = row - 1
    j = column - 1
    while(i > -1 and j > -1):
        bitMap[i][j] += add
        i -= 1
        j -= 1
    assign_arc_consistency()  

def assign_arc_consistency():                               # Transfers Map to Consistency List
    global bitMap
    global arc_List
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (bitMap[i][j] == -1.0):                      # Queen Check
                arc_List[i] = [j]
                break
            if (bitMap[i][j] == 0.0):                       # Open Slot Check
                arc_List[i] += [j]

def check_arc_consistency():                                # Checks if consistent if element is added
    global arc_List
    for i in arc_List:
        if len(i) == 0:                                     # Empty list returns Fail
            return False
    return True

#################################################################  Question 4  ###################################################################

def setBoard(queens):
    for i in range(BOARD_SIZE):                                    
        queens += [random.randint(0,BOARD_SIZE-1)]          # Assigns random column to row     
    return minConflictSort(currentState(queens),queens)

def currentState(queens):
    if(conflicted(queens) == -1):                           # Check for any conflicted queens
        return True
    return False

def minConflictSort(current_State,queens):
    global maxSteps
    global total_number_of_assignments                      # Everytime method is called, something is assigned (starts at -1 to get rid of first assignment)
    while(True):                                            # Tries to solve problem while True
        if current_State:                                   # Check if queens is optimal
            return queens                                   
        if(total_number_of_assignments == maxSteps):        # Checks if maxSteps is reached
            return []
        total_number_of_assignments += 1                    # Increment assignment each time method is called 
        var = conflicted(queens)                            # Returns row of random conflicted queen
        value = minConflict(var,queens)                     # Returns row of with minimum conflicts
        queens[var] = value                                 # Changes a conflicted queen's value to a value with minimum conflicts
        current_State = currentState(queens)                # Assigns optimality of the queens                           
    return []                                               # Not Solvable

def conflicted(queens):                                     # Checks for conflicted queens
    conflicted_Queens = []
    for i in range(BOARD_SIZE):
        if(conflicts(queens[i],i,queens) > 0):              # Checks for conflicts
            conflicted_Queens += [i]
    if (len(conflicted_Queens) == 0):                       # Check if there is a conflict
        return -1
    var = random.choice(conflicted_Queens)                  # Chooses a random conflicted queen                               
    return var                                              # Returns column of a conflicted queen

def conflicts(i,var,queens):                                # Checks for conflicts
    conflicts = 0
    for j in range(BOARD_SIZE):                             # Loops through rows of board
        if j == var:                                        # Skips check for same value
            continue
        newColumn = queens[j]                                   # assign the queen's column of a given row
        if (newColumn == i or abs(newColumn-i) == abs(j-var)):  # Checks for conflicting diagonals and columns
            conflicts += 1                                      # Increment conflicts
    return conflicts

def minConflict(var,queens):                                # Calculates a row with minimum conflicts
    minConflicts = BOARD_SIZE
    minConflicts_List = []
    for i in range(BOARD_SIZE):
        numberOfConflicts = conflicts(i,var,queens)
        if numberOfConflicts == minConflicts:               # Checks for ties
            minConflicts_List += [i]
        if numberOfConflicts < minConflicts:                # Checks for smaller conflicts
            minConflicts = numberOfConflicts
            minConflicts_List.clear()
            minConflicts_List += [i]
    value = random.choice(minConflicts_List)                # Chooses a random minimum conflict point
    return value                                            # returns row
        
################################################### USED BY QUESTIONS 1, 2 AND/OR 3 ##########################################################

def optimal_points(queens):                                 # Finds the least constraint points for the least constraint column
    point_weights = []                                      # Holds lowest constraint column in the next row
    for i in range(BOARD_SIZE):                             # Loops through possible columns
        weight_counter = 0
        if not under_attack((len(queens),i),queens):            # Checks if there is Queen at the selected point
            weight_counter += 1                                 # Counts initial point
                                                            # Only Diagonals
                                                            # Checks for right lower diagonal impact
            row =  len(queens) + 1
            column = i + 1
            while(row < BOARD_SIZE and column < BOARD_SIZE):
                if not under_attack((row,column),queens):
                    weight_counter += 1
                row += 1
                column += 1
                                                            # Checks for left lower diagonal impact
            row = len(queens) + 1
            column = i - 1
            while(row < BOARD_SIZE and column > -1):
                if not under_attack((row,column),queens):
                    weight_counter += 1
                row += 1
                column -= 1
                                                                # Checks for left upper diagonal impact
            row = len(queens) - 1   
            column = i + 1
            while(row > -1 and column < BOARD_SIZE):
                if not under_attack((row,column),queens):
                    weight_counter += 1
                row -= 1
                column += 1
                                                                # Checks for right upper diagonal impact
            row = len(queens) - 1                           
            column = i - 1
            while(row > -1 and column > -1):
                if not under_attack((row,column),queens):
                    weight_counter += 1
                row -= 1
                column -= 1
            point_weights += [(weight_counter,len(queens),i)]       # Updates the column constraint list
    point_weights.sort()                                            # Sorts points in least constraint order
    return point_weights

def cleanup_Queens(queens):                                 # Changes List of Tuples to List of Queens
    queens.sort()
    ans = []
    for i in queens:
        ans = ans+[i[1]]
    return ans


def print_board(queens):                                    # Prints Board
    n = len(queens)
    for pos in queens:
        for i in range(pos):
            sys.stdout.write( ". ")
        sys.stdout.write( "Q ")
        for i in range((n-pos)-1):
            sys.stdout.write( ". ")
        sys.stdout.write("\n")                              # My python version didn't print the new line
        print

BOARD_SIZE = 4                                          
results = []
arc_List = []                                                       # Creates List for Arc Consistency  (Q3) 
boardcheck = input("Input board size (4 if enter): " )
if not (boardcheck == ""):
    BOARD_SIZE = int(boardcheck)
    

bitMap = np.zeros((BOARD_SIZE,BOARD_SIZE))                          # Creates Board for Arc Consistency (Q3)
maxSteps = -1                                                       # Check maximum steps

Backtracking_flag = input("Do you want to run backtracking? (Y/N) (Default No)")
LCV_Dflag = input("Do you want to run least-constraining-value? (Y/N) (Default No)")
ALCV_Dflag = input("Do you want to run least-constraining-value with arc-consistency checking? (Y/N) (Default No)")
MinConflicts_flag = input("Do you want to run min-conflicts local search? (Y/N) (Default No)")

if(MinConflicts_flag == "Y" or MinConflicts_flag == "y"):
    stepcheck = input("What is your maxSteps for min-conflicts local search? (Infinite if enter)")
    if not (stepcheck == ""):
        maxSteps = int(stepcheck)

                                                        # Back Tracing
if(Backtracking_flag == "Y" or Backtracking_flag == "y"):
    start_time = time.time()                                                      
    ans_tuples = rsolve([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"Back Tracking",ans)]

                                                        # Least Constraint Value

if(LCV_Dflag == "Y" or LCV_Dflag == "y"):
    total_number_of_assignments = -1
    start_time = time.time()
    ans_tuples = lcv([])
    ans = cleanup_Queens(ans_tuples)
    executionTime = time.time() - start_time
    results += [(total_number_of_assignments,executionTime,"LCV: Diagonals",ans)]

                                                        # Arc Consistency

if(ALCV_Dflag == "Y" or ALCV_Dflag == "y"):
    total_number_of_assignments = -1
    start_time = time.time()
    ans_tuples = lcv_ac3([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"LCV AC3: Diagonals",ans)]

                                                        # Min-conflict local search

if(MinConflicts_flag == "Y" or MinConflicts_flag == "y"):
    total_number_of_assignments = 0
    start_time = time.time()
    ans = setBoard([])
    result = " SUCCESSFUL"                              # Check if queens are in final position
    if(ans == []):
        result = " FAILED"                              
    executionTime = time.time() - start_time
    results += [(total_number_of_assignments,executionTime,"Minimum Conflict"+result,ans)]

print("---------------------------------------------------------------------------------------------")
if not (len(results) == 0):
    print("                           AND THE RESULTS FOR ",BOARD_SIZE," BOARD SIZE")
    results.sort()
    print("---------------------------------------------------------------------------------------------")
else:
    print("                           NO ALGORITHMS RUN FOR ",BOARD_SIZE, " BOARD SIZE")
for i in results:
    print("METHOD:          ",i[2])
    print("EXECUTION TIME:  ",i[1], " secs")
    print("ASSIGNMENTS:     ",i[0])
    #print_board(i[3])
    print("---------------------------------------------------------------------------------")
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

#################################################################  Question 4  ###################################################################

def minConflictSort():
    queens = []                                             # Create new Queens List
    for i in range(BOARD_SIZE):                                    
        queens += [(i,random.randint(0,BOARD_SIZE))]        # Randomly assigns each columns to rows
    random.shuffle(queens)                                  # Shuffles the queens

#################################################################  Question 3  ###################################################################

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
    assign_arc_consistency()                                # Transfers map to Consisency List
        
def lcv_ac3(queens):                                        # Least Constraint Implementation (Uses List of Tuples for Queens)
    global total_number_of_assignments                      # Everytime method is called, something is assigned (starts at -1 to get rid of first assignment)
    total_number_of_assignments += 1                        # Increment assignment each time method is called 
    if BOARD_SIZE == len(queens):                           # Check if all the Queens are assigned
        return queens
    else:
        columns = possibleColumns(queens)                   # Columns without Queens
        choice = optimal_points(columns,queens)             # If a Queen is placed, calculates the impact on the board and returns the least impactful points (low to high) of the least impactful column (chooses lowest if tie)                             
        for j in choice:                                    # Loops through points in the least constraining row
            upDateMap(j[1],j[2],1)                          # Adds newest Queen test
            if not check_arc_consistency():                 # Checks for arc consistency
                newqueens = []                              # DOES NOT ASSIGN IF LEADS TO INCONSISTENCY
            else:  
                newqueens = lcv_ac3(queens+[(j[1],j[2])])   # Assigns point and recurses
            if newqueens != []:                             # Checks for deadend
                return newqueens
            upDateMap(j[1],j[2],0)                      # Removes newest Queen test
    return []                                               # FAIL

#################################################################  Question 2  ###################################################################

def lcv(queens):                                            # Least Constraint Implementation (Uses List of Tuples for Queens)
    global total_number_of_assignments                      # Everytime method is called, something is assigned (starts at -1 to get rid of first assignment)
    total_number_of_assignments += 1                        # Increment assignment each time method is called 
    if BOARD_SIZE == len(queens):                           # Check if all the Queens are assigned
        return queens
    else:
        columns = possibleColumns(queens)                   # Columns without Queens
        choice = optimal_points(columns,queens)             # If a Queen is placed, calculates the impact on the board and returns the least impactful points (low to high) of the least impactful column (chooses lowest if tie)                             
        for j in choice:                                    # Loops through points in the least constraining row
            newqueens = lcv(queens+[(j[1],j[2])])           # Assigns point and recurses
            if newqueens != []:                             # Checks for deadend
                return newqueens
    return []                                               # FAIL

def possibleColumns(queens):                                # Checks for rows without Queens
    columns = []                                                   
    flag = True                                            
    for i in range(BOARD_SIZE):                             # Loops through columns
        for j in queens:            
            if(j[1] == i):                                  # Checks if Queen is in selected column
                flag = False
        if flag:
            columns += [i]                                  # Adds to a list of posisble columns
        flag = True
    return columns

def optimal_points(columns,queens):                                 # Finds the least constraint points for the least constraint column
    point_weights = []                                              # Holds points and its contraint (weight)
    column_weights = []                                             # Holds column and its contraint (weight)
    optimal_points = []                                             # Holds lowest constraint column and its points in sorted order of constraint
    k = 0
    while k < len(columns):                                         # Loops through possible columns
        column_weight_counter = 0
        no_column_left_behind = True                                # Check if a possible column is full due to other queens
        for i in range(BOARD_SIZE):                                 # Loops through all rows
            weight_counter = 0                                      # Counts initial point
            if not under_attack((i,columns[k]),queens):             # Checks if there is Queen at the selected point
                no_column_left_behind = False                       # There exists a point in possible column
                weight_counter += 1                                 # Counts initial point
                if(rowsAndColumns):                                 # Only Row and Column weights
                    for j in range (BOARD_SIZE):
                        if not under_attack((j,columns[k]),queens): # Checks for column impact 
                            weight_counter += 1
                        if not under_attack((i,j),queens):          # Checks for row impact
                            weight_counter += 1                 
                    weight_counter -= 2                             # Removes 2 for double counting
                if(diagonals):                                      # Only Diagonals
                                                                    # Checks for right lower diagonal impact
                    row =  i + 1
                    column = columns[k] + 1
                    while(row < BOARD_SIZE and column < BOARD_SIZE):
                        if not under_attack((row,column),queens):
                            weight_counter += 1
                        row += 1
                        column += 1
                                                                    # Checks for left lower diagonal impact
                    row = i + 1
                    column = columns[k] - 1
                    while(row < BOARD_SIZE and column > -1):
                        if not under_attack((row,column),queens):
                            weight_counter += 1
                        row += 1
                        column -= 1
                                                                        # Checks for left upper diagonal impact
                    row = i - 1   
                    column = columns[k] + 1
                    while(row > -1 and column < BOARD_SIZE):
                        if not under_attack((row,column),queens):
                            weight_counter += 1
                        row -= 1
                        column += 1
                                                                        # Checks for right upper diagonal impact
                    row = i - 1                           
                    column = columns[k] - 1
                    while(row > -1 and column > -1):
                        if not under_attack((row,column),queens):
                            weight_counter += 1
                        row -= 1
                        column -= 1
                point_weights += [(weight_counter,i,columns[k])]    # Updates the point constraint list
            column_weight_counter += weight_counter                 # Increments the row constraint
        if(no_column_left_behind):                                  # Possible Column with no points
            return []
        column_weights += [(column_weight_counter,columns[k])]      # Updates the column constraint list
        k += 1
    column_weights.sort()                            
    best_column = (column_weights[0])[1]                            # Finds the least constraint column  
    for l in point_weights:                                         # Checks for points of the least constraint column
        if(l[2] == best_column):
            optimal_points += [l]
    optimal_points.sort()                                           # Sorts points in least constraint order
    return optimal_points

def cleanup_Queens(queens):                                         # Changes List of Tuples to List of sorted Queens
    queens.sort()
    ans = []
    for i in queens:
        ans = ans+[i[1]]
    return ans

def print_board(queens):                                            # Prints Board
    n = len(queens)
    for pos in queens:
        for i in range(pos):
            sys.stdout.write( ". ")
        sys.stdout.write( "Q ")
        for i in range((n-pos)-1):
            sys.stdout.write( ". ")
        sys.stdout.write("\n")                                      # My version did not print \n
        print

results = []
arc_List = []                                                       # Creates List for Arc Consistency  (Q3) 
BOARD_SIZE = int(input("Input board size: "))
bitMap = np.zeros((BOARD_SIZE,BOARD_SIZE))                          # Creates Board for Arc Consistency (Q3)

Backtracking_flag = input("Do you want to run backtracking? (Y/N)")
LCV_HVflag = input("Do you want to run Row and Column only LCV? (Y/N)")
LCV_Dflag = input("Do you want to run Diagonal only LCV? (Y/N)")
LCV_HVDflag = input("Do you want to run Row and Column and Diagonal LCV? (Y/N)")
ALCV_HVflag = input("Do you want to run Row and Column only LCV AC3? (Y/N)")
ALCV_Dflag = input("Do you want to run Diagonal only LCV AC3? (Y/N)")
ALCV_HVDflag = input("Do you want to run Row and Column and Diagonal LCV AC3? (Y/N)")

                                                        # Back Tracing
if(Backtracking_flag == "Y" or Backtracking_flag == "y"):
    start_time = time.time()                                                      
    ans_tuples = rsolve([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"Back Tracking",ans)]
    total_number_of_assignments = -1
                                                        # Least Constraint Value
if(LCV_HVflag == "Y" or LCV_HVflag == "y"):
    rowsAndColumns = True
    diagonals = False
    start_time = time.time()
    ans_tuples = lcv([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"LCV: Rows,Columns",ans)]
    total_number_of_assignments = -1

if(LCV_Dflag == "Y" or LCV_Dflag == "y"):
    diagonals = True
    rowsAndColumns = False
    start_time = time.time()
    ans_tuples = lcv([])
    ans = cleanup_Queens(ans_tuples)
    executionTime = time.time() - start_time
    results += [(total_number_of_assignments,executionTime,"LCV: Diagonals",ans)]
    total_number_of_assignments = -1

if(LCV_HVDflag == "Y" or LCV_HVDflag == "y"):
    diagonals = True
    rowsAndColumns = True
    start_time = time.time()
    ans_tuples = lcv([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"LCV: Rows,Columns,Diagonals",ans)]
    total_number_of_assignments = -1
                                                        # Arc Consistency
if(ALCV_HVflag == "Y" or ALCV_HVflag == "y"):
    rowsAndColumns = True
    diagonals = False
    start_time = time.time()
    ans_tuples = lcv_ac3([])  
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"LCV AC3: Rows,Columns",ans)]
    bitMap = np.zeros((BOARD_SIZE,BOARD_SIZE))              # zero out map for next
    total_number_of_assignments = -1

if(ALCV_Dflag == "Y" or ALCV_Dflag == "y"):
    diagonals = True
    rowsAndColumns = False
    start_time = time.time()
    ans_tuples = lcv_ac3([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)
    results += [(total_number_of_assignments,executionTime,"LCV AC3: Diagonals",ans)]
    bitMap = np.zeros((BOARD_SIZE,BOARD_SIZE))              # zero out map for next
    total_number_of_assignments = -1

if(ALCV_HVDflag == "Y" or ALCV_HVDflag == "y"):
    diagonals = True
    rowsAndColumns = True
    start_time = time.time()
    ans_tuples = lcv_ac3([])
    executionTime = time.time() - start_time
    ans = cleanup_Queens(ans_tuples)                                                        
    results += [(total_number_of_assignments,executionTime,"LCV AC3: Rows,Columns,Diagonals",ans)]
    bitMap = np.zeros((BOARD_SIZE,BOARD_SIZE))              # zero out map for next
    total_number_of_assignments = -1

print("                                 AND THE RESULTS FOR ",BOARD_SIZE)
results.sort()
print("---------------------------------------------------------------------------------")
for i in results:
    print("METHOD:          ",i[2])
    print("EXECUTION TIME:  ",i[1], " secs")
    print("ASSIGNMENTS:     ",i[0])
    #print_board(i[3])
    print("---------------------------------------------------------------------------------")

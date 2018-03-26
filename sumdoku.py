import numpy as np
import sys
from math import ceil
condition_index = {0: [0], 1: [0,1], 2: [1], 3: [2], 4: [2,3], 5: [3], 6: [4], 7: [4,5], 8: [5]}
grid = np.zeros((9,9),dtype=int).tolist()
condition_row = list()
condition_column = list()

def findNextCellToFill(i, j):
        for x in range(i,9):
                for y in range(j,9):
                        if grid[x][y] == 0:
                                return x,y
        for x in range(0,9):
                for y in range(0,9):
                        if grid[x][y] == 0:
                                return x,y
        print(x,y)
        return -1,-1

def evalCondition(values,condition):
    if all([x != 0 for x in values]) == False:
        return True
    if condition == -1:
        return sum(values) < 10
    elif condition == 0:
        return sum(values) == 10
    else:
        return sum(values) > 10

def evalRowCriteria(i,j,e,condition):
    index = iter(condition_index[j])
    if j%3 != 0:
        # if evalCondition([grid[i][j-1],e],condition[index.next()]) == False:
        if evalCondition([grid[i][j-1],e],condition[next(index)]) == False:
            return False
    if (j-2)%3 != 0:
        # if evalCondition([e,grid[i][j+1]],condition[index.next()]) == False:
        if evalCondition([e,grid[i][j+1]],condition[next(index)]) == False:
            return False
    return True

def evalColumnCriteria(i,j,e,condition):
    index = iter(condition_index[i])
    if i%3 != 0:
        # if evalCondition([grid[i-1][j],e],condition[index.next()]) == False:
        if evalCondition([grid[i-1][j],e],condition[next(index)]) == False:
            return False
    if (i-2)%3 != 0:
        # if evalCondition([e,grid[i+1][j]],condition[index.next()]) == False:
        if evalCondition([e,grid[i+1][j]],condition[next(index)]) == False:
            return False
    return True


def isValid(i, j, e):
        rowOk = all([e != grid[i][x] for x in range(9)]) and evalRowCriteria(i,j,e,condition_row[i])
        if rowOk:
            columnOk = all([e != grid[x][j] for x in range(9)]) and evalColumnCriteria(i,j,e,condition_column[j])
            if columnOk:
                    # finding the top left x,y co-ordinates of the section containing the i,j cell
                    secTopX, secTopY = 3 *(i//3), 3 *(j//3)
                    for x in range(secTopX, secTopX+3):
                            for y in range(secTopY, secTopY+3):
                                    if grid[x][y] == e:
                                            return False
                    return True
        return False

def solveSudoku(i=0, j=0):
        i,j = findNextCellToFill(i, j)
        if i == -1:
                return True
        for e in range(1,10):
                if isValid(i,j,e):
                        grid[i][j] = e
                        if solveSudoku(i, j):
                                return True
                        # Undo the current cell for backtracking
                        grid[i][j] = 0
        return False

def condition_map(condition):
    if condition == "<":
        return -1
    elif condition == "=":
        return 0
    else:
        return 1

def parseCondition(conditions):
    row_indices = [0,2,4,5,7,9,10,12,14]
    column_indices = [1,3,6,8,11,13]
    col_condition = list()
    row = list()
    column = list()
    for index in row_indices:
        row.append(list(map(condition_map,list(conditions[index]))))
    for index in column_indices:
        col_condition.append(list(map(condition_map,list(conditions[index]))))
    column = list(map(list,zip(*col_condition)))
    return row,column


fileName = sys.argv[1]
with open(fileName) as f:
    x = f.read()
# temp_condition = x.split('\n')
parser_input = x.split('\n')
number_of_test_cases = int(parser_input[0])
count = 1
for i in range(number_of_test_cases):  # number_of_test_cases
    test_case = parser_input[count: count+16]
    index = test_case[0]
    temp_condition = test_case[1:]
    print(index, temp_condition)
    condition_row,condition_column = parseCondition(temp_condition)
    solveSudoku()
    print(grid)
    grid = np.zeros((9,9),dtype=int).tolist()
    count = count + 16

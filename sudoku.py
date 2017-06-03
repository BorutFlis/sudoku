import itertools

"""
def solve(puzzle):
    candidates=[]
    for i in range(9):
        for j in range(9):
            candidates[i][j]=[]

    #filling up candidates
    for row in puzzle:
        for square in row:
"""            

def findSquare(puzzle):
    #find the square with least amount of candidates
    candidates=[]
    least_candidates=9
    least_i=-1
    least_j=-1
    for i in range(9):
        candidates.append([set([1,2,3,4,5,6,7,8,9]) if puzzle[i][j]==0 else None for j in range(9)])
    #mistake there is a set appended where there is already a solution
    for i in range(9):
        for j in range(9):
            if puzzle[i][j]==0:
                for candidate in puzzle[i]:
                    if candidate in candidates[i][j]:
                        candidates[i][j].remove(candidate)
                #all the numbers in the row of the puzzle
                for row in range(9):
                    if puzzle[row][j] in candidates[i][j]:
                        candidates[i][j].remove(puzzle[row][j])
                #all the numbers in the column of the puzzle
                begin_i=i-(i%3)
                begin_j=j-(j%3)
                for sub_i in range(begin_i,begin_i+3):
                    for sub_j in range(begin_j,begin_j+3):
                        if puzzle[sub_i][sub_j] in candidates[i][j]:
                            candidates[i][j].remove(puzzle[sub_i][sub_j])
                #all the numbers in the square
                if len(candidates[i][j]) < least_candidates:
                    least_candidates=len(candidates[i][j])
                    least_i=i
                    least_j=j
    return least_i, least_j, candidates

def isValid(puzzle):
    #First check if the argument is not false
    if puzzle!=False:
        #checks rows
        for row in puzzle:
            if not sudoku_ok_and_complete(row):
                print("Row ",row ," is wrong.")
                return False
        reverse_grid = list(zip(*puzzle))
        #checks columns
        for column in reverse_grid:
            if not sudoku_ok_and_complete(column):
                print("Column ",column ," is wrong.")
                return False
        #checks squares
        for i in range(0,9,3):
            for j in range(0,9,3):
                square=[]
                for row in puzzle[i:i+3]:
                    square.extend(row[j:j+3])
                if not sudoku_ok_and_complete(square):
                    print("Square ",i," ",j," is wrong.")
                    print(square)
                    return False
        return True


def sudoku_ok(line):
    if(max(line)>9 or min(line)<=0):
        return False
    return (len(line) == 9 and sum(line) == sum(set(line)))
    
def sudoku_ok_and_complete(line):
    if(max(line)>9 or min(line)<=0):
        return False
    return(len(line) == 9 and sum(line) == sum(set(line)) == 45)

def backtrack(puzzle):
    x,y,candidates=findSquare(puzzle)
    if x==-1 and y==-1:
        return puzzle #stop condition
    while len(candidates[x][y])>0:
        puzzle[x][y]=candidates[x][y].pop()
        puzzler=backtrack(puzzle)
        if isValid(puzzler):
            return puzzler
        else:
            return False



puzzle=[
        [0,6,5,3,0,9,0,1,0],
        [0,0,8,0,7,6,2,0,0],
        [7,0,9,4,0,0,0,0,0],
        [6,0,0,7,0,0,0,0,1],
        [0,9,0,8,6,2,0,7,0],
        [4,0,0,0,0,1,0,0,8],
        [0,0,0,0,0,7,5,0,3],
        [0,0,4,2,9,0,1,0,0],
        [0,7,0,5,0,3,9,4,0]
        ]


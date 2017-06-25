import itertools, os, bdb, copy

def import_sudokus():
    sudokus=[]
    f=open("sudokus_in_string.txt")
    for line in f:
        p,s=line.split()
        puzzle=[]
        solution=[]
        for i in range(9):
            puzzle.append(list(map(int,p[i*9:i*9+9])))
            solution.append(list(map(int,s[i*9:i*9+9])))
        sudokus.append((puzzle,solution))
    f.close()
    return sudokus


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
                if len(candidates[i][j])==0:
                    #it means the quess was wrong
                    return i,j,candidates
                
                if len(candidates[i][j]) < least_candidates:
                    least_candidates=len(candidates[i][j])
                    least_i=i
                    least_j=j
    return least_i, least_j, candidates

def isValid(puzzle):
    #First check if the argument is not false
    #print(puzzle)
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
    else:
        return False


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
    iter=0
    while len(candidates[x][y])>0:
        puzzle[x][y]=candidates[x][y].pop()
        puzzler=backtrack(copy.deepcopy(puzzle))
        if isValid(puzzler):
            return puzzler
    return False


def rule_based(puzzle):
    while True:
        #naked_single(puzzle)
        puzzle,applied=hidden_single(puzzle)
        if applied:
            continue
        break
    return backtrack(puzzle)

"""
def naked_single(puzzle):
    #checks if any of the squares have 0 candidates
"""
def hidden_single(puzzle):
    applied=False
    #a boolean variable which is set to true if we find a hidden_single
    for i,row in enumerate(puzzle):
        list_of_candidates=[0,0,0,0,0,0,0,0,0]
        for j in range(len(row)):
            if row[j]==0:
                #check if it is an empty space
                #we are looking for a candidate that is possible
                #in only one square, even though that square might
                #have more candidates
                set_of_candidates=set(range(1,10))-set(row)
                for sub_row in range(len(puzzle)):
                    set_of_candidates.discard(puzzle[sub_row][j])
                #remove all the candidates from the column
                begin_i=i-(i%3)
                begin_j=j-(j%3)
                for sub_i in range(begin_i, begin_i+3):
                    for sub_j in range(begin_j,begin_j+3):
                        set_of_candidates.discard(puzzle[sub_i][sub_j]) 
                #remove all the candidates from the square
                list_of_candidates[j]=set_of_candidates
        multi_candidates=dict()
        #dictionary that will count the number of occurences of candidates
        for candidates in list_of_candidates:
            if candidates!=0:
            #checks if the square is empty
                for candidate in candidates:
                    if candidate in multi_candidates:
                        multi_candidates[candidate]+=1
                    else:
                        multi_candidates[candidate]=1
                
        for j,candidates in enumerate(list_of_candidates):
            if candidates!=0:
            #checks if the square is empty
                if len(candidates)==1 :
                    #naked single
                    puzzle[i][j]=candidates.pop()
                    continue
                for candidate in candidates:
                    if multi_candidates[candidate]==1:
                        #hidden single
                        applied=True
                        puzzle[i][j]=candidate
                        break
    return puzzle, applied
                    
                    
                    
            

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

puzzle1=[[0, 0, 0, 7, 0, 4, 0, 0, 5],
         [0, 2, 0, 0, 1, 0, 0, 7, 0], 
         [0, 0, 0, 0, 8, 0, 0, 0, 2], 
         [0, 9, 0, 0, 0, 6, 2, 5, 0], 
         [6, 0, 0, 0, 7, 0, 0, 0, 8], 
         [0, 5, 3, 2, 0, 0, 0, 1, 0],
         [4, 0, 0, 0, 9, 0, 0, 0, 0], 
         [0, 3, 0, 0, 6, 0, 0, 9, 0], 
         [2, 0, 0, 4, 0, 7, 0, 0, 0]]


#backtrack(puzzle1)
#import_sudokus()


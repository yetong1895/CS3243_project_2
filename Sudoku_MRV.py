import sys
import copy
import heapq
import collections

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

#class Check:
#Get the location of empty cell
def empty_cell(grid):
	for row in range(9):
		for col in range(9):
			if(grid[row][col] == 0):
				return True
	return False

#check if the number to assign exists in the row
def not_in_row(grid, row, num):
	for i in range(9):
		if(grid[row][i] == num):
			return False
	return True

#check if the number to assign exists in the column
def not_in_col(grid, col, num):
	for i in range(9):
		if(grid[i][col] == num):
			return False
	return True
		
#check if the number to assign exists in its subgrid
def not_in_subgrid(grid, row, col, num):
	r = row - row % 3
	c = col - col % 3
	for i in range(3):
		for j in range(3):
			if(grid[i+r][j+c] == num):
				return False
	return True

#check if the number to assign is valid
def is_valid(grid, row, col, num):
	if(not_in_row(grid, row, num) and not_in_col(grid, col, num) and not_in_subgrid(grid, row, col, num)):
		return True
	else:
		return False

def select_variables(puzzle):
	min_value = 10
	row = 0
	col = 0
	value_list = collections.deque() #list to store possible values of that variable
	for i in range(9):
		for j in range(9):
			if(puzzle[i][j] == 0): #find a variable
				temp_list = collections.deque()
				count = 0 #number of possible values
				for num in range(1, 10): #check for possible values
					if(is_valid(puzzle, i, j, num)):
						temp_list.append(num)
						count += 1
				if(count == 0): #no possible values for this variable hence stop exploring
					return False
				elif(count < min_value): #update info
					min_value = count
					row = i
					col = j
					value_list = temp_list
	return row, col, value_list, min_value

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        # TODO: Write your code here
		if(empty_cell(puzzle) is False): #goal state no empty cell found
			self.ans = copy.deepcopy(puzzle)
			print puzzle
			return self.ans
		
		if(select_variables(self.puzzle) is False):
			#print "start backtrack"
			return False
		else:
			row, col, value_list, number_of_values = select_variables(self.puzzle)
			while(number_of_values > 0):
				num = value_list.popleft()
				number_of_values -= 1
				puzzle[row][col] = num
				
				if(self.solve() is not False):
					return self.ans
				
				puzzle[row][col] = 0
				
		return False
		
    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")

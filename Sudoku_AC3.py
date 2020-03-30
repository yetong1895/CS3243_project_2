import sys
import copy
import time
from collections import deque

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
class Variable:
	def __init__(slef, row, col, domain, count, neighbor):
		self.coordinate = row, col
		self.domain = domain
		self.count = count
		self.neighbor = neighbor #same row/col/subgrid

class Sudoku(object):
	def __init__(self, puzzle):
		# you may add more attributes if you need
		self.puzzle = puzzle # self.puzzle is a list of lists
		self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
		
	def find_empty_pos(self, list):
		for i in range(9):
			for j in range(9):
				if self.puzzle[i][j] == 0:
					return True
		return False
					

	def not_in_col(self, number, col):
		for i in range(9):
			if self.puzzle[i][col] == number:
				return False
		return True
	
	def not_in_row(self, number, row):
		for i in range(9):
			if self.puzzle[row][i] == number:
				return False
		return True
	
	def not_in_subgrid(self, number, row, col):
		row_start = row - row % 3
		col_start = col - col % 3
		
		for i in range(3):
			for j in range(3):
				if self.puzzle[row_start + i][col_start + j] == number:
					return False
		return True
	
	def is_valid(self, number, row, col):
		return self.not_in_col(number, col) and self.not_in_row(number, row) and self.not_in_subgrid(number, row, col)

	def csp(self): 
		variables = deque()
		for i in range(9):
			for j in range(9):
				if(self.puzzle[i][j] == 0): #find a variable
					domain = deque()
					count = 0
					
					#check for possible values
					for num in range(1, 10): 
						if(self.is_valid(num, i, j)):
							domain.append(num)
							count += 1
							
					#check for neighbor
					neighbor = deque()
					#check for same row
					for col in range(9): 
						if((self.puzzle[i][col] == 0) and (col != j)): 
							neighbor.append((i, col))
					
					#check for same column
					for row in range(9): 
						if((self.puzzle[row][j] == 0) and (row != i)):
							neighbor.append((row, j))
					
					#check for same subgrid
					row_start = i - i%3
					col_start = j - j%3
					for s_i in range(3):
						for s_j in range(3):
							if((self.puzzle[row_start + s_i][col_start + s_j] == 0) and (s_i != i) and (s_j != j)):
								neighbor.append((s_i, s_j))
					
					new_variable = Variable(i, j, domain, count, neighbor) #create new variable		
					variables.append(new_variable)
		return variables
	
	def AC3(self, queue = None, removals=None)
	
	def revise(self, x_domain, y_domain) #return true if we remove a value from the domain
		revised = False
		for x in x_domain:
			
		
	
	def find_solution(self):
		
		if self.find_empty_pos(list) is False:
			#no more empty space
			return True
			
		if(self.select_variables() is False): ##############
			return False
		else:
			row, col, value_list, number_of_values = self.select_variables() ###############
			while(number_of_values > 0):
				num = value_list.popleft()
				number_of_values -= 1
				self.puzzle[row][col] = num
				
				if(self.find_solution()):
					return True
					
				self.puzzle[row][col] = 0
		#print('backtrack')
		return False

	def solve(self):
		# TODO: Write your code here
		start = time.time()
		self.find_solution()
		end = time.time()
		print (end - start)
		self.ans = copy.deepcopy(puzzle)
		# self.ans is a list of lists
		return self.ans

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

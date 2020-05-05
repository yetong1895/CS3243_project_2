import sys
import copy
import time
from collections import deque
from Queue import PriorityQueue


# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
class Variable:
	def __init__(self, row, col, domain, count, neighbor):
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

	def lcv(self):
		variables = {}
		for i in range(9):
			for j in range(9):
				if(self.puzzle[i][j] == 0): #find a variable
					domain = []
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
							if((self.puzzle[row_start + s_i][col_start + s_j] == 0) and (row_start + s_i != i) and (col_start + s_j != j)):
								neighbor.append((row_start + s_i, col_start + s_j))
					new_variable = Variable(i, j, domain, count, neighbor) #create new variable
					variables[(i, j)] = new_variable
		return variables

	def select_values(self, variable, variables):
		value_list = PriorityQueue()
		domain = variable.domain
		for i in domain:
			count = 0
			for j in variable.neighbor:
				if(variables[j].domain.count(i) == 1):
					count += 1

			value_list.put((count, j))

		return value_list

	def find_solution(self, variables):

		if self.find_empty_pos(list) is False:
			#no more empty space
			return True
		for key, value in variables.iteritems():
			value_list = self.select_values(value, variables)

			if(self.select_values(value, variables) is False):
				return False
			else:
				while not value_list.empty():
					count, value = value_list.get()
					self.puzzle[key[0]][key[1]] = value

					if(self.find_solution(variables)):
						return True

					self.puzzle[row][col] = 0
		#print('backtrack')
		return False

	def solve(self):
		# TODO: Write your code here
		start = time.time()
		variables = self.lcv()
		self.find_solution(variables)
		end = time.time()
		# print (end - start)
		self.time = end - start
		self.ans = copy.deepcopy(self.puzzle)
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

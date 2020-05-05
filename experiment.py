# Experimental Code
import Sudoku_AC3
import Sudoku_LCV
import Sudoku_MRV
import os
#import matplotlib.pyplot as plt

def readPuzzle(file):
	puzzle = [[0 for i in range(9)] for j in range(9)]
	lines = f.readlines()
	i,j = 0, 0
	for line in lines:
		for number in line:
			if '0' <= number <= '9':
				puzzle[i][j] = int(number)
				j += 1
				if j == 9:
				    i += 1
				    j = 0
	return puzzle


AC_3_timing = []
LCV_timing = []
MRV_timing = []



# read inputs

for filename in os.listdir(os.getcwd() + "/testcases/"):
	with open(os.path.join(os.getcwd() + "/testcases/", filename), 'r') as f:
		# Taken from main
		puzzle = readPuzzle(f)
		# run each algorithm for 5 times and take average
		sudoku_AC3 = Sudoku_AC3.Sudoku(puzzle)
		sudoku_LCV = Sudoku_LCV.Sudoku(puzzle)
		sudoku_MRV = Sudoku_MRV.Sudoku(puzzle)


		time_AC3 = 0
		time_LCV = 0
		time_MRV = 0

		for i in range(5):
			sudoku_AC3.solve()
			print("AC3 time ", sudoku_AC3.time)
			sudoku_LCV.solve()
			print("LCV time ", sudoku_LCV.time)
			sudoku_MRV.solve()
			print("MRV time ", sudoku_MRV.time)

			t_AC3 = sudoku_AC3.time
			t_LCV = sudoku_LCV.time
			t_MRV = sudoku_MRV.time

			time_AC3 += t_AC3
			time_LCV += t_LCV
			time_MRV += t_MRV

		ave_time_AC3 = time_AC3 / 5
		ave_time_LCV = time_LCV / 5
		ave_time_MRV = time_MRV / 5

		AC_3_timing.append(ave_time_AC3)
		LCV_timing.append(ave_time_LCV)
		MRV_timing.append(ave_time_MRV)

# Mean time over all test cases
print("Mean time AC3: ", sum(AC_3_timing) / len(AC_3_timing))
print("Mean time MRV: ", sum(MRV_timing) / len(MRV_timing))
print("Mean time LCV: ", sum(LCV_timing) / len(LCV_timing))

AC3_range = max(AC_3_timing) - min(AC_3_timing)
MRV_range = max(MRV_timing) - min(MRV_timing)
LCV_range = max(LCV_timing) - min(LCV_timing)

width_AC3 = AC3_range / 10
width_MRV = MRV_range / 10
width_LCV = LCV_range / 10


# plt.hist(AC_3_timing, bins=width_AC3)
# plt.hist(LCV_timing, bins=width_LCV)
# plt.hist(MRV_timing, bins=width_MRV)

# plt.show()



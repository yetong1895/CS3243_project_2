# Experimental Code
import Sudoku_AC3
import Sudoku_LCV
import Sudoku_MRV
import CS3243_P2_Base_code
import os
import copy
import matplotlib.pyplot as plt

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
Base_timing = []

AC3_backtrack = []
LCV_backtrack = []
MRV_backtrack = []
Normal_backtrack = []

# read inputs
for filename in os.listdir(os.getcwd() + "/hard_testcases/"):
	with open(os.path.join(os.getcwd() + "/hard_testcases/", filename), 'r') as f:
		# Taken from main
		puzzle = readPuzzle(f)
		time_AC3 = 0
		time_LCV = 0
		time_MRV = 0
		time_Norm = 0

		tot_backtrack_AC3 = 0
		tot_backtrack_LCV = 0
		tot_backtrack_MRV = 0
		tot_backtrack_Norm = 0


		# run each algorithm for 5 times and take average
		for i in range(5):

			sudoku_AC3 = Sudoku_AC3.Sudoku(copy.deepcopy(puzzle))
			sudoku_LCV = Sudoku_LCV.Sudoku(copy.deepcopy(puzzle))
			sudoku_MRV = Sudoku_MRV.Sudoku(copy.deepcopy(puzzle))
			sudoku_Base = CS3243_P2_Base_code.Sudoku(copy.deepcopy(puzzle))

			sudoku_AC3.solve()
			sudoku_MRV.solve()
			sudoku_LCV.solve()
			sudoku_Base.solve()

			t_AC3 = sudoku_AC3.time
			t_LCV = sudoku_LCV.time
			t_MRV = sudoku_MRV.time
			t_base = sudoku_Base.time

			backtrack_AC3 = sudoku_AC3.num_backtrack
			backtrack_LCV = sudoku_LCV.num_backtrack
			backtrack_MRV = sudoku_MRV.num_backtrack
			backtrack_Base = sudoku_Base.num_backtrack

			tot_backtrack_AC3 += backtrack_AC3
			tot_backtrack_LCV += backtrack_LCV
			tot_backtrack_MRV += backtrack_MRV
			tot_backtrack_Norm += backtrack_Base

			time_AC3 += t_AC3
			time_LCV += t_LCV
			time_MRV += t_MRV
			time_Norm += t_base

		ave_time_AC3 = time_AC3 / 5
		ave_time_LCV = time_LCV / 5
		ave_time_MRV = time_MRV / 5
		ave_time_Norm = time_Norm / 5

		ave_backtrack_AC3 = tot_backtrack_AC3 / 5
		ave_backtrack_LCV = tot_backtrack_LCV / 5
		ave_backtrack_MRV = tot_backtrack_MRV / 5
		ave_backtrack_Norm = tot_backtrack_Norm / 5

		print(ave_time_AC3)
		print(ave_time_LCV)
		print(ave_time_MRV)


		AC_3_timing.append(ave_time_AC3)
		LCV_timing.append(ave_time_LCV)
		MRV_timing.append(ave_time_MRV)
		Base_timing.append(ave_time_Norm)

		AC3_backtrack.append(ave_backtrack_AC3)
		LCV_backtrack.append(ave_backtrack_LCV)
		MRV_backtrack.append(ave_backtrack_MRV)
		Normal_backtrack.append(ave_backtrack_Norm)


# Mean time over all test cases
print("Mean time AC3: ", sum(AC_3_timing) / len(AC_3_timing))
print("Mean time MRV: ", sum(MRV_timing) / len(MRV_timing))
print("Mean time LCV: ", sum(LCV_timing) / len(LCV_timing))
print("Mean time Base: ", sum(Base_timing) / len(Base_timing))

print("Average num backtracks AC3: ",  sum(AC3_backtrack) / len(AC3_backtrack))
print("Average num backtracks LCV: ", sum(LCV_backtrack) / len(LCV_backtrack))
print("Average num backtracks MRV: ", sum(MRV_backtrack) / len(MRV_backtrack))
print("Average num backtracks Base: ", sum(Normal_backtrack) / len(Normal_backtrack))

# AC3_range = max(AC_3_timing) - min(AC_3_timing)
# MRV_range = max(MRV_timing) - min(MRV_timing)
# LCV_range = max(LCV_timing) - min(LCV_timing)

# width_AC3 = AC3_range // 10
# width_MRV = MRV_range // 10
# width_LCV = LCV_range // 10

#plt.xlim(0,0.2)
print("Num data AC3: ", sum(i < 0.2 for i in AC_3_timing))
print("Num data LCV: ", sum(i < 0.2 for i in LCV_timing))
print("Num data MRV: ", sum(i < 0.2 for i in MRV_timing))
print("Num data Base: ", sum(i < 0.2 for i in Base_timing))


plt.hist(AC_3_timing, bins='auto', alpha=0.5, label='AC3')
plt.hist(LCV_timing, bins='auto', alpha=0.5, label="LCV")
plt.hist(MRV_timing, bins='auto', alpha =0.5, label='MRV')
plt.hist(Base_timing, bins='auto', alpha =0.5, label='Base')
plt.legend(loc='upper right')
plt.show()
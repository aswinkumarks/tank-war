import random
import sys

class Cell:
	def __init__(self,set_no):
		self.right_wall = False
		self.bottom_wall = False
		self.setId = set_no

	def __str__(self):
		return "Right wall:"+str(self.right_wall)+" Bottom wall:"+str(self.bottom_wall)


class Map:
	def __init__(self, no_rows,no_cols):
		self.curr_row = []
		self.matrix = [[0]*(no_cols*2) for i in range(no_rows*2)]
		self.row_set = {}
		self.set_id = 0
		self.no_rows = no_rows
		self.no_cols = no_cols
		for index in range(no_cols):
			self.row_set[index] = []

	def getUniqueSetNo(self):
		for set_no in self.row_set:
			if len(self.row_set[set_no])==0:
				return set_no
		print(self.row_set)
		print("Error")
		exit(0)

	def genFirstRow(self):
		for index in range(self.no_cols):
			cellSet = self.getUniqueSetNo()
			cell =  Cell(cellSet)
			self.curr_row.append(cell)
			self.row_set[cellSet] = [cell]

	def genNextRow(self):
		for col_no in range(self.no_cols):
			curr_cell = self.curr_row[col_no]
			curr_cell.right_wall = False

			if curr_cell.bottom_wall:
				self.row_set[curr_cell.setId].remove(curr_cell)
				cellSet = self.getUniqueSetNo()
				curr_cell.setId = cellSet
				self.row_set[cellSet].append(curr_cell)

			curr_cell.bottom_wall = False

	def genFinalRow(self):
		for col_no in range(self.no_cols-1):
			curr_cell = self.curr_row[col_no]
			next_cell = self.curr_row[col_no+1]
			curr_cell.bottom_wall = True
			if curr_cell.setId != next_cell.setId:
				curr_cell.right_wall = False
				next_cell_setId = next_cell.setId
				for cell in self.row_set[next_cell_setId]:
					cell.setId = curr_cell.setId

				self.row_set[curr_cell.setId] += self.row_set[next_cell_setId]
				self.row_set[next_cell_setId] = []
			else:
				curr_cell.right_wall = True


		self.curr_row[-1].bottom_wall = True

	def updateRightWall(self):
		for col_no in range(self.no_cols-1):
			curr_cell = self.curr_row[col_no]
			next_cell = self.curr_row[col_no+1]

			if curr_cell.setId == next_cell.setId:
				curr_cell.right_wall = True
				continue

			if bool(random.getrandbits(1)):
				curr_cell.right_wall = True
			else:
				#Union two sets 
				next_cell_setId = next_cell.setId
				for cell in self.row_set[next_cell_setId]:
					cell.setId = curr_cell.setId

				self.row_set[curr_cell.setId] += self.row_set[next_cell_setId]
				self.row_set[next_cell_setId] = []

	def updateBottomWall(self):
		for col_no in range(self.no_cols):
			curr_cell = self.curr_row[col_no]
			if len(self.row_set[curr_cell.setId]) == 1:
				continue

			bottom_wall_possi = False
			for cell in self.row_set[curr_cell.setId]:
				if not cell.bottom_wall and cell != curr_cell:
					bottom_wall_possi = True
					break

			if bottom_wall_possi:
				curr_cell.bottom_wall = bool(random.getrandbits(1))


	def printRow(self,row_no):
		if row_no == 0:
			print(' ___'*self.no_cols)

		print('|',end='')

		for col_no in range(self.no_cols):
			curr_cell = self.curr_row[col_no]

			if curr_cell.right_wall:
				print('   |',end='')
				# print('%3d|'%(curr_cell.setId),end='')
			else:
				print('    ',end='')
				# print('%3d '%(curr_cell.setId),end='')

		print('\b|')

		for col_no in range(self.no_cols):
			curr_cell = self.curr_row[col_no]
			if curr_cell.bottom_wall:
				print(' ___',end='')
			else:
				print('    ',end='')
		print("")

	def update_matrix(self,row_no):
		row_no = row_no * 2
		for index, cell in enumerate(self.curr_row):
			if cell.right_wall:
				self.matrix[row_no][index*2+1] = 1
				self.matrix[row_no + 1][index*2+1] = 1
			if cell.bottom_wall:
				self.matrix[row_no+1][index*2] = 1
				self.matrix[row_no+1][index*2+1] = 1

	def generate(self):
		for row_no in range(self.no_rows):
			if row_no == 0:
				self.genFirstRow()
			else:
				self.genNextRow()

			if row_no == self.no_rows-1:
				self.genFinalRow()
				# self.printRow(row_no)
				self.update_matrix(row_no)
				break

			self.updateRightWall()
			self.updateBottomWall()
			# self.printRow(row_no)
			self.update_matrix(row_no)

		return self.matrix

if len(sys.argv) > 2:
	maze = Map(int(sys.argv[1]),int(sys.argv[2]))
else:
	maze = Map(7,7)
maze.generate()
			
		
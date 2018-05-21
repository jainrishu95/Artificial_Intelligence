import sys, time, copy, random, math, timeit
queue = []

class State:
	'''
	matrix = list within list of matrix
	lizards_placed = list of positions of lizards placed
	number_of_lizards = num of lizards to be placed
	next_tree = position of next tree in a row
	'''
	def __init__(self, matrix, lizards_placed, number_of_lizards):
		if lizards_placed == None:
			if number_of_lizards == None:
				self.matrix = matrix.matrix
				self.lizards_placed = matrix.lizards_placed
				self.number_of_lizards = matrix.number_of_lizards
				self.search_position = 0
			else:	
				self.matrix = matrix
				self.lizards_placed = []
				self.number_of_lizards = number_of_lizards
				self.search_position = 0			

#make avoidable places for next iteration
def placeQueen(mat, row, j, size):
	#print(mat.matrix)
	mat.matrix[row][j] = 1
	#determine avoidable row's position's for next iteration in right direction of queen 
	for ix in range(j+1, size):
		if mat.matrix[row][ix] == 2:
			break
		else:
			mat.matrix[row][ix] = -1
	#determine avoidable row's position's for next iteration in left direction of queen 
	for ix in range(j-1,-1,-1):
		if mat.matrix[row][ix] == 2:
			break
		else:
			mat.matrix[row][ix] = -1
	#determine avoidable colum	ns's position's for next iteration in the bottom direction
	for ix in range(row+1, size):
		if mat.matrix[ix][j] == 2:
			break
		else:
			mat.matrix[ix][j] = -1
	#determine avoidable columns's position's for next iteration in the above position 
	for ix in range(row-1,-1,-1):
		if mat.matrix[ix][j] == 2:
			break
		else:
			mat.matrix[ix][j] = -1
	#determine avoidable columns's position's for next iteration in both above digoanal directions 
	flag1 = False
	flag2 = False
	for ix in range(0, row):
		for iy in range(0, size):
			if abs(row-j == ix-iy):
				if flag1 != True:
					if mat.matrix[ix][iy] == 2:
						flag1 = True
					elif mat.matrix[ix][iy] == 1:
						continue
					else:
						mat.matrix[ix][iy] = -1
			elif row+j==ix+iy:
				if flag2 != True:
					if mat.matrix[ix][iy] == 2:
						flag2 = True
					elif mat.matrix[ix][iy] == 1:
						continue
					else:
						mat.matrix[ix][iy] = -1					 		
	
	#determine avoidable columns's position's for next iteration in both below digoanal directions 
	flag1 = False
	flag2 = False
	for ix in range(row+1, size):
		for iy in range(0, size):
			if abs(row-j == ix-iy):
				if flag1 != True:
					if mat.matrix[ix][iy] == 2:
						flag1 = True
					else:
						mat.matrix[ix][iy] = -1
			elif row+j==ix+iy:
				if flag2 != True:
					if mat.matrix[ix][iy] == 2:
						flag2 = True
					else:
						mat.matrix[ix][iy] = -1	
	'''
	for i in range(size):
		for j in range(size):
			print(mat.matrix[i][j], end =' ')		
		print()
	'''		 		
	return mat

def initialize():
    file = open('input.txt','r').read().split('\n')
    if file[-1]=='' :
        file = file[:-1]
    #extracted size, lizards, algotye
    #print(file[1])
    size = int(file[1])
    lizards = int(file[2])
    algotype = file[0]
    matrix = []
    count = 0
    #computing matrix from given input and storing in a list within list
    for ix in range(3,3+size):
        row = file[ix].strip()
        temp = []
        for every in row:
        	if int(every) == 2:
        		count+=1
        	temp.append(int(every))
        matrix.append(temp)
    matrix = State(matrix, None, lizards)
    return algotype, size, matrix, count

def display(mat, size):
	file = open('output.txt', 'w+')
	file.write('OK\n')
	for i in range(size):
		for j in range(size):
			if mat.matrix[i][j] == -1:
				file.write(str(0) + '')
			else:
				file.write(str(mat.matrix[i][j]) + '')
		file.write('\n')
	file.close()

def generateobstacle(mat, row, col, size):
	for j in range(col, size):
		if mat.matrix[row][j] == 2:			
			return j
	return -1

def createchilds(matrix, posx, j, size):
	global queue
	flag = False
	if j > size:
		matrix.search_position = 0
		j = 0
	while j < size:
		if matrix.matrix[posx][j] == 0:
			next_tree = generateobstacle(matrix, posx, j, size)
			if next_tree == -1:
				next_tree = size
			#print(next_tree)
			flag = True
			#import copy
			#child = State(matrix, None, None)
			child = copy.deepcopy(matrix)
			child.lizards_placed.append((posx, j))
			child.number_of_lizards -= 1
			#print(matrix.matrix, child.matrix)
			child = placeQueen(child, posx, j, size)
			child.search_position = next_tree + 1
			queue.append(child)
			#print(child.matrix)
			j += 1
		elif matrix.matrix[posx][j] == 2: #and generateobstacle(matrix, posx, matrix.search_position, size)!=j: 
			if flag == False:
				j+=1
			else:
				matrix.search_position = j+1
				break
		else:
			j += 1	
	#print(queue)
	return flag	

def makechild(matrix, size):
	if len(matrix.lizards_placed) == 0:
		posx = 0
	else:
		posx = matrix.lizards_placed[-1][0]
		#posy = matrix.lizards_placed[-1][1]
	j = matrix.search_position
	times = 0
	while True:
		#print('make child')
		if createchilds(matrix, posx, j, size) == False:
			times += 1
			if posx + times == size:
				break
			createchilds(matrix, posx + times, 0, size)
		else:
			break

def implementBFS(size):
#temp = State(main_matrix.matrix, main_matrix.lizards_placed, main_matrix.number_of_lizards)
	global queue
	flag = False
	while len(queue)>0:
		matrix = queue.pop(0)
		#success
		if matrix.number_of_lizards == 0:
			display(matrix, size)
			flag = True
			break
		#Expland children
		else:
			makechild(matrix, size)
	#false case
	if flag==False:
		file = open('output.txt', 'w')
		file.write('FAIL\n')
		file.close()

def implementDFS(size):
#temp = State(main_matrix.matrix, main_matrix.lizards_placed, main_matrix.number_of_lizards)
	global queue
	flag = False
	while len(queue)>0:
		matrix = queue.pop()
		#success
		if matrix.number_of_lizards == 0:
			display(matrix, size)
			flag = True
			break
		#Expland children
		else:
			makechild(matrix, size)
	#false case
	if flag==False:
		file = open('output.txt', 'w+')
		file.write('FAIL\n')
		file.close()
 
def generateRandomPosition(matrix, size):
	#import random
	x = random.randint(0,size-1)
	y = random.randint(0,size-1)
	if matrix.matrix[x][y] == 1 or matrix.matrix[x][y] == 2:
		matrix = generateRandomPosition(matrix, size)
	else:
		matrix.matrix[x][y] = 1
	return matrix

def countlizards(matrix):
	for ix in range(0, size):
		for iy in range(0, size):
			if matrix.matrix[ix][iy] == 1:
				matrix.lizards_placed.append((ix, iy))
	return matrix

def countconflicts(mat):
	conflicts = 0
	for i in mat.lizards_placed:
		x = i[0]
		y = i[1]
		#print(x, y, end = '\n')
		#determine avoidable row's position's for next iteration in right direction of queen 
		for ix in range(y+1, size):
			if mat.matrix[x][ix] == 1:
				conflicts +=1
				break
			elif mat.matrix[x][ix] == 2:
				break
			elif mat.matrix[x][ix] == -1:
				continue
			else:
				mat.matrix[x][ix] = -1
		#print(mat.matrix)
		#determine avoidable row's position's for next iteration in left direction of queen 
		for ix in range(y-1,-1,-1):
			if mat.matrix[x][ix] == 2:
				break
			elif mat.matrix[x][ix] == 1:
				conflicts += 1
				break
			elif mat.matrix[x][ix] == -1:
				continue
			else:
				mat.matrix[x][ix] = -1
		#print(mat.matrix)
		#determine avoidable colum	ns's position's for next iteration in the bottom direction
		for ix in range(x+1, size):
			if mat.matrix[ix][y] == 1:
				conflicts +=1
				break
			elif mat.matrix[ix][y] == 2:
				break
			elif mat.matrix[ix][y] == -1:
				continue
			else:
				mat.matrix[ix][y] = -1
		#print(mat.matrix)
		#determine avoidable columns's position's for next iteration in the above position 
		for ix in range(x-1, -1, -1):
			if mat.matrix[ix][y] == 1:
				conflicts +=1
				break
			elif mat.matrix[ix][y] == 2:
				break
			elif mat.matrix[ix][y] == -1:
				continue
			else:
				mat.matrix[ix][y] = -1
		#print(mat.matrix)
		#determine avoidable columns's position's for next iteration in both above digoanal directions 
		flag1 = False
		flag2 = False
		for ix in range(0, x):
			for iy in range(0, size):
				if abs(x-y == ix-iy):
					if flag1 != True:
						if mat.matrix[ix][iy] == 2:
							flag1 = True
						elif mat.matrix[ix][iy] == 1:
							conflicts+=1
							break
						elif mat.matrix[ix][iy] == -1:
							continue
						else:
							mat.matrix[ix][iy] = -1
				elif x+y == ix+iy:
					if flag2 != True:
						if mat.matrix[ix][iy] == 2:
							flag2 = True
						elif mat.matrix[ix][iy] == 1:
							conflicts += 1
							break
						elif mat.matrix[ix][iy] == -1:
							continue
						else:
							mat.matrix[ix][iy] = -1					 		
		#print(mat.matrix)
		#determine avoidable columns's position's for next iteration in both below digoanal directions 
		flag1 = False
		flag2 = False
		for ix in range(x+1, size):
			for iy in range(0, size):
				if abs(x-y == ix-iy):
					if flag1 != True:
						if mat.matrix[ix][iy] == 2:
							flag1 = True
						elif mat.matrix[ix][iy] == 1:
							conflicts+=1
							break
						elif mat.matrix[ix][iy] == -1:
							continue
						else:
							mat.matrix[ix][iy] = -1
				elif x+y == ix+iy:
					if flag2 != True:
						if mat.matrix[ix][iy] == 2:
							flag2 = True
						elif mat.matrix[ix][iy] == 1:
							conflicts += 1
							break
						elif mat.matrix[ix][iy] == -1:
							continue
						else:
							mat.matrix[ix][iy] = -1
		'''
		for i in range(size):
			for j in range(size):
				print(mat.matrix[i][j], end =' ')		
			print()
		'''
		#print(mat.matrix)		 		
	return conflicts, mat

def generateoneRandomPosition(matrix, size, removed):
	x = random.randint(0,size-1)
	y = random.randint(0,size-1)
	if (x, y) in matrix.lizards_placed or (x,y) == removed or matrix.matrix[x][y] == 2:
		matrix = generateoneRandomPosition(matrix, size, removed)
	else:
		matrix.matrix[x][y] = 1
	return matrix

def printmatrix(matrix, size):
	for ix in range(size):
		for iy in range(size):
			print(matrix.matrix[ix][iy], end= ' ')
		print()

def creatematrix(matrix):
	for ix in matrix.lizards_placed:
		matrix.matrix[ix[0]][ix[1]] = 1
	return matrix

def sacountlizards(matrix):
	for ix in range(size):
		for iy in range(size):
			if matrix.matrix[ix][iy] == 1:
				if (ix, iy) in matrix.lizards_placed:
					continue
				else: 
					matrix.lizards_placed.append((ix, iy))
	matrix.lizards_placed = sorted(matrix.lizards_placed, key = lambda entry:(entry[0], entry[1]))
	return matrix

def calculateSimulated(matrix, input_matrix, conflicts, size, temp, counter):
	flag = False
	start = time.time()
	while counter<100000 and time.time() - start < 60:
		counter += 1	
		if conflicts>0:
			child = copy.deepcopy(input_matrix)
			queenpos = random.choice(matrix.lizards_placed)
			lst = copy.deepcopy(matrix.lizards_placed)
			lst.remove(queenpos)
			child.lizards_placed = lst
			child = generateoneRandomPosition(child, size, queenpos)
			child = creatematrix(child)
			#printmatrix(child, size)
			child = sacountlizards(child)
			#print(matrix.lizards_placed, child.lizards_placed)
			childconflicts, child = countconflicts(child)
			delta = childconflicts - conflicts
			rand = random.random()
			probab = math.exp(-delta/temp)
			#printmatrix(matrix, size)
			#printmatrix(child, size)
			if delta <= 0:
				#print('1')
				matrix = copy.deepcopy(child)
				conflicts = copy.deepcopy(childconflicts)
				temp = 1/math.log(counter)
			elif rand < probab and delta > 0:
				#accept case with propility
				#print('2')
				matrix = copy.deepcopy(child)
				conflicts = copy.deepcopy(childconflicts)
		#parent has 0 conflicts 
		else:
			#print('Success')
			display(matrix, size)
			flag = True
			break
	#temp == 0
	if flag == False:
		file = open('output.txt', 'w')
		file.write('FAIL\n')
		file.close()

def prepareSimulated(count, size):
	#import copy
	global queue
	matrix = queue.pop()
	input_matrix = copy.deepcopy(matrix)
	if count == 0:
		if matrix.number_of_lizards>size:
			file = open('output.txt', 'w')
			file.write('FAIL\n')
			file.close()
		else:
			for ix in range(0,matrix.number_of_lizards):
				matrix = generateRandomPosition(matrix, size)
			matrix = countlizards(matrix)			
			conflicts, matrix = countconflicts(matrix)
			calculateSimulated(matrix, input_matrix, conflicts, size, 1, 10)
	else:
		for ix in range(0, matrix.number_of_lizards):
			matrix = generateRandomPosition(matrix, size)
		matrix = countlizards(matrix)			
		conflicts, matrix = countconflicts(matrix)
		calculateSimulated(matrix, input_matrix, conflicts, size, 1, 10)

if __name__ == '__main__':
	#start = timeit.default_timer()
	#Extract algotype, size of array, no of lizards, input matrix
	algotype, size, main_matrix, counttrees = initialize()
	if(algotype == 'BFS'):
		queue.append(main_matrix)
		implementBFS(size)
		#stop = timeit.default_timer()
		#print(stop - start) 
	elif algotype == 'DFS':
		queue.append(main_matrix)
		implementDFS(size)
	else:
		queue.append(main_matrix)
		prepareSimulated(counttrees, size)
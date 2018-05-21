import string, copy, timeit
Index = dict(zip(string.ascii_uppercase, range(1,27)))
startalpha = -9999
startbeta = 9999
maxmoves = 0
prunecount = 0
counter = 0
class State:
	def __init__(self, matrix):
		self.matrix = matrix
		self.xvalue = 0
		self.yvalue = 0

def checkmatrix(state, size):
	flag = False
	for ix in range(size):
		for iy in range(size):
			try:
				if state.matrix[int(iy)]:
					flag = True
					break
			except:
				continue
	return flag

def initialize():
	inp = open('input.txt', 'r').read().split()
	size = int(inp[0])
	num_of_fruits = int(inp[1])
	time = float(inp[2])
	inp = inp[3:]
	inp = [[each if each=='*' else int(each) for each in every] for every in inp]
	s = State(inp)
	return size, num_of_fruits, time, inp, s
 
def makegroups(state, ix, iy, lst, size):
	lst.append((ix,iy))
	temp = state.matrix[ix][iy]
	state.matrix[ix][iy] = '*'
	if iy+1 < size and state.matrix[ix][iy+1] == temp:
		makegroups(state, ix, iy+1, lst, size)
	if ix+1 < size and state.matrix[ix+1][iy] == temp:
		makegroups(state, ix+1, iy, lst, size)
	if iy-1 >= 0 and state.matrix[ix][iy-1] == temp:
		makegroups(state, ix, iy-1, lst, size)
	if ix-1 >= 0 and state.matrix[ix-1][iy] == temp:
		makegroups(state, ix-1, iy, lst, size)

def generatechilds(state, size):
	allchilds = list()
	for ix in range(size):
		for iy in range(size):
			if type(state.matrix[ix][iy]) == str:
				continue
			else:
				lst = list()
				makegroups(state, ix, iy, lst, size)
				allchilds.append(lst)
	return allchilds

def printmatrix(state, size):
	for ix in range(size):
		for iy in range(size):
			print(state.matrix[ix][iy], end=' ')
		print()

def makechildstates(state, allchilds, size, flag):
	child = list()
	for everychild in allchilds:
		temp = copy.deepcopy(state)
		for iy in range(size-1, -1, -1):
			pointer = size-1
			for ix in range(size-1, -1, -1):
				if (ix, iy) in everychild:
					continue
				else:
					temp.matrix[pointer][iy] = state.matrix[ix][iy]
					pointer -= 1
			while(pointer>=0):
				temp.matrix[pointer][iy] = '*'
				pointer -= 1
		if flag == True:
			temp.xvalue += len(everychild)**2
		else:
			temp.yvalue += len(everychild)**2 
		child.append(temp)
	return child

def maxValue(state, size, alpha, beta, depth):
	global maxmoves, counter, prunecount
	counter += 1
	if depth == maxdepth or checkmatrix(state, size) == False:
		return state.xvalue - state.yvalue
	childs = generatechilds(copy.deepcopy(state), size)
	childs = sorted(childs, key = lambda x:len(x), reverse = True)
	childs = makechildstates(state, childs, size, True)
	for everychild in childs:
		tempalpha = max(alpha, minValue(everychild, size, alpha, beta, depth+1))
		if depth == 0:
			if tempalpha != alpha:
				maxmoves = copy.deepcopy(everychild)
		alpha = tempalpha 
		if alpha >= beta:
			prunecount+=1
			return beta
	return alpha 

def minValue(state, size, alpha, beta, depth):
	global counter, prunecount
	counter += 1
	if depth == maxdepth or checkmatrix(state, size)== False:
		return state.xvalue - state.yvalue
	childs = generatechilds(copy.deepcopy(state), size)
	childs = sorted(childs, key = lambda x:len(x), reverse = True)
	childs = makechildstates(state, childs, size, False)
	for everychild in childs:
		beta = min(beta, maxValue(everychild, size, alpha, beta, depth+1))
		if beta <= alpha:
			prunecount+=1
			return alpha
	return beta

def display(state, position, size):
	file = open('output.txt', 'w+')
	file.write(str(position[0]))
	file.write(str(position[1]))
	file.write('\n')
	for i in range(size):
		for j in range(size):
			if type(state.matrix[i][j]) == str:
				file.write(state.matrix[i][j])
			else:
				file.write(str(state.matrix[i][j]))
		file.write('\n')
	file.close()

if __name__ == '__main__':
	#start = timeit.default_timer()
	size, num_of_fruits, time, inputmatrix, state = initialize()
	childs = generatechilds(copy.deepcopy(state), size)
	childs = len(childs)
	if time <= 5:
		if childs <= size :
			maxdepth = childs
		elif childs/size <= 2:
			maxdepth = 2
		else:
			maxdepth = 1
		'''
			childs = generatechilds(copy.deepcopy(state), size)
			childs = sorted(childs, key = lambda x:len(x), reverse = True)
			childs = makechildstates(state, childs, size, False)
			childs = childs[0]
			flag = False
			for i in range(size-1, -1, -1):
				for j in range(size-1, -1, -1):
					if flag == False and childs.matrix[i][j] != state.matrix[i][j]:
						flag = True
						pos = (i+1, j+1)
						break
				if flag == True:
					break
			position = [key for key, value in Index.items() if value == pos[1]][0]
			position = (position, pos[0])
			display(childs, position, size)
		'''
	else:	
		if childs <= size :
			maxdepth = childs
		elif childs/size <= 2:
			maxdepth = 4
		elif childs/size <= 3:
			maxdepth = 3
		else:
			maxdepth = 2
	#print(maxdepth, size, childs, int(childs/size))
	value = maxValue(copy.deepcopy(state), size, startalpha, startbeta, 0)
	flag = False
	for i in range(size-1, -1, -1):
		for j in range(size-1, -1, -1):
			if flag == False and maxmoves.matrix[i][j] != state.matrix[i][j]:
				flag = True
				pos = (i+1, j+1)
				break
		if flag == True:
			break
	position = [key for key, value in Index.items() if value == pos[1]][0]
	position = (position, pos[0])
	display(maxmoves, position, size)
	#end = timeit.default_timer()
	#print(counter, prunecount, end - start)


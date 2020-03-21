import node
from enum import IntEnum
#import pandas
#import copy

class Action(IntEnum):
	ADVANCE = 1
	U_TURN = 2
	TURN_RIGHT = 3
	TURN_LEFT = 4
	HALT = 5
	STOP = 6

class Maze:
	def __init__(self, filepath):
		'''
		raw_data -> list, store the data that read from the file
		nodes -> list, list of all the nodes in the maze
		nd_dic -> dictionary, 
				key: node
				value: list, Successors(0 for no node at the direction)
					Successors in order [North, South, West, East]
		distance_dic -> dictionary,
				key: set, (node1, node2)
				value: distance between node1 and node2
		'''
		self.filepath = filepath
		#self.raw_data = pandas.read_csv(filepath).values
		#time for simple case = 0.021767854690551758
		self.raw_data = []
		self.readfile()
		#self.raw_data.append([0]*9)
		#time for simple case = 0.0006518363952636719

		self.nodes = {}	#nodes
		self.nd_dic = {}	#neighbors

		self.distance_dic = {}	#distance
		self.update()

		self.deadend = [i for i in self.nodes if self.nodes[i].isEndPoint()]

		self.manhattan = {1:(0,0)}
		#when need to calculate the manhattan distance
		#add the following line in the code
		self.update_manhattan()

	def update(self):
		for i in self.raw_data:
			j = node.Node(i)
			#self.nodes.append(j.getIndex())
			#self.nodes.append(j)
			self.nodes[j.index] = j
			self.nd_dic[j.index] = j.Successors
			for k in j.Successors:
				if k != 0:
					self.distance_dic[(j.index, k)] = j.getDistance(k) if j.getDistance(k) != 0 else 1
				else:
					pass
					#self.distance_dic[(j.getIndex(), 0)] = float('inf')
					#self.distance_dic[(j.getIndex(), k)] = j.getDistance(k) if j.getDistance(k) != 0 else 1

	def update_manhattan(self):
		remain = [i for i in self.nodes]
		visited = [1]
		remain.remove(1)
		while len(remain) != 0:
			for i in visited:
				x = self.manhattan[i][0]
				y = self.manhattan[i][1]
				for j in range(4):
					k = self.nd_dic[i][j]
					if j == 0 and k in remain:
						self.manhattan[k] = (x, y + self.distance_dic[(i, k)])
						remain.remove(k)
						visited.append(k)
					elif j == 1 and k in remain:
						self.manhattan[k] = (x, y - self.distance_dic[(i, k)])
						remain.remove(k)
						visited.append(k)
					elif j == 2 and k in remain:
						self.manhattan[k] = (x + self.distance_dic[(i, k)], y)
						remain.remove(k)
						visited.append(k)
					elif j == 3 and k in remain:
						self.manhattan[k] = (x - self.distance_dic[(i, k)], y)
						remain.remove(k)
						visited.append(k)
				visited.remove(i)

	def getStartPoint(self):
		if len(self.nodes) < 2:
			print ('Error: the start point is not included.')
			return 0
		return 1
		#return self.nodes[1]

	def readfile(self):
		with open(self.filepath, 'r') as r:
			l = r.read().split()
		for i in l[1:]:
			k = []
			i1 = i.split(',')
			for j in i1:
				try:
					k.append(int(j))
				except:
					k.append(0)
			self.raw_data.append(k)

	def BFS(self, startpoint):	#ALGORITHM FOR GAME1(RETURN THE ORDER OF DEADEND AND ALL THE NODES THAT IT WILL PASS)
		'''
		total path for game1 (all the nodes in path)
		'''
		total_path = []
		order = []
		#dead = copy.deepcopy(self.deadend)
		#while len(order) == len(self.deadend):
		path = {i:[] for i in self.deadend}
		cp = {i:0 for i in self.deadend}
		while len(order) != len(self.deadend):
			for i in cp:
				path[i], distance = self.BFS_shortest_path(startpoint, i)
				cp[i] = (abs(self.manhattan[i][0]) + abs(self.manhattan[i][1]))/(len(path) * 2 + distance)
			startpoint = max(cp, key = cp.get)
			total_path += path[startpoint][1:]
			order.append(startpoint)
			cp.pop(startpoint)
			path.pop(startpoint)
		return order, [1] + total_path

	def BFS_shortest_path(self, nd_from, nd_to):	#GET THE NODES ALONG THE SHORTEST PATH BETWEEN TWO NODES
		prev = {nd_from:1}
		#prev -> keys::nodes
		#	-> values::distance from the node to the current layer
		dd = {i:self.nd_dic[i][::] for i in self.nd_dic}
		#dd = copy.deepcopy(self.nd_dic)
		distance = 0
		while nd_to not in prev.keys():
			k = [i for i in prev.keys()]
			for keys in k:
				neighbor = dd[keys][::]
				for i in neighbor:
					if i == 0:
						dd[keys].remove(i)
					else:
						if self.distance_dic[(keys, i)] == prev[keys]:
							prev[i] = 1
							self.nodes[i].information = self.nodes[keys].information[::] + [keys]
							dd[keys].remove(i)
				prev[keys] += 1
				if dd[keys] == []:
					prev.pop(keys)
			distance += 1
		nd_path = self.nodes[nd_to].information[::] + [nd_to]
		for i in self.nodes.keys():
			self.nodes[i].clearInformation()
		return nd_path, distance

	def getAction(self, car_dir, nd_from, nd_to):	#GET THE DIRECTION
		i = self.nd_dic[nd_from].index(nd_to)
		if car_dir == 1:	#North
			if i == 0:	#North
				action = Action.ADVANCE
				next_car_dir = node.Direction.North
			elif i == 1:	#South
				action = Action.U_TURN
				next_car_dir = node.Direction.South
			elif i == 2:	#West
				action = Action.TURN_LEFT
				next_car_dir = node.Direction.West
			elif i == 3:	#East
				action = Action.TURN_RIGHT
				next_car_dir = node.Direction.East
		elif car_dir == 2:	#South
			if i == 0:	#North
				action = Action.U_TURN
				next_car_dir = node.Direction.North
			elif i == 1:	#South
				action = Action.ADVANCE
				next_car_dir = node.Direction.South
			elif i == 2:	#West
				action = Action.TURN_RIGHT
				next_car_dir = node.Direction.West
			elif i == 3:	#East
				action = Action.TURN_LEFT
				next_car_dir = node.Direction.East
		elif car_dir == 3:	#West
			if i == 0:	#North
				action = Action.TURN_RIGHT
				next_car_dir = node.Direction.North
			elif i == 1:	#South
				action = Action.TURN_LEFT
				next_car_dir = node.Direction.South
			elif i == 2:	#West
				action = Action.ADVANCE
				next_car_dir = node.Direction.West
			elif i == 3:	#East
				action = Action.U_TURN
				next_car_dir = node.Direction.East
		elif car_dir == 4:	#East
			if i == 0:	#North
				action = Action.TURN_LEFT
				next_car_dir = node.Direction.North
			elif i == 1:	#South
				action = Action.TURN_RIGHT
				next_car_dir = node.Direction.South
			elif i == 2:	#West
				action = Action.U_TURN
				next_car_dir = node.Direction.West
			elif i == 3:	#East
				action = Action.ADVANCE
				next_car_dir = node.Direction.East

		return next_car_dir, action

	def strategy_1(self, car_dir = node.Direction.South, startpoint = 1):	#GET ACTIONLIST FOR GAME1
		deadend_order, total_path = self.BFS(startpoint)
		self.deadend = deadend_order[::]
		act_list = []
		for i in range(len(total_path) - 1):
			car_dir, act = self.getAction(car_dir, total_path[i], total_path[i+1])
			if act == 2:
				act_list.append(Action.HALT)
				act_list.append(act)
			else:
				act_list.append(act)
		return act_list + [Action.HALT, Action.U_TURN, Action.STOP], deadend_order, total_path
		#return act_list + [Action.U_TURN, Action.STOP], deadend_order, total_path

	def sub_strategy(self, car_dir, nd_from, nd_to):	#GET ACTIONLIST BETWEEN TWO NODES
		total_path, dis = self.BFS_shortest_path(nd_from, nd_to)
		act_list = []
		for i in range(len(total_path) - 1):
			car_dir, act = self.getAction(car_dir, total_path[i], total_path[i+1])
			act_list.append(act)
		return car_dir, act_list + [Action.HALT], total_path
		#return car_dir, act_list, total_path

	def strategy_2(self, nd_list, car_dir = node.Direction.South, startpoint = 1):	#GET ACTIONLIST FOR GAME2
		total_path = []
		if nd_list[0] != startpoint:
			nd_list.insert(0,startpoint)
		act_list = []
		for i in range(len(nd_list) - 1):
			car_dir, act, sub_path = self.sub_strategy(car_dir, nd_list[i], nd_list[i+1])
			act_list = act_list + act
			total_path  = total_path + sub_path
		return act_list + [Action.U_TURN, Action.STOP], total_path



from enum import IntEnum

class Direction(IntEnum):
	North = 1
	South = 2
	West = 3
	East = 4

class Node:
	def __init__(self, raw = []):
		self.raw = raw
		if len(self.raw) == 9:
			self.index = int(self.raw[0])
			self.Successors = []
			self.raw_distance = []
			for i in self.raw[1:5]:
				try:
					self.Successors.append(int(i))
				except:
					self.Successors.append(0)
			for i in self.raw[5:]:
				try:
					self.raw_distance.append(int(i))
				except:
					self.raw_distance.append(0)

		#self.winformation = []
		#self.wclearInformation()

		self.information = []
		self.clearInformation()

	def __bool__(self):
		'''
		return whether the input list is a node
		'''
		if len(self.raw) == 9:
			return True
		return False

	def getDistance(self, other):
		'''
		return the distance between self, other
		'''
		if isinstance(other, int):
			return self.raw_distance[self.Successors.index(other)]

	def isEndPoint(self):
		count = 0
		for i in self.Successors:
			if i != 0:
				count += 1
		if (self.index != 1 or self.index != 0) and count == 1:
			return True
		return False

	def clearInformation(self):
		self.information = []

	'''def wclearInformation(self):
		if self.index == 0:
			self.winformation = [float('inf'), [], False, self.index]
		else:
			self.winformation = [float('inf'), [], True, self.index]'''

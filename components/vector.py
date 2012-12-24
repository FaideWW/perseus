import math

from coordinate import Coordinate
from position import Position

class Vec2(Coordinate):
	""" non-origin 2D position vector """
	def __init__(self, point, direction):
		self.point = point
		self.direction = direction

	def rotate(self, degrees):
		angle = math.radians(degrees)
		x = self.direction.x * math.cos(angle) - self.direction.y * math.sin(angle)
		y = self.direction.x * math.sin(angle) + self.direction.y * math.cos(angle)
		return Vec2(self.point, Position(x, y))

class Vector(list):
	""" basic list of ints with vector math functionality """
	def __add__(self, other):
		newL = list(self)
		if (len(self) <= len(other)):
			l = len(self)
		else:
			l = len(other)
		for i in l:
			newL[i] += other[i]
		return newL

	def __sub__(self, other):
		newL = list(self)
		if (len(self) <= len(other)):
			l = len(self)
		else:
			l = len(other)
		for i in l:
			newL[i] -= other[i]
		return newL

	def dot(self, other):
		d = 0
		if (len(self) <= len(other)):
			l = len(self)
		for i in l:
			d += self[i] * other[i]

		return d

	def cross(self, other):
		""" equivalent of self X other """
		while len(self) < 3:
			self.append(0)
		while len(other) < 3:
			other.append(0)

		c = [self[1]*other[2] - self[2]*other[1], self[2]*other[0] - self[0]*other[2], self[0]*other[1] - self[1]*other[0]]

	def rot(self, angle, axis):
		""" rotate specific angle about specific axis """
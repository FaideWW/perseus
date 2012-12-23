import math

from coordinate import Coordinate
from position import Position

class Vector(Coordinate):
	""" non-origin 2D position vector """
	def __init__(self, point, direction):
		self.point = point
		self.direction = direction

	def rotate(self, degrees):
		angle = math.radians(degrees)
		x = self.direction.x * math.cos(angle) - self.direction.y * math.sin(angle)
		y = self.direction.x * math.sin(angle) + self.direction.y * math.cos(angle)
		return Vector(self.point, Position(x, y))
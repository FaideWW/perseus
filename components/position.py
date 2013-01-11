import math

from coordinate import Coordinate


class Position(Coordinate):
	def add(self, x, y, z=0):
		return super(Position, self).add(x, y, z)

	def set(self, x, y, z=0):
		return super(Position, self).set(x, y, z)

	def scale(self, sX, sY, sZ=1):
		return super(Position, self).scale(sX, sY, sZ)

	def distTo(self, pos):
		return (self - pos).mag()

	def dirTo(self, pos):
		return (self - pos).normalize()


class Ray(Coordinate):
 	""" non-origin 2D position vector """
 	def __init__(self, point, direction):
 		self.point = point
 		self.direction = direction
 	def rotate(self, degrees):
 		angle = math.radians(degrees)
 		x = self.direction.x * math.cos(angle) - self.direction.y * math.sin(angle)
 		y = self.direction.x * math.sin(angle) + self.direction.y * math.cos(angle)
 		return Ray(self.point, Position([x, y]))

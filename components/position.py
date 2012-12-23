from coordinate import Coordinate


class Position(Coordinate):
	def __init__(self, x, y, z=0):
		self.x = x
		self.y = y
		self.z = z
	""" Position coordinates.  The only difference here is the z value is optional. """
	def add(self, x, y, z=0):
		return super(Position, self).add(x, y, z)

	def set(self, x, y, z=0):
		return super(Position, self).set(x, y, z)

	def scale(self, sX, sY, sZ=1):
		return super(Position, self).scale(sX, sY, sZ)
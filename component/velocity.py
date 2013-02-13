from coordinate import Coordinate

class Velocity(Coordinate):
	""" Not actually a true Coordinate; only two values are used (z is ignored) """

	

	def add(self, x, y, z=0):
		return super(Velocity, self).add(x, y, 0)

	def set(self, x, y, z=0):
		return super(Velocity, self).set(x, y, 0)

	def scale(self, sX, sY, sZ=0):
		return super(Velocity, self).scale(sX, sY, 0)
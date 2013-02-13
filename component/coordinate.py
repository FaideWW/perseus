from vector import Vector

class Coordinate(Vector):
	"""Base class for a triplet of integer values"""


	def add(self, x, y, z):
		""" change position relative to current position """
		self.x += x
		self.y += y
		self.z += z
		return self

	def set(self, x, y, z):
		""" set position absolutely on world space """
		self.x = x
		self.y = y
		self.z = z
		return self

	def scale(self, sX, sY, sZ):
		""" scale position relative to the origin """
		self.x *= sX
		self.y *= sY
		self.z *= sZ
		return self

	""" Operator definition """
	
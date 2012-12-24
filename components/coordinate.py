class Coordinate(object):
	"""Base class for a triplet of integer values"""
	
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

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

	def __add__(self, coor):
		return Coordinate(self.x + coor.x, self.y + coor.y, self.z + coor.z)

	def __sub__(self, coor):
		return Coordinate(self.x - coor.x, self.y - coor.y, self.z - coor.z)

	def __mul__(self, coor):
		return Coordinate(self.x * coor.x, self.y * coor.y, self.z * coor.z)

	def __div__(self, coor):
		return Coordinate(self.x / coor.x, self.y / coor.y, self.z / coor.z)

	
	def __str__(self):
		return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'
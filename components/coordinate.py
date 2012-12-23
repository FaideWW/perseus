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
		return self.add(coor.x, coor.y, coor.z)

	def __sub__(self, coor):
		return self.add(coor.x*-1, coor.y*-1, coor.z*-1)

	def __mul__(self, coor):
		return self.scale(coor.x, coor.y, coor.z)

	def __div__(self, coor):
		return self.scale(1/coor.x, 1/coor.y, 1/coor.z)

	
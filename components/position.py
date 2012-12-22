class Position:
	self.x
	self.y
	self.z
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def rel(self, x, y, z=0):
		""" change position relative to current position """
		self.x += x
		self.y += y
		self.z += z
		return self

	def abs(self, x, y, z=0):
		""" set position absolutely on world space """
		self.x = x
		self.y = y
		self.z = z
		return self

	def scale(self, sX, sY, sZ=1):
		""" scale position relative to the origin """
		self.x *= sX
		self.y *= sY
		self.z *= sZ
		return self
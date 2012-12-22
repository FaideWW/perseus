import BoundingObject

class BoundingSphere(BoundingObject):
	self.radius

	def __init__(self, r):
		self.radius = r

	def getBoundType(self):
		return "sphere"
from boundingobject import BoundingObject

class BoundingSphere(BoundingObject):
	def __init__(self, r):
		self.radius = r

	def getBoundType(self):
		return 'sphere'

	def getBoundShape(self):
		return 'convex'

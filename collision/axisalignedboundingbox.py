import BoundingObject

class AxisAlignedBoundingBox(BoundingObject):
	self.half_width
	self.half_height

	def __init__(self, halfwidth, halfheight):
		self.half_width = halfwidth
		self.half_height = halfheight

	def getBoundType(self):
		return "aabb"

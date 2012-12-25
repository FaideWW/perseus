from boundingobject import BoundingObject 
from components.position import Position

class AxisAlignedBoundingBox(BoundingObject):
	def __init__(self, halfwidth, halfheight):
		self.half_width = halfwidth
		self.half_height = halfheight

	def getBoundType(self):
		return 'aabb'

	def getBoundShape(self):
		return "convex"

	def getVertices(self):
		x1 = Position([(self.half_width * -1), (self.half_height * -1)])
		x2 = Position([self.half_width, (self.half_height * -1)])
		y1 = Position([(self.half_width * -1), self.half_height])
		y2 = Position([self.half_width, self.half_height])
		return [x1, x2, y2, y1]

	def __str__(self):
		return str(self.half_width * 2) + 'x' + str(self.half_height * 2)


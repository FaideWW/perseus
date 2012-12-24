class BoundingObject:
	def __init__(self):
		pass

	def getBoundType(self):
		raise NotImplementedError('Bounding object type is an interface.')

	def getBoundShape(self):
		raise NotImplementedError('Bounding object type is an interface.')

	def getVertices(self):
		""" Returns a list of Positions that mark each vertex of the bounding box """

		raise NotImplementedError('Bounding object type is an interface.')
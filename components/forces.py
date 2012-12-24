class Gravity(object):
	""" Gravitational force that always points down (270 degrees) """
	def __init__(self, accel=-2):
		self.accel = accel

	def g(self):
		return self.accel

	def setGravity(self, g):
		self.accel = g
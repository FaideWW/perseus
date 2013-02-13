import math
import math

class Vector(list):
	""" basic list of 3 floats with vector math functionality """


	def __init__(self, lst = []):
		list.__init__(self, lst[:3])
		while len(self) < 3:
			self.append(0)
		self.x = self[0]
		self.y = self[1]
		self.z = self[2]

		#floating point precision margin of 2 decimal places
		self.floatMargin = 10**-2

	def __iadd__(self, other):
		# inline addition is called when the shorthand operator += is used
		self = self + other
		return self

	def __add__(self, other):
		newL = Vector(self)
		if (len(self) <= len(other)):
			l = len(self)
		else:
			l = len(other)
		for i in range(l):
			newL[i] += other[i]
		return Vector(newL[:3])

	def __isub__(self, other):
		self = self - other
		return self

	def __sub__(self, other):
		newL = Vector(self)

		if (len(self) <= len(other)):
			l = len(self)
		else:
			l = len(other)
		for i in range(l):
			newL[i] -= other[i]

		return Vector(newL[:3])

	def __imul__(self, factor):
		self = self * factor
		return self

	def __mul__(self, factor):
		""" multiply vector by a scalar factor """

		ret = Vector(self)
		for x in range(len(ret)):
			ret[x] = ret[x] * float(factor)
		return Vector(ret[:3])

	def __idiv__(self, factor):
		self = self / factor
		return self

	def __div__ (self, factor):
		# should return floating point values
		ret = Vector(self)
		for x in range(len(ret)):
			ret[x] = ret[x] / float(factor)
		return Vector(ret[:3])

	def __ifloordiv(self, factor):
		self = self // factor
		return self

	def __floordiv__(self, factor):
		# equivalent to self // factor
		ret = Vector(self)
		for x in range(len(ret)):
			ret[x] = ret[x] // factor
		return Vector(ret[:3])

	def __eq__(self, other):
		#since we're dealing with floating point values, we need a comparison that allows for some error margin
		areEqual = True
		for i in range(len(self)):
			if abs(self[i] - other[i]) > self.floatMargin:
				areEqual = False
		return areEqual

	def dot(self, other):
		d = 0
		if (len(self) <= len(other)):
			l = len(self)
		for i in range(l):
			d += self[i] * other[i]

		return d

	def cross(self, other):
		""" equivalent of self X other """
		a = list(self)
		b = list(other)
		while len(a) < 3:
			a.append(0)
			b.append(0)

		c = Vector([a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]])
		return Vector(c[:3])

	def rot(self, angle):
		""" rotate a 2d vector by specific angle about Z axis """
		rad_angle = math.radians(angle)
		x = self[0] * math.cos(rad_angle) - self[1] * math.sin(rad_angle)
		y = self[0] * math.sin(rad_angle) + self[1] * math.cos(rad_angle)

		rotV = Vector([x,y])


		return Vector(rotV[:3])

	def mag(self):
		""" returns magnitude of self """
		magsq = 0.0
		for axis in self:
			magsq += axis**2
		magnitude = math.sqrt(magsq)
		return magnitude

	def normalize(self):
		""" return unit vector in the direction of self """
		mag = self.mag()
		if mag == 0: return 0
		return self / mag

	def project(self, axis):
		""" return the 1d projection of a 2d vector onto an arbitrary axis """
		unit_axis = axis.normalize()
		projection = self.dot(unit_axis)
		return projection

	def isParallel(self, other):
		""" returns true if both vectors have the same direction """
		return self.normalize().rot(180) == other.normalize()

	@staticmethod
	def zero():
		return Vector([0,0,0])

	def __str__(self):
		s = '['
		for i in self:
			if abs(i) < self.floatMargin:
				i = 0
			s += str(i) + ', '
		s = s[:-2] + ']'
		return s

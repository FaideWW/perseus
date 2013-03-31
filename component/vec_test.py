import math
class Vector(list):
	""" basic list of ints with vector math functionality """

	def __init__(self, lst = []):
		list.__init__(self, lst)
		while len(self) < 3:
			self.append(0)
		self.x = self[0]
		self.y = self[1]
		self.z = self[2]

	def __add__(self, other):
		newL = list(self)
		if (len(self) <= len(other)):
			l = len(self)
		else:
			l = len(other)
		for i in range(l):
			newL[i] += other[i]
		return newL

	def __sub__(self, other):
		newL = list(self)
		if (len(self) <= len(other)):
			l = len(self)
		else:
			l = len(other)
		for i in range(l):
			newL[i] -= other[i]
		return newL

	def __mul__(self, factor):
		""" multiply vector by a scalar factor """

		ret = list(self)
		for x in range(len(ret)):
			ret[x] = ret[x] * float(factor)
		return ret

	def __div__ (self, factor):
		# should return floating point values
		ret = list(self)
		for x in range(len(ret)):
			ret[x] = ret[x] / float(factor)
		return ret

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
		return c

	def rot(self, angle):
		""" rotate a 2d vector by specific angle about Z axis """
		rad_angle = math.radians(angle)
		x = self[0] * math.cos(rad_angle) - self[1] * math.sin(rad_angle)
		y = self[0] * math.sin(rad_angle) + self[1] * math.cos(rad_angle)

		rotV = Vector([x,y])

		return rotV

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
		return self / mag

	def project(self, axis):
		""" return the 1d projection of a 2d vector onto an arbitrary axis """
		unit_axis = axis.normalize()
		projection = self.dot(unit_axis)
		return projection

	def __str__(self):
		s = '['
		for i in self:
			s += str(i) + ', '
		s = s[:-2] + ']'
		return s

v1 = Vector([2,2])
v2 = Vector([3,1])
v3 = Vector([2,0])
v4 = v2.rot(90)

print v1 + v2, v2 - v1, v1 * 2, v2 / 4
print v1.normalize(), v2.normalize(), v3.normalize()
print
print v2.project(v3), v1.project(v2), v4.scalar_project(v2)
print
print v1.dot(v2)
print v1.cross(v2)
print v1.rot(180)
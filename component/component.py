import math

class Vector(list):
    def __init__(self, num_list):
        list.__init__(self, num_list)
        self.x = self[0]
        self.y = self[1]
        if len(self) > 2:
            self.z = self[2]

        self.space = len(self)

    def dot(self, other):
        if self.space != other.space:
            raise InvalidComparisonException('Vectors are not in the same space')
        return sum([x*y for x,y in zip(self, other)])

    def cross(self, other):
        if self.space != other.space != 3:
            raise InvalidComparisonException('Vectors are not in the correct space')
        return Vector([
            self.y * other.z - self.z * other.y, 
            self.x * other.z - self.z * other.x,
            self.x * other.y - self.y * other.x])

    def rot(self, angle):
        rad_angle = math.radians(angle)
        x = self.x * math.cos(rad_angle) - self.y * math.sin(rad_angle)
        y = self.y * math.sin(rad_angle) + self.y * math.cos(rad_angle)
        return Vector([x,y])

    def mag(self):
        magsq = 0.0
        for axis in self:
            magsq += axis**2
        magnitude = math.sqrt(magsq)
        return magnitude

    def normalize(self):
        mag = self.mag()
        if mag == 0: 
            return 0
        return self / mag

    def project(self, axis):
        unit_axis = axis.normalize()
        projection = self.dot(unit_axis)
        return projection

    def isParallel(self, other):
        return self.normalize() == other.normalize() or self.normalize(180) == other.normalize()

    @staticmethod
    def zero():
        return Vector([0,0,0])


    def __iadd__(self, other):
        self = self + other
        return self

    def __add__(self, other):
        return Vector([x+y for x,y in zip(self, other)])

    def __isub__(self, other):
        self = self - other
        return self

    def __sub__(self, other):
        return Vector([x-y for x,y in zip(self, other)])

    def __imul__(self, factor):
        self = self * other
        return self

    def __mul__(self, factor):
        if not isinstance(factor, (int, long, float)):
            raise TypeError('Scalar multiplication must take an integer or float.  Use dot or cross products for Vector multiplication.')
        return Vector([factor * x for x in self])

    def __idiv__(self, factor):
        self = self / factor
        return self

    def __div__(self, factor):
        if not isinstance(factor, (int, long, float)):
            raise TypeError('Scalar multiplication must take an integer or float.  Use dot or cross products for Vector multiplication.')
        return Vector([x / factor for x in self])

    def __ifloordiv__(self, factor):
        self = self // factor
        return self

    def __floordiv__(self, factor):
        if not isinstance(factor, (int, long, float)):
            raise TypeError('Floor division must take an integer or float.  Use dot or cross products for Vector multiplication.')
        return Vector ([x // factor for x in self])

    def __eq__(self, other):
        return False not in [x == y for x,y in zip(self, other)]

class Position(Vector):
    pass

class Velocity(Vector):
    pass

class InvalidComparisonException(Exception):
    pass
import component.component as component
import render.render as render
import component.unit as unit


class BoundingPoly(object):
    def __init__(self, vertices):
        self.vertex_list = vertices
        self.normal_list = self._genNormalVectors(self.vertex_list)
        self.sides = [True for x in enumerate(self.normal_list)]

    def _genNormalVectors(self, vertices):
        #huzzah for list comprehensions!
        vertices.append(vertices[0])
        return [(component.Vector(dest) - component.Vector(source)).rot(90) for source, dest in zip(vertices, vertices[1:])]

    def getVertices(self):
        return self.vertex_list

    def getAxes(self):
        return [axis for axis, mask in zip(self.normal_list, self.sides) if mask]

    def generateGLObject(self, color):
        topleft = component.Vector([float(min([point[0] for point in self.vertex_list])), float(max([point[1] for point in self.vertex_list]))])
        botright = component.Vector([float(max([point[0] for point in self.vertex_list])), float(min([point[1] for point in self.vertex_list]))])

        return render.GLObject.rectFromPoints(unit.Unit.toPixels(topleft), unit.Unit.toPixels(botright), color)

    def scalar_project(self, axis):
        min_value = min([component.Vector(vertex).scalar_project(axis) for vertex in self.vertex_list])
        max_value = max([component.Vector(vertex).scalar_project(axis) for vertex in self.vertex_list])
        return [min_value, max_value]

    def offset(self, position):
        return BoundingPoly([component.Vector(vertex) + position for vertex in self.vertex_list])

    def positionToString(self, position):
        return [component.Vector(vertex) + position for vertex in self.vertex_list]

    def disableSide(self, side):
        self.sides[side] = False

    def enableSide(self, side):
        self.sides[side] = True

    def toggleSide(self, side):
        self.sides[side] = not self.sides[side]

    @staticmethod
    def fromSize(size):
        return BoundingPoly([[-size.x, size.y], [size.x, size.y], [size.x, -size.y], [-size.x, -size.y]])


class Collidable(object):
    def __init__(self):
        raise NotImplementedError('Collidable is an interface.  Please use one of the available subclasses.')

    def getType(self):
        raise NotImplementedError('Collidable is an interface.  Please use one of the available subclasses.')

    def collideWith(self, ctype):
        raise NotImplementedError('Collidable is an interface.  Please use one of the available subclasses.')


class EntityCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Entity'

    def collideWith(self, ctype):
        if ctype is 'Entity' or ctype is 'Trigger':
            return None
        elif ctype is 'Hostile' or ctype is 'Attack' or ctype is 'Projectile':
            return 'Knockback'
        elif ctype is 'Static':
            return 'Stop'

        #if the code reaches this point there's an invalid type
        raise TypeError('Invalid collision type.')


class HostileCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Hostile'

    def collideWith(self, ctype):
        if ctype is 'Entity' or ctype is 'Hostile' or ctype is 'Trigger' or ctype is 'Player':
            return None
        elif ctype is 'Attack' or ctype is 'Projectile':
            return 'Knockback'
        elif ctype is 'Static':
            return 'Stop'

        #if the code reaches this point there's an invalid type
        raise TypeError('Invalid collision type.')


class PlayerCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Player'

    def collideWith(self, ctype):
        if ctype is 'Entity':
            return None
        elif ctype is 'Hostile':
            return 'Knockback'
        elif ctype is 'Trigger':
            return None
        elif ctype is 'Attack' or ctype is 'Projectile':
            return 'Knockback'
        elif ctype is 'Static':
            return 'Stop'

        #if the code reaches this point there's an invalid type
        raise TypeError('Invalid collision type.')


class TriggerCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Trigger'

    def collideWith(self, ctype):
        if ctype in ['Entity', 'Hostile', 'Player', 'Trigger', 'Attack', 'Projectile', 'Static']:
            return None

        #if the code reaches this point there's an invalid type
        raise TypeError('Invalid collision type.')


class AttackCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Attack'

    def collideWith(self, ctype):
        if ctype in ['Entity', 'Hostile', 'Player', 'Trigger', 'Attack', 'Projectile', 'Static']:
            return None
        #if the code reaches this point there's an invalid type
        raise TypeError('Invalid collision type.')


class ProjectileCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Projectile'

    def collideWith(self, ctype):
        if ctype is 'Entity' or ctype is 'Hostile' or ctype is 'Player':
            return 'StopAll'
        elif ctype is 'Trigger':
            return 'StopAll'
        elif ctype is 'Attack':
            return 'Knockback'
        elif ctype is 'Projectile':
            return 'Bounce'
        elif ctype is 'Static':
            return 'StopAll'

        #if the code reaches this point there's an invalid type
        raise TypeError('Invalid collision type.')


class StaticCollidable(Collidable):
    def __init__(self):
        pass

    def getType(self):
        return 'Static'

    def collideWith(self, ctype):
        return None

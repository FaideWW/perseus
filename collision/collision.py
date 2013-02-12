from components.components import Velocity

class Collider(Object):
    def __init__(self):
        self.collision_queue = []

    def detectCollisions(self, objects):

        possibles = self._broadPhase(objects)
        self.collision_queue = self._narrowPhase(possibles)

    def _broadPhase(self, objects):
        possibles = []
        for i in range(len(objects)-1):
            j = i + 1
            dist = (objects[i].getWorldSpacePosition() - objects[j].getWorldSpacePosition()).mag()
            max_dist = objects[i].getVelocity().mag() + objects[j].getVelocity().mag()
            if dist < max_dist:
                possible = ObjectCollision(objects[i], objects[j])
                if True in [possible.compare(n) for n in possibles]:
                    continue
                else:
                    possibles.append(possible)

        return possibles

    def _narrowPhase(self, possibles):
        collisions = []
        for match in possibles:
            collider = match.obj1.getBoundingPoly() if match.obj1.getVelocity().mag() > match.obj1.getVelocity().mag() else match.obj2.getBoundingPoly()
            colldiee = match.obj2.getBoundingPoly() if collider is match.obj1 else match.obj1.getBoundingPoly()

            collisionExists = True

            collision_axis  = None

            for axis in collidee.getAxes():
                projection1 = collider.project(axis)
                projection2 = collidee.project(axis)

                if projection1.max() < projection2.min() or projection1.min() > projection2.max():
                    collisionExists = False
                    break
                else:
                    axis_depth = max(projection1.max() - projection2.min(), projection2.max() - projection1.min())
                    if collision_depth > axis_depth or collision_axis is None:
                        collision_axis = axis
                        collision_depth = axis_depth

            if collisionExists:
                #get the collision axis
                match.axis = collision_axis
                collisions.append(match)
        return collisions

    def resolveCollisions(self, collisions):
        for collision in collisions:
            obj1 = collision.obj1
            obj2 = collision.obj2
            reaction1 = obj1.collideWith(obj2.getCollider().getType())
            reaction2 = obj2.collideWith(obj1.getCollider().getType())

            for reaction, obj in zip([reaction1, reaction2], [obj1, obj2]):
                if reaction is 'Bounce':
                    #reflect the velocity along the normal then reverse it
                    obj.setVelocity((obj.getVelocity().reflect(collision.axis) * -1))
                elif reaction is 'Stop':
                    reflection = obj.getVelocity().reflect(collision.axis) * -1
                    #"flatten" the reflection along the collision axis, but maintain the corresponding velocity
                    incident_velocity = reflection.project(collision.axis.rot(90))
                    obj.setVelocity(incident_velocity)
                elif reaction is 'StopAll':
                    obj.setVelocity(Velocity.zero())
                elif reaction is 'Knockback':
                    #set the velocity to a preset reverse jump
                    new_velocity = Velocity([(-1 if obj.getDirection is 'right' else 1), 1])
                    obj.setVelocity(new_velocity)
                elif reaction is 'Slow':
                    #this really should accept a factor, but that's a challenge for another build
                    obj.setVelocity(obj.getVelocity() * 0.2)

class ObjectCollision(Object):
    def __init__(self, obj1, obj2, axis=None):
        self.obj1 = obj1
        self.obj2 = obj2
        self.axis = axis

    def compare(self, other):
        return  self.obj1 is other.obj1 and 
                self.obj2 is other.obj2 or 
                self.obj1 is other.obj2 and
                self.obj2 is other.obj1

class BoundingPoly(Object):
    def __init__(self, vertices):
        self.vertex_list = vertices
        self.normal_list = self._genNormalVectors(self.vertex_list)


    def _genNormalVectors(self, vertices):
        #huzzah for list comprehensions!
        return [(dest - source).rot(90) for source, dest in zip(vertices, vertices[1:])]

    def getVertices(self):
        return self.vertex_list

    def getAxes(self):
        return self.normal_list

    def project(self, axis):
        min_value = min([vertex.project(axis) for vertex in self.vertex_list])
        max_value = max([vertex.project(axis) for vertex in self.vertex_list])
        return [min_value,max_value]



class Collidable(Object):
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
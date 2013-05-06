#force floating point division
from __future__ import division

import component.component as component
import maps.map

class Collider(object):
    def __init__(self, tolerance):
        self.collision_queue = []
        self.COLLISION_TOLERANCE = 1 / tolerance

        #this variable determines whether the collider will predict the object's next step,
        # or use the object's current step
        self.PREDICT_STEP = True

        print 'COLLISION_TOLERANCE', self.COLLISION_TOLERANCE

    def detectCollisions(self, objects, worldmap, dt):

        possibles = self._broadPhase(objects, worldmap, dt)
        self.collision_queue = self._narrowPhase(possibles, dt)

    def _broadPhase(self, objects, worldmap, dt):
        """
            Takes a list of all objects, and returns a list of possible object collision points
        """

        space = []

        mapsize = worldmap.getMapSize()

        for row in range(mapsize.y):
            space.append([])
            for block in range(mapsize.x):
                space[row].append(SpaceBlock())

        block_size = worldmap.getTileSize()

        for obj in objects:

            obj_position = self.getObjectPosition(obj, dt, self.PREDICT_STEP)

            if obj.getBoundingPoly() is None:
                continue
            bp = obj.getBoundingPoly().offset(obj_position)

            minx = min([pos.x for pos in bp.getVertices()])
            maxx = max([pos.x for pos in bp.getVertices()])
            miny = min([pos.y for pos in bp.getVertices()])
            maxy = max([pos.y for pos in bp.getVertices()])

            row_min = int(miny / block_size.y)
            row_max = maxy / block_size.y
            col_min = int(minx / block_size.x)
            col_max = maxx / block_size.x


            #print 'rmin', row_min
            #print 'rmax', row_max
            #print 'cmin', col_min
            #print 'cmax', col_max

            #hack to resolve on-edge spatial partitioning

            if row_max % 1 == 0:
                row_max = int(row_max)
            else:
                row_max = int(row_max) + 1
            if col_max % 1 == 0:
                col_max = int(col_max)
            else:
                col_max = int(col_max) + 1

            for row in range(row_min, row_max):
                for col in range(col_min, col_max):
                    space[row][col].objects.append(obj)

        possibles = []

        #this tab nest makes me sick
        for row in space:
            for block in row:
                if len(block) > 1:
                    block_collisions = self._getObjectInteractions(block)
                    for c in block_collisions:
                        if c not in possibles:
                            possibles.append(c)
        #print len(possibles)
        return possibles

    def _getObjectInteractions(self, block):
        #returns a list of objects who share the same block
        obj_pairs = []
        for i in range(len(block.objects)):
            for j in range(i+1, len(block.objects)):
                if type(block.objects[i]) is not maps.map.Tile or type(block.objects[j]) is not maps.map.Tile:
                    obj_pairs.append(ObjectCollision(block.objects[i], block.objects[j]))
        return obj_pairs

    def _narrowPhase(self, possibles, dt):
        collisions = []
        for match in possibles:
            collider = match.obj1 if match.obj1.getVelocity().mag() > match.obj1.getVelocity().mag() else match.obj2
            collidee = match.obj2 if collider is match.obj1 else match.obj1

            collisionExists = True
            collision_depth = None
            collision_axis = None

            axes = collidee.getBoundingPoly().getAxes()
            for axis in axes:
                # #print 'testing'
                # #print axis
                # bp1 = collider.getBoundingPoly().offset(collider.getWorldSpacePosition())
                # bp2 = collidee.getBoundingPoly().offset(collidee.getWorldSpacePosition())
                # #print bp1.positionToString(component.Position.zero())
                # #print bp2.positionToString(component.Position.zero())
                # projection1 = bp1.scalar_project(axis)
                # projection2 = bp2.scalar_project(axis)

                axis_depth = self._getIntersectionDepth(collider, collidee, axis, dt)

                if axis_depth > 0:
                    if axis_depth < self.COLLISION_TOLERANCE:
                        axis_depth = 0
                    if collision_axis is None or collision_depth > axis_depth:
                        collision_axis = axis
                        collision_depth = axis_depth
                else:
                    collisionExists = False
                    #print 'no collision'
                    break

            if collisionExists:
                #get the collision axis
                match.axis = collision_axis
                match.depth = collision_depth
                collisions.append(match)
        return collisions

    def _getIntersectionDepth(self, obj1, obj2, axis, dt):
        """ Return the exact depth of the intersection between two projections """

        pos1 = self.getObjectPosition(obj1, dt, self.PREDICT_STEP)
        pos2 = self.getObjectPosition(obj2, dt, self.PREDICT_STEP)

        bp1 = obj1.getBoundingPoly().offset(pos1)
        bp2 = obj2.getBoundingPoly().offset(pos2)
        projection1 = bp1.scalar_project(axis)
        projection2 = bp2.scalar_project(axis)
        return min(max(projection1) - min(projection2), max(projection2) - min(projection1))

    def getObjectPosition(self, obj, dt, predict=False):
        position = obj.getWorldSpacePosition() + obj.getVelocity() * dt if predict else obj.getWorldSpacePosition()
        #print 'position', position, obj.getWorldSpacePosition(), '+', obj.getVelocity(), '*', dt
        return position

    def resolveCollisions(self, collisions, dt):
        for collision in collisions:
            obj1 = collision.obj1
            obj2 = collision.obj2
            #refresh collision depth

            collision.depth = self._getIntersectionDepth(obj1, obj2, collision.axis, dt)
            if collision.depth < self.COLLISION_TOLERANCE:
                #not a real collision
                continue
            #get the interpolated v for this frame

            #interpolation = self.interpolateCollisionPosition(collision)
            reaction1 = obj1.getCollider().collideWith(obj2.getCollider().getType())
            reaction2 = obj2.getCollider().collideWith(obj1.getCollider().getType())

            for reaction, obj in zip([reaction1, reaction2], [obj1, obj2]):
                if hasattr(obj, 'jumping') and obj.jumping:
                    continue

                other = obj1 if obj is not obj1 else obj2

                pos = self.getObjectPosition(obj, dt, self.PREDICT_STEP)
                pos_other = self.getObjectPosition(other, dt, self.PREDICT_STEP)

                #landing hack
                if hasattr(obj, 'landed'):
                    lateral_vector = component.Vector([1, 0])
                    if collision.axis.dot(lateral_vector) == 0 and pos.y > pos_other.y:
                        #if the collision is vertical and the entity is above its collider
                        obj.landed = True

                if reaction is 'Bounce':
                    #reflect the velocity along the normal then reverse it
                    obj.setVelocity((obj.getVelocity().reflect(collision.axis) * -1))
                elif reaction is 'Stop':
                    #flushly align the bounding boxes along the axis of collision
                    #and flatten the velocity normal to the axis of collision
                    #also flatten acceleration

                    if collision.depth > 0:
                        reverse = collision.axis * collision.depth
                        #get proper directionality for collision axis
                        separation_vector = pos - pos_other
                        if separation_vector.dot(reverse) > 0:
                            #flip the axis
                            reverse *= -1
                        obj.setPosition(pos - reverse)
                        final_velocity = obj.getVelocity().vector_reject(collision.axis)
                        final_acceleration = obj.getAcceleration().vector_reject(collision.axis)

                        #print 'vel1', obj.getVelocity()
                        obj.setVelocity(final_velocity)
                        obj.setAcceleration(final_acceleration)
                    #print 'vel2', obj.getVelocity()
                    pass
                elif reaction is 'StopAll':
                    obj.setVelocity(component.Velocity.zero())
                elif reaction is 'Knockback':
                    #set the velocity to a preset reverse jump
                    new_velocity = component.Velocity([(-1 if obj.getDirection is 'right' else 1), 1])
                    obj.setVelocity(new_velocity)
                elif reaction is 'Slow':
                    #this really should accept a factor, but that's a challenge for another build
                    obj.setVelocity(obj.getVelocity() * 0.2)

    def interpolateCollisionPosition(self, collision):
        """
            Returns the value of interpolation for an object collision to properly position
            colliding objects without clipping into each other

            To simplify things, if both objects are moving we'll hold the slower object
            still during collision

            divide the collision depth by the projection of the velocity on the collision axis
        """

        velocity = collision.obj1.getVelocity() if collision.obj1.getAbsVelocity() >= collision.obj2.getAbsVelocity() else collision.obj2.getVelocity()
        if velocity.mag() == 0:
            return 1
        return 1 - (collision.depth / velocity.scalar_project(collision.axis))


class SpaceBlock(object):
    def __init__(self):
        self.objects = []

    def __len__(self):
        return len(self.objects)


class ObjectCollision(object):
    def __init__(self, obj1, obj2, axis=None, depth=0):
        self.obj1 = obj1
        self.obj2 = obj2
        self.axis = axis
        self.depth = depth

    def compare(self, other):
        return (self.obj1 is other.obj1 and self.obj2 is other.obj2 or self.obj1 is other.obj2 and self.obj2 is other.obj1)

    def __str__(self):
        return '[' + str(self.obj1.id) + ',' + str(self.obj2.id) + ']'

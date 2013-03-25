import component.component as component
import maps.map


class Collider(object):
    def __init__(self):
        self.collision_queue = []

    def detectCollisions(self, objects, worldmap):

        possibles = self._broadPhase(objects, worldmap)
        self.collision_queue = self._narrowPhase(possibles)

    def _broadPhase(self, objects, worldmap):
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
            if obj.getBoundingPoly() is None:
                continue
            bp = obj.getBoundingPoly().offset(obj.getWorldSpacePosition())

            minx = min([pos.x for pos in bp.getVertices()])
            maxx = max([pos.x for pos in bp.getVertices()])
            miny = min([pos.y for pos in bp.getVertices()])
            maxy = max([pos.y for pos in bp.getVertices()])

            row_min = int(miny / block_size.y)
            row_max = maxy / block_size.y
            col_min = int(minx / block_size.x)
            col_max = maxx / block_size.x

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

    def _narrowPhase(self, possibles):
        collisions = []
        for match in possibles:
            collider = match.obj1 if match.obj1.getVelocity().mag() > match.obj1.getVelocity().mag() else match.obj2
            collidee = match.obj2 if collider is match.obj1 else match.obj1

            collisionExists = True
            collision_depth = None
            collision_axis = None

            for axis in collidee.getBoundingPoly().getAxes():
                #print 'testing'
                #print axis
                bp1 = collider.getBoundingPoly().offset(collider.getWorldSpacePosition())
                bp2 = collidee.getBoundingPoly().offset(collidee.getWorldSpacePosition())
                #print bp1.positionToString(component.Position.zero())
                #print bp2.positionToString(component.Position.zero())
                projection1 = bp1.project(axis)
                projection2 = bp2.project(axis)

                if min(projection1) < max(projection2) and min(projection2) < max(projection1) or min(projection2) < max(projection1) and min(projection1) < max(projection2):
                    axis_depth = min(max(projection1) - min(projection2), max(projection2) - min(projection1))
                    if collision_axis is None or collision_depth > axis_depth:
                        collision_axis = axis
                        collision_depth = axis_depth
                else:
                    collisionExists = False
                    #print 'no collision'
                    break

            if collisionExists:
                print 'collision', collision_depth
                #print match.obj1.getWorldSpacePosition(), match.obj1.getBoundingPoly().getVertices()
                #print type(match.obj1), match.obj1.getBoundingPoly().positionToString(match.obj1.getWorldSpacePosition())
                #print match.obj1.getBoundingPoly().project(collision_axis), max(match.obj1.getBoundingPoly().project(collision_axis))

                #print match.obj2.getWorldSpacePosition(), match.obj2.getBoundingPoly().getVertices()
                #print type(match.obj2), match.obj2.getBoundingPoly().positionToString(match.obj2.getWorldSpacePosition())
                #print match.obj2.getBoundingPoly().project(collision_axis), max(match.obj1.getBoundingPoly().project(collision_axis))
                #get the collision axis
                match.axis = collision_axis
                match.depth = collision_depth
                collisions.append(match)
        return collisions

    def resolveCollisions(self, collisions):
        for collision in collisions:

            obj1 = collision.obj1
            obj2 = collision.obj2

            print obj1.getVelocity(), obj2.getVelocity()
            interpolation = self.interpolateCollisionPosition(collision)
            
            reaction1 = obj1.getCollider().collideWith(obj2.getCollider().getType())
            reaction2 = obj2.getCollider().collideWith(obj1.getCollider().getType())

            for reaction, obj in zip([reaction1, reaction2], [obj1, obj2]):
                if reaction is 'Bounce':
                    #reflect the velocity along the normal then reverse it
                    obj.setVelocity((obj.getVelocity().reflect(collision.axis) * -1))
                elif reaction is 'Stop':
                    #flushly align the bounding boxes along the axis of collision
                    #...somehow
                    obj.setVelocity(component.Velocity([0, obj.getVelocity().y]))
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
        return 1 - (collision.depth / velocity.project(collision.axis))


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

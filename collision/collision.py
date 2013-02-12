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

            for axis in collidee.getAxes():
                projection1 = collider.project(axis)
                projection2 = collidee.project(axis)

                if projection1.max() < projection2.min() or projection1.min() > projection2.max():
                    collisionExists = False
                    break
                if collisionExists:
                    collisions.append(match)
        return collisions

    def resolveCollisions(self, collisions):


        # TODO: this method


class ObjectCollision(Object):
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

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




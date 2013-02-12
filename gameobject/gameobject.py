from components.components import Velocity, Position

MAX_VEL = 10

class GameObject(Object):
    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            raise ArgumentError('GameObject properties must contain an ID.')
        if 'position' in kwargs:
            self.position = kwargs['position']
        else:
            raise ArgumentError('GameObject properties must contain a 2D position.')
        self.boundingpoly = None if 'boundingpoly' not in kwargs else kwargs['boundingpoly']
        self.collider = None if 'collider' not in kwargs else kwargs['collider']
        self.type = None if 'type' not in kwargs else kwargs['type']
        self.sprite = None if 'sprite' not in kwargs else kwargs['sprite']
        self.to_render = []
        if self.sprite is not None:
            self.to_render.append(self.sprite)

        self.dir = 'left'

        self.vel = Velocity.zero()
        self.acc = Velocity.zero()

        self.maxV = MAX_VEL

    def addGLObject(self, globj):
        self.to_render.append(globj)

    def getRenderables(self):
        return self.to_render

    def accelerate(self, acc):
        self.acc = self.acc + acc

    def stopAcceleration(self):
        self.acc = Velocity.zero()

    def setVelocity(vel):
        if vel.x < 0:
            self.dir = 'left'
        elif vel.x > 0:
            self.dir = 'right' 
        self.vel = vel

    def getDirection(self):
        return self.dir

    def getWorldSpacePosition(self):
        return self.position

    def getVelocity(self):
        return self.vel

    def getBoundingPoly(self):
        return self.boundingpoly

    def getCollider(self):
        return self.collider

    def addVelocity(self, rel_vel):
        self.vel = self.vel + rel_vel

    def setFlags(self, flag_data):
        #not sure why I put this in for this release.
        pass

    def update(self, dt):
        #add a to v
        self.vel = self.vel + self.acc * dt

        #clamp v
        self.vel = max(self.vel, self.maxV)

        #add p to v
        self.position = self.position self.vel * dt

        for item in self.to_render:
            item.position = (self.position.x, self.position.y)
            
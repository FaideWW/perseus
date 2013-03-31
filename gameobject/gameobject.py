import component.component as component

MAX_VEL = 10
LOCK_X_NEGATIVE = 0
LOCK_X_POSITIVE = 1
LOCK_Y_NEGATIVE = 2
LOCK_Y_POSITIVE = 3

class GameObject(object):
    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            raise ArgumentError('GameObject properties must contain an ID.')
        self.position = None if 'position' not in kwargs else kwargs['position']
        self.boundingpoly = None if 'boundingpoly' not in kwargs else kwargs['boundingpoly']
        self.collider = None if 'collider' not in kwargs else kwargs['collider']
        self.type = None if 'type' not in kwargs else kwargs['type']
        self.position = component.Position.zero() if 'position' not in kwargs else kwargs['position']
        self.sprite = None if 'sprite' not in kwargs else kwargs['sprite']
        self.size = None if 'size' not in kwargs else kwargs['size']

        #movement vector locks
        self.lock_x_negative = False
        self.lock_x_positive = False
        self.lock_y_negative = False
        self.lock_y_positive = False

        self.showingBoundingPoly = False

        self.to_render = []
        if self.sprite is not None:
            self.to_render.append(self.sprite)

        self.renderables = []

        self.dir = 'left'

        self.renderer_index = None

        self.vel = component.Velocity.zero()
        self.acc = component.Velocity.zero()

        self.maxV = MAX_VEL

    def addRenderables(self, rens):
        for ren in rens:
            ren.updatePosition(self.position, self.vel)
        self.renderables += rens

    def addGLObject(self, globj):
        self.to_render.append(globj)

    def setRenderIndex(self, index):
        self.renderer_index = index

    def getSize(self):
        return self.size

    def getToRender(self):
        return self.to_render

    def getRenderables(self):
        return self.renderables

    def accelerate(self, acc):
        self.acc = self.acc + acc

    def stopAcceleration(self):
        self.acc = component.Velocity.zero()

    def showBoundingPoly(self, r=None):
        if not self.showingBoundingPoly:
            self.showingBoundingPoly = True
            if self.boundingpoly is not None:
                if r is None:
                    self.to_render.append(self.boundingpoly.generateGLObject([0.0, 1.0, 0.0, 1.0]))
                else:
                    self.addRenderables(r.generateRenderables([self.boundingpoly.generateGLObject([0.0, 1.0, 0.0, 1.0])]))

    def hideBoundingPoly(self):
        pass

    def setVelocity(self, vel):
        print 'setting velocity to', vel
        if vel.x < 0:
            self.dir = 'left'
        elif vel.x > 0:
            self.dir = 'right'
        self.vel = vel

    def setAcceleration(self, acc):
        self.acc = acc

    def getDirection(self):
        return self.dir

    def setPosition(self, pos):
        self.position = pos

    def getWorldSpacePosition(self):
        return self.position

    def getVelocity(self):
        return self.vel

    def getAcceleration(self):
        return self.acc

    def getAbsVelocity(self):
        return self.vel.mag()

    def getBoundingPoly(self):
        return self.boundingpoly

    def getCollider(self):
        return self.collider

    def addVelocity(self, rel_vel):
        self.vel = self.vel + rel_vel

    def lockMovement(self, direction):
        if (direction == LOCK_X_NEGATIVE):
            self.lock_x_negative = True
        elif (direction == LOCK_X_POSITIVE):
            self.lock_x_positive = True
        elif (direction == LOCK_Y_NEGATIVE):
            self.lock_y_negative = True
        elif (direction == LOCK_X_POSITIVE):
            self.lock_x_positive = True

    def unlockMovement(self, direction):
        if (direction == LOCK_X_NEGATIVE):
            self.lock_x_negative = False
        elif (direction == LOCK_X_POSITIVE):
            self.lock_x_positive = False
        elif (direction == LOCK_Y_NEGATIVE):
            self.lock_y_negative = False
        elif (direction == LOCK_X_POSITIVE):
            self.lock_x_positive = False

    def getSpeedAlongAxis(self, axis):
        return self.getVelocity().scalar_project(axis)

    def setFlags(self, flag_data):
        #not sure why I put this in for this release.
        pass

    def update(self, dt):
        #add a to v
        self.setVelocity(self.getVelocity() + self.acc * dt)

        #clamp v
        self.vel = max(self.vel, self.maxV)

        #lock any vectors
        if self.lock_x_negative:
            self.vel.x = max(self.vel.x, 0)
        if self.lock_x_positive:
            self.vel.x = min(self.vel.x, 0)
        if self.lock_y_negative:
            self.vel.y = max(self.vel.y, 0)
        if self.lock_y_positive:
            self.vel.y = min(self.vel.y, 0)

        #add p to v
        self.position = self.position + self.vel * dt

        if self.sprite is not None:
            self.sprite.update(dt)

        for item in self.to_render:
            item.position = (self.position.x, self.position.y)

        for ren in self.renderables:
            ren.updatePosition(self.position, self.vel)




class ArgumentError(Exception):
    pass

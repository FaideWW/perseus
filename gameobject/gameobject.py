import component.component as component

MAX_VEL = 10


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
        if vel.x < 0:
            self.dir = 'left'
        elif vel.x > 0:
            self.dir = 'right'
        self.vel = vel

    def getDirection(self):
        return self.dir

    def setPosition(self, pos):
        self.position = pos

    def getWorldSpacePosition(self):
        return self.position

    def getVelocity(self):
        return self.vel

    def getAbsVelocity(self):
        return self.vel.mag()

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
        self.position = self.position + self.vel * dt
        print 'pos', self.position

        if self.sprite is not None:
            self.sprite.update(dt)

        for item in self.to_render:
            item.position = (self.position.x, self.position.y)

        for ren in self.renderables:
            ren.updatePosition(self.position, self.vel)


class ArgumentError(Exception):
    pass

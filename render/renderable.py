import component.component as component

class Renderable(object):
    """
        Renderable component
        wraps position updating
    """
    def __init__(self, obj, renderer, index):
        self.object = obj
        self.r = renderer
        self.index = index
        self.pos = component.Position.zero()
        self.vel = component.Velocity.zero()

    def updatePosition(self, pos, vel=component.Velocity.zero()):
        del_pos = pos - self.pos
        self.pos = pos
        #ALYWAYS reset velocity if it's not specified.  we'll get some wacky
        #behavior if we don't
        self.vel = vel
        self.r.changeBatchPosition(self.index, del_pos)
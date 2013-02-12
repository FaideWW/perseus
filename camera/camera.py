class Camera(GameObject):
    def __init__(self, viewport, target=None):
        self.viewport = viewport
        self.dest_viewport = None
        self.target = target
        self.target_ransition = 0
        self.viewport_transition = 0

    def setTarget(self, target, transition=0):
        self.target = target
        self.target_transition = transition

    def zoom(self, new_viewport, transition=0):
        self.dest_viewport = new_viewport
        self.viewport_transition = transition

    def toClipSpace(self):
        return (-1) * self.getWorldSpacePosition() + self.viewport / 2

    def update(self, dt):
        if self.target_transition > 0:
            self.target_transition = self.target_transition - dt
            dest_direction = self.target - self.getWorldSpacePosition()
            to_move = dest_direction * min((dt / self.target_transition),1)
            self.position = self.position + to_move
        else:
            self.position = self.target.getWorldSpacePosition()
        if self.viewport_transition > 0:
            self.viewport_transition - self.viewport_transition - dt
            diff = self.dest_viewport - self.viewport
            to_scale = diff * min((dt, self.viewport_transition), 1)
            self.viewport = self.viewport + to_scale
        else:
            self.viewport = self.dest_viewport
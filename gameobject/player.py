import gameobject
import component.component as component


ROLL_TIMER = 1

PLAYER_X_RUN = 4
PLAYER_X_SPRINT = 1.5
PLAYER_X_CROUCH = 0.5
PLAYER_Y_JUMP = 6
PLAYER_Y_ROLLJUMP = 8
PLAYER_Y_DBLJUMP = 3


class Player(gameobject.GameObject):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.setState('IDLE')
        self.landed = True
        self.moving_left = False
        self.moving_right = False
        self.roll_timer = 0

    def getMovementState(self):
        return self.movement_state

    def checkState(self):
        #state checks
        if self.vel == component.Velocity.zero():
            self.setState('IDLE')
        if not self.landed and (self.movement_state is not 'AIRONE' or self.movement_state is not 'AIRTWO'):
            self.setState('AIRONE')
        if self.movement_state is 'AIRONE' or self.movement_state is 'AIRTWO' and self.landed and self.vel.y != 0:
            self.setState('LAND')
            self.roll_timer = 0
        if self.movement_state is 'LAND' and self.roll_timer > ROLL_TIMER:
            if self.vel.x > 0:
                self.movment_state = 'RUN'
            else:
                self.setState('IDLE')
        if self.movement_state is 'ROLL' and self.roll_timer > ROLL_TIMER:
            if self.landed:
                if self.vel.x > 0:
                    self.setState('RUN')
                else:
                    self.setState('IDLE')
            else:
                self.setState('AIRONE')

    def left(self, pressed):
        if pressed:
            self.moving_left = True
            self.vel = component.Velocity([-PLAYER_X_RUN, self.vel.y])
            if self.movement_state is 'SPRINT':
                self.vel = self.vel * PLAYER_X_SPRINT
            elif self.movement_state is 'CROUCH':
                self.vel = self.vel * PLAYER_X_CROUCH
            else:
                self.setState('RUN')
        else:
            self.moving_left = False
            if not self.moving_right:
                self.stop()
            self.checkState()

    def right(self, pressed):
        if pressed:
            self.moving_right = True
            self.vel = component.Velocity([PLAYER_X_RUN, self.vel.y])
            if self.movement_state is 'SPRINT':
                self.vel = self.vel * PLAYER_X_SPRINT
            elif self.movement_state is 'CROUCH':
                self.vel = self.vel * PLAYER_X_CROUCH
            else:
                self.setState('RUN')
        else:
            self.moving_right = False
            if not self.moving_left:
                self.stop()
            self.checkState()

    def sprint(self):
        if self.movement_state is 'RUN':
            self.vel = self.vel * PLAYER_X_SPRINT
        self.setState('SPRINT')

    def down(self, pressed):
        if pressed:
            if self.movement_state is 'IDLE' or self.movement_state is 'RUN':
                self.setState('CROUCH')
            elif self.movement_state is 'SPRINT':
                self.setState('SLIDE')
            elif self.movement_state is 'LAND':
                self.roll_timer = 0
                self.setState('ROLL')
        else:
            self.checkState()

    def up(self, pressed):
        if pressed:
            if self.movement_state is 'IDLE' or self.movement_state is 'RUN' or self.movement_state is 'SPRINT':
                self.landed = False
                self.vel.y = PLAYER_Y_JUMP
                self.setState('AIRONE')
            elif self.movement_state is 'ROLL':
                self.landed = False
                self.vel.y = PLAYER_Y_ROLLJUMP
                self.setState('AIRONE')
            elif self.movement_state is 'AIRONE':
                self.vel.y = self.vel.y + PLAYER_Y_DBLJUMP
                self.setState('AIRTWO')
        else:
            self.checkState()

    def stop(self):
        self.vel = component.Velocity([0, self.vel.y])

    def setState(self, state):
        print 'state: ' + state
        self.movement_state = state

    def update(self, dt):
        """
            things to do in this update:
            clamp velocity
            update the roll timer
        """
        super(Player, self).update(dt)

        if self.movement_state is 'LAND' or self.movement_state is 'ROLL':
            self.roll_timer = self.roll_timer + dt

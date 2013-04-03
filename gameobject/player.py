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
        self.landed = False
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.roll_timer = 0

    def getMovementState(self):
        return self.movement_state

    def checkState(self):
        #state checks
        print 'land', self.landed
        if self.vel == component.Velocity.zero():
            self.setState('IDLE')
            self.moving_left = False
            self.moving_right = False
        elif not self.landed and (self.movement_state is not 'AIRONE' or self.movement_state is not 'AIRTWO'):
            self.setState('AIRONE')
        elif (self.movement_state is 'AIRONE' or self.movement_state is 'AIRTWO') and self.landed and self.vel.y != 0:
            self.setState('LAND')
            self.landed = True
            self.roll_timer = 0
        elif self.movement_state is 'LAND' and self.roll_timer > ROLL_TIMER:
            if self.vel.x > 0:
                self.movment_state = 'RUN'
            else:
                self.setState('IDLE')
        elif self.movement_state is 'ROLL' and self.roll_timer > ROLL_TIMER:
            if self.landed:
                if self.vel.x > 0:
                    self.setState('RUN')
                else:
                    self.setState('IDLE')
            else:
                self.setState('AIRONE')

    def left(self):
        self.moving_left = True
        self.setVelocity(component.Velocity([-PLAYER_X_RUN, self.vel.y]))
        if self.movement_state is 'SPRINT':
            self.setVelocity(self.getVelocity() * PLAYER_X_SPRINT)
        elif self.movement_state is 'CROUCH':
            self.setVelocity(self.getVelocity() * PLAYER_X_CROUCH)
        else:
            self.setState('RUN')

    def right(self):
        self.moving_right = True
        self.setVelocity(component.Velocity([PLAYER_X_RUN, self.vel.y]))
        if self.movement_state is 'SPRINT':
            self.setVelocity(self.getVelocity() * PLAYER_X_SPRINT)
        elif self.movement_state is 'CROUCH':
            self.setVelocity(self.getVelocity() * PLAYER_X_CROUCH)
        else:
            self.setState('RUN')

    def sprint(self):
        if self.movement_state is 'RUN':
            self.setVelocity(self.getVelocity() * PLAYER_X_SPRINT)
        self.setState('SPRINT')

    def down(self):
        if self.movement_state is 'IDLE' or self.movement_state is 'RUN':
            self.setState('CROUCH')
        elif self.movement_state is 'SPRINT':
            self.setState('SLIDE')
        elif self.movement_state is 'LAND':
            self.roll_timer = 0
            self.setState('ROLL')

    def up(self):
        self.jumping = True
        if self.movement_state is 'IDLE' or self.movement_state is 'RUN' or self.movement_state is 'SPRINT':
            self.landed = False
            self.setVelocity(component.Velocity([self.getVelocity().x, PLAYER_Y_JUMP]))
            self.setState('AIRONE')
        elif self.landed and self.movement_state is 'ROLL':
            self.landed = False
            self.setVelocity(component.Velocity([self.getVelocity().x, PLAYER_Y_ROLLJUMP]))
            self.setState('AIRONE')
        elif self.movement_state is 'AIRONE':
            self.setVelocity(component.Velocity([self.getVelocity().x, self.getVelocity().y + PLAYER_Y_DBLJUMP]))
            self.setState('AIRTWO')

    def stop(self):
        self.setVelocity(component.Velocity([0, self.vel.y]))

    def setState(self, state):
        print 'state: ' + state
        self.movement_state = state

    def setFlags(self, flags):
        pass

    def resetState(self):
        #reset all flags for a given cycle
        self.jumping = False

        #reset lateral movement
        v = component.Velocity([0, self.getVelocity().y])
        self.setVelocity(v)

    def update(self, dt):
        """
            things to do in this update:
            clamp velocity
            update the roll timer
        """
        super(Player, self).update(dt)

        self.checkState()
        if self.movement_state is 'LAND' or self.movement_state is 'ROLL':
            self.roll_timer = self.roll_timer + dt

        self.resetState()


ROLL_TIMER = 1000

PLAYER_X_RUN = 4
PLAYER_X_SPRINT = 1.5
PLAYER_X_CROUCH = 0.5
PLAYER_Y_JUMP = 6
PLAYER_Y_ROLLJUMP = 8
PLAYER_Y_DBLJUMP = 3

class Player(GameObject):
    def __init__(self, **kwargs):
        super(Player, self).__init__(kwargs)
        self.movement_state = 'IDLE'
        self.landed = True
        self.roll_timer = 0

    def getMovementState(self):
        return self.movement_state

    def checkState(self):
        #state checks
        if self.vel == vel.zero():
            self.movement_state = 'IDLE'
        if not self.landed and (self.movement_state is not 'AIRONE' or self,movement_state is not 'AIRTWO'):
            self.movement_state = 'AIRONE'
        if self.movement_state is 'AIRONE' or self.movement_state is 'AIRTWO' and self.landed and self.vel.y != 0:
            self.movement_state = 'LAND'
            self.roll_timer = 0
        if self.movement_state is 'LAND' and self.roll_timer > ROLL_TIMER:
            if self.vel.x > 0:
                self.movment_state = 'RUN'
            else:
                self.movement_state = 'IDLE'
        if self.movement_state is 'ROLL' and self.roll_timer > ROLL_TIMER:
            if self.landed:
                if self.vel.x > 0:
                    self.movement_state = 'RUN'
                else:
                    self.movement_state = 'IDLE'
            else:
                self.movement_state = 'AIRONE'

    def left(self):
        self.vel = -PLAYER_X_RUN
        if self.movement_state is 'SPRINT':
            self.vel = self.vel * PLAYER_X_SPRINT
        elif self.movement_state is 'CROUCH':
            self.vel = self.vel * PLAYER_X_CROUCH
        else:
            self.movement_state = 'RUN'

    def right(self):
        self.vel = PLAYER_X_RUN
        if self.movement_state is 'SPRINT':
            self.vel = self.vel * PLAYER_X_SPRINT
        elif self.movement_state is 'CROUCH':
            self.vel = self.vel * PLAYER_X_CROUCH
        else:
            self.movement_state = 'RUN'

    def sprint(self):
        if self.movement_state is 'RUN':
            self.vel = self.vel * PLAYER_X_SPRINT
        self.movement_state = 'SPRINT'

    def down(self):
        if self.movement_state is 'IDLE' or self.movement_state is 'RUN':
            self.movement_state = 'CROUCH'
        elif self.movement_state is 'SPRINT':
            self.movement_state = 'SLIDE'
        elif self.movement_state is 'LAND':
            self.roll_timer = 0
            self.movement_state = 'ROLL'

    def up(self):
        if self.movement_state is 'IDLE' or self.movement_state is 'RUN' or self.movement_state is 'SPRINT':
            self.landed = False
            self.vel.y = PLAYER_Y_JUMP
            self.movement_state = 'AIRONE'
        elif self.movement_state is 'ROLL':
            self.landed = False
            self.vel.y = PLAYER_Y_ROLLJUMP
            self.movement_state = 'AIRONE'
        elif self.movement_state is 'AIRONE':
            self.vel.y = self.vel.y + PLAYER_Y_DBLJUMP
            self.movement_state = 'AIRTWO'

    def stop(self):
        self.vel.x = 0

    def update(self, dt):
        """
            things to do in this update:
            clamp velocity
            update the roll timer
        """
        super(Player, self).update(dt)

        if self.movement_state is 'LAND' or self.movement_state is 'ROLL':
            self.roll_timer = self.roll_timer + dt

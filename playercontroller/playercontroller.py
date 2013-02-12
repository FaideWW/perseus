from pyglet.window import key

class PlayerController(Object):
    def __init__(self, player):
        self.player = player
        self.keymap = {
            '97':'left',
            '100':'right',
            '115':'down',
            '119':'up'
        }
        self.pressed_keys = []
        self.downfunction_table = {
            'left': 'leftPress',
            'right': 'rightPress',
            'up': 'upPress',
            'down': 'downPress',
        }

        self.upfunction_table = {
            'left': 'leftRelease',
            'right': 'rightRelease'
        }

    def bindKeys(self, key_config):
        """
            still not sure how I want to handle this.  for now this method is
            unnecessary since the only bindings are the directional keys.
            maybe push this into the next prototype
        """


    def keyDown(self, key):
        if str(key) in self.keymap:
            action = getattr(PlayerController, self.downfunction_table[self.keymap[str(key)]])
            self.action()
        self.pressed_keys.append(key)

    def keyUp(self, key):
        if str(key) in self.keymap and self.keymap[str(key)] in self.upfunction_table:
            action = getattr(PlayerController, self.upfunction_table[self.keymap[str(key)]])
        self.pressed_keys.remove(key)

    def leftPress(self):
        self.player.left()

    def rightPress(self):
        self.player.right()

    def upPress(self):
        self.player.up()

    def downPress(self):
        self.player.down()

    def leftRelease(self):
        if key.S not in self.pressed_keys and key.A not in self.pressed_keys:
            self.player.stop()

    def rightRelease(self):
        if key.S not in self.pressed_keys and key.A not in self.pressed_keys:
            self.player.stop()

    
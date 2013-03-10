from pyglet.window import key


class PlayerController(object):
    def __init__(self, player):
        self.player = player
        self.keymap = {
            '65361': 'left',
            '65363': 'right',
            '65364': 'down',
            '65362': 'up'
        }
        self.pressed_keys = []
        self.function_table = {
            'left': 'left',
            'right': 'right',
            'up': 'up',
            'down': 'down',
        }

    def bindKeys(self, key_config):
        """
            still not sure how I want to handle this.  for now this method is
            unnecessary since the only bindings are the directional keys.
            maybe push this into the next prototype
        """

    def keyDown(self, key):
        if str(key) in self.keymap:
            getattr(PlayerController, self.function_table[self.keymap[str(key)]])(self, True)
        self.pressed_keys.append(key)

    def keyUp(self, key):
        if str(key) in self.keymap and self.keymap[str(key)] in self.function_table:
            getattr(PlayerController, self.function_table[self.keymap[str(key)]])(self, False)
        self.pressed_keys.remove(key)

    def left(self, pressed):
        print 'left'
        self.player.left(pressed)

    def right(self, pressed):
        print 'right'
        self.player.right(pressed)

    def up(self, pressed):
        print 'up'
        self.player.up(pressed)

    def down(self, pressed):
        print 'down'
        self.player.down(pressed)

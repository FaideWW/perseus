class PlayerController(object):

    def __init__(self, player):
        self.player = player
        self.keymap = {
            '65361': 'left',
            '65363': 'right',
            '65364': 'down',
            '65362': 'up'
        }
        self.function_table = {
            'left': 'left',
            'right': 'right',
            'up': 'up',
            'down': 'down',
        }

        """
            key bindings

            we need two separate mappings here: one for instant 'one-off'
            bindings (jump, fire, etc) and another for continuous bindings
            (run, crouch, etc)

        """
        self.instant_mapping = {}
        self.instant_mapping['up'] = self.up

        self.continuous_mapping = {}
        self.continuous_mapping['left'] = self.left
        self.continuous_mapping['right'] = self.right

    def bindKeys(self, key_config):
        """
            still not sure how I want to handle this.  for now this method is
            unnecessary since the only bindings are the directional keys.
            maybe push this into the next prototype
        """

    def keyDown(self, key):
        mapped_key = self.keymap[str(key)]
        if mapped_key in self.instant_mapping:
            self.instant_mapping[mapped_key]()

    def keyUp(self, key):
        pass

    def left(self):
        self.player.left()

    def right(self):
        self.player.right()

    def up(self):
        self.player.up()

    def down(self):
        self.player.down()

    def update(self, dt, key_state):
        #throw updates for all keys that need them
        for keypress in key_state.items():
            if keypress[1] is True:
                if str(keypress[0]) in self.keymap:
                    mapped_key = self.keymap[str(keypress[0])]
                    if mapped_key in self.continuous_mapping:
                        self.continuous_mapping[mapped_key]()

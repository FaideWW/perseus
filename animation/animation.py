from pyglet.sprite import Sprite
import pyglet.image

import component.component as component


class Animation(object):
    def __init__(self, spritesheet, region_data, o=None, repeats=True):
        origin = component.Position.zero() if o is None else o
        #region data is a filesheet
        self.spritesheet = spritesheet
        self.region_data = self._readAnimationData(region_data)
        self.frames = self._buildFrames(self.spritesheet, self.region_data, origin)
        self.time_since = 0
        self.repeats = repeats
        self.current_frame = 0

        self.sprite = Sprite(self.frames[0])

    def _readAnimationData(self, region_data):
        dataArray = []
        with open(region_data) as r:
        #number of milliseconds between frames
            self.freq = (1 / float(r.readline())) * 1000
            for line in r.readlines():
                data = line.rstrip('\n').split(',')
                if len(data) != 4 and len(data) != 6:
                    raise TypeError('Region data is invalid. ' + str(len(data)))
                #translate data into position values
                data = [component.Position([int(i), int(j)]) for i, j in zip(data[::2], data[1::2])]
                dataArray.append(data)
        return dataArray

    def _buildFrames(self, spritesheet, frame_data, o):
        """
            Gen a bunch of TextureRegions from spritesheet.
        """
        sprites = pyglet.image.load(spritesheet)
        frame_list = []

        for frame in range(len(frame_data)):

            #the formatting on this gets a little wonky because of the way pyglet accepts coordinates

            x = frame_data[frame][0].x
            y = frame_data[frame][0].y
            w = frame_data[frame][1].x - x
            h = frame_data[frame][1].y - y

            pygl_x = x
            pygl_y = sprites.height - (y + h)

            frame_obj = sprites.get_region(pygl_x, pygl_y, w, h)

            #compensate for silly frame offset issues
            frame_obj.anchor_x = (w / 2) + o.x
            frame_obj.anchor_y = (h / 2) + o.y

            frame_list.append(frame_obj)
        return frame_list

    def update(self, dt):
        self.time_since += dt
        if self.time_since >= self.freq:
            self.nextFrame()
            self.time_since = self.time_since % self.freq

    def nextFrame(self):
        if self.repeats:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        else:
            self.current_frame = min(self.current_frame + 1, len(self.frames) - 1)
        self.sprite.image = self.frames[self.current_frame]

    def getCurrentFrame(self):
        return self.current_frame

    def asPygletAnimation(self):
        return pyglet.image.Animation.from_image_sequence(self.frames, self.freq / 1000, self.repeats)

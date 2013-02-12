from pyglet.graphics import Sprite
import pyglet.image

class Animation(Object):
    def __init__(self, spritesheet, region_data, fps, repeats=True):
        #region data is a filesheet
        self.spritesheet = spritesheet
        self.region_data = self._readAnimationData(region_data) 
        self.frames = self._buildFrames(self.spritesheet, self.region_data)
        #number of milliseconds between frames
        self.freq = (1 / fps) * 1000
        self.time_since = 0
        self.repeats = repeats
        self.current_frame = 0

        self.sprite = pyglet.graphics.Sprite(self.frames[0])

    def _readAnimationData(self, region_data):
        dataArray = []
        with open(region_data) as r:
            for line in r.readLines():
                data = line.rstrip('\n').split(',')
                if len(data) != 8 or len(data) != 10:
                    raise TypeError('Region data is invalid.')
                #translate data into position values
                data = [Position([int(i), int(j)]) for i, j in zip(data[::2], data[1::2])]
                dataArray.append(data)
        return dataArray

    def _buildFrames(self, spritesheet, frame_data):
        """
            Gen a bunch of TextureRegions from spritesheet.
        """
        sprites = pyglet.image.load(spritesheet)
        frame_list = []


        for frame in range(len(frame_data)):
            x = frame_data[frame][0]
            y = frame_data[frame][1]
            w = frame_data[frame][2] - x
            h = frame_data[frame][3] - y
            o = Position.zero() if len(frame_data) < 5 else frame_data[frame][4]

            frame = sprites.get_region(x,y,w,h)
            frame.anchor_x = -o.x
            frame.anchor_y = -o.y

            frame_list.append(frame)
        return frame_list

    def update(self, dt):
        self.time_since = self.time_since + dt
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
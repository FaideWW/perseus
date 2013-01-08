import sys, os
import pyglet
from pyglet.window import key
import math

from components.position import Position

asset_path = '/'.join(os.path.abspath(__file__).rsplit('/')[:-2]) + '/assets'


class SpritesheetAnimation(object):
	def __init__(self, spritesheet, anim_data, fps, position, repeats=True):
		"""
			anim_data should include the full filepath to the data file
			same with spritesheet
		"""
		self.imgdata = self.readAnimationData(anim_data)
		self.spritesheet = spritesheet
		self.fps = fps
		self.position = position
		self.repeats = repeats
		self.currentframe = 0
		self.paused = False

		self.images = self.buildFrames(self.imgdata, self.spritesheet)

		self.spriteRenderer = pyglet.sprite.Sprite(self.images[0])

	def readAnimationData(self, dataFile):
		dataArray = []
		with open(dataFile) as animation_data:
			for line in animation_data.readlines():
				data = line.rstrip('\n').split(',')
				data[0] = int(data[0])
				while len(dataArray) <= data[0]:
					dataArray.append({})
				for item in data:
					if item == data[0]:
						continue
					kv = item.split(':')

					# property-ambiguous list comprehension.  
					# most properties of animation frames are just lists of integers
					# if we need a string/float comprehension, this will change
					kv[1] = [int(x) for x in kv[1].split(' ')]
					dataArray[data[0]][kv[0]] = kv[1]

		return dataArray

	def buildFrames(self, imgdata, spritesheet):
		sprites = pyglet.image.load(spritesheet)
		frameList = []

		for frame in range(len(imgdata)):	
			if 'region' in imgdata[frame]:
				x = imgdata[frame]['region'][0]
				y = imgdata[frame]['region'][1]
				w = imgdata[frame]['region'][2] - imgdata[frame]['region'][0]
				h = imgdata[frame]['region'][3] - imgdata[frame]['region'][1]
				
				f = sprites.get_region(x,y,w,h)
				if 'offset' in imgdata[frame]:
					f.anchor_x = -imgdata[frame]['offset'][0]
					f.anchor_y = -imgdata[frame]['offset'][1]

				frameList.append(f)
		return frameList

	def setSpecialImageData(self, imgdata, frame=-1):
		if frame == -1:
			self.imgdata = imgdata
		else:
			self.imgdata[frame] = imgdata

	def draw(self):
		self.spriteRenderer.draw()

	def togglePause(self):
		self.paused = not self.paused

	def igetCurrentFrame(self):
		return int(math.floor(self.currentframe))

	def update(self, dt):
		lastFrame = self.currentframe
		if not self.paused:
			self.currentframe += (dt * self.fps)
		self.currentframe %= len(self.images)

		self.spriteRenderer.set_position(self.position.x, self.position.y)

		if lastFrame != self.currentframe:
			self.changeFrames(self.igetCurrentFrame())

	def changeFrames(self, newframe):
		self.spriteRenderer.image = self.images[newframe]

		if newframe+1 == len(self.images) and not self.repeats:
			self.paused = True

spritesheet_path = asset_path + '/sliced_sprites/left/jump/left_jump_0.png'
data_path = asset_path + '/sliced_sprites/left/jump/jump.imgdata'
anim = SpritesheetAnimation(spritesheet_path, data_path, 1, Position([100, 100]))
#anim.setSpecialImageData({'offset': Position([100,100])}, 1)

window = pyglet.window.Window()
fps = pyglet.clock.ClockDisplay()


totalseconds = 0


label = pyglet.text.Label(str(totalseconds),
	font_name='Times New Roman',
	font_size=36,
	x=window.width//2, y=window.height//2,
	anchor_x='center', anchor_y='center')

@window.event
def on_draw():
	window.clear()
	label.draw()
	anim.draw()
	fps.draw()
	#image.blit(0,0)


@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.SPACE:
		anim.togglePause()


# log all events (including mouse movement, which can get quite annoying)
# window.push_handlers(pyglet.window.event.WindowEventLogger())

def update(dt):
	global totalseconds
	totalseconds += dt
	label.text = str(math.floor(totalseconds))
	anim.update(dt)
	pass

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
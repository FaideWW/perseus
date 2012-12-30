import sys, os
import pyglet
from pyglet.window import key
import math

from components.position import Position

asset_path = '/'.join(os.path.abspath(__file__).rsplit('/')[:-2]) + '/assets'


class Animation(object):
	def __init__(self, imageName, fps, position, repeats=True):

		self.imgdata = []
		self.imgpath = asset_path + '/sliced_sprites/' + imageName
		self.imglist = []
		for filename in sorted(os.listdir(self.imgpath)):
			if filename.endswith('.imgdata'):
				self.imgdata = self.readData(self.imgpath + '/' + filename)
				continue
			self.imglist.append(pyglet.image.load(self.imgpath + '/' + filename))
			self.imgdata.append({})
		print self.imglist
		self.fps = fps
		self.currentframe = 0
		self.paused = False

		self.isRepeating = repeats
		self.position = position
		self.spriteRenderer = pyglet.sprite.Sprite(self.imglist[0])

	def readData(self, filename):
		dataArray = []
		with open(filename) as imgData:
			for line in imgData.readlines():
				data = line.rstrip('\n').split(',')
				data[0] = int(data[0])
				while len(dataArray) <= data[0]:
					dataArray.append({})
					print len(dataArray)
				for item in data:
					if item == data[0]: continue
					#key_value: [0] is the key, [1] is the value
					key_value = item.split(':')

					if key_value[0] == 'offset':
						key_value[1] = Position([int(x) for x in key_value[1].split(' ')])
					print len(dataArray), data[0], key_value[0], key_value[1]
					dataArray[data[0]][key_value[0]] = key_value[1]

		return dataArray



	def setSpecialImageData(self, imgData, frame=-1):
		""" if no frame is specified, imgData is a 2D list.  else, imgData is a 1D list """ 
		if frame == -1:
			self.imgdata = imgData
		else:
			self.imgdata[frame] = imgData

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
		self.currentframe %= len(self.imglist)

		if lastFrame != self.currentframe:
			#we're dealing with a new frame
			self.changeFrames(self.igetCurrentFrame())

	def changeFrames(self, newframe):
		self.spriteRenderer.image = self.imglist[newframe]
		if 'offset' in self.imgdata[newframe]:
			net_position_x = self.imgdata[newframe]['offset'].x + self.position.x
			net_position_y = self.imgdata[newframe]['offset'].y + self.position.y
			self.spriteRenderer.set_position(net_position_x, net_position_y)
		else:
			self.spriteRenderer.set_position(self.position.x, self.position.y)


		if newframe+1 == len(self.imglist) and not self.isRepeating:
			self.paused = True

anim = Animation('left/jump', 20, Position([100,100]))
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
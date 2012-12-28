import sys, os
import pyglet
from pyglet.window import key
import math

asset_path = '/'.join(os.path.abspath(__file__).rsplit('/')[:-2]) + '/assets'


class Animation(object):
	def __init__(self, imageName, fps):
		self.imgpath = asset_path + '/sliced_sprites/' + imageName
		self.imglist = []
		for filename in sorted(os.listdir(self.imgpath)):
			self.imglist.append(pyglet.image.load(self.imgpath + '/' + filename))

		print self.imglist
		self.fps = fps
		self.currentframe = 0
		self.paused = False


	def getSprite(self):
		return self.imglist[int(math.floor(self.currentframe))]

	def togglePause(self):
		self.paused = not self.paused


	def update(self, dt):
		if not self.paused:
			self.currentframe += (dt * self.fps)
		self.currentframe %= len(self.imglist)

anim = Animation('left/jump', 20)
print anim.imglist

window = pyglet.window.Window()
image = pyglet.sprite.Sprite(anim.getSprite(), 100, 100)
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
	image.draw()
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
	image.image = anim.getSprite()
	pass

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
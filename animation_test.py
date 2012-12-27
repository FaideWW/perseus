import pyglet, sys




window = pyglet.window.Window()
fps = pyglet.clock.ClockDisplay()
batch = pyglet.graphics.Batch()
vertex_list = batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
	[0,1,2,1,2,3],
    ('v2i', (100, 150, 100, 350, 300, 150, 300, 350)),
    ('c3B', (0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0,))
)

bin = pyglet.image.atlas.TextureBin()

path = '/'.join(sys.argv[0].rsplit('/')[:-1]) + 'assets/sliced_sprites/'

left_begin_run = [
	pyglet.image.load(path + 'left_begin_run_0.png'),
	pyglet.image.load(path + 'left_begin_run_1.png'),
	pyglet.image.load(path + 'left_begin_run_2.png'),
	pyglet.image.load(path + 'left_begin_run_3.png'),
	pyglet.image.load(path + 'left_begin_run_4.png'),
]

right_begin_run = [
	pyglet.image.load(path + 'right_begin_run_0.png'),
	pyglet.image.load(path + 'right_begin_run_1.png'),
	pyglet.image.load(path + 'right_begin_run_2.png'),
	pyglet.image.load(path + 'right_begin_run_3.png'),
	pyglet.image.load(path + 'right_begin_run_4.png'),
]

left_idle = [
	pyglet.image.load(path + 'left_idle_0.png'),
	pyglet.image.load(path + 'left_idle_1.png'),
	pyglet.image.load(path + 'left_idle_2.png'),
]

right_idle = [
	pyglet.image.load(path + 'right_idle_0.png'),
	pyglet.image.load(path + 'right_idle_1.png'),
	pyglet.image.load(path + 'right_idle_2.png'),
]

left_jump = [
	pyglet.image.load(path + 'left_jump_0.png'),
	pyglet.image.load(path + 'left_jump_1.png'),
	pyglet.image.load(path + 'left_jump_2.png'),
	pyglet.image.load(path + 'left_jump_3.png'),
	pyglet.image.load(path + 'left_jump_4.png'),
]

right_jump = [
	pyglet.image.load(path + 'right_jump_0.png'),
	pyglet.image.load(path + 'right_jump_1.png'),
	pyglet.image.load(path + 'right_jump_2.png'),
	pyglet.image.load(path + 'right_jump_3.png'),
	pyglet.image.load(path + 'right_jump_4.png'),
]

left_runloop = [
	pyglet.image.load(path + 'left_runloop_0.png'),
	pyglet.image.load(path + 'left_runloop_1.png'),
	pyglet.image.load(path + 'left_runloop_2.png'),
	pyglet.image.load(path + 'left_runloop_3.png'),
	pyglet.image.load(path + 'left_runloop_4.png'),
	pyglet.image.load(path + 'left_runloop_5.png'),
]

right_runloop = [
	pyglet.image.load(path + 'right_runloop_0.png'),
	pyglet.image.load(path + 'right_runloop_1.png'),
	pyglet.image.load(path + 'right_runloop_2.png'),
	pyglet.image.load(path + 'right_runloop_3.png'),
	pyglet.image.load(path + 'right_runloop_4.png'),
	pyglet.image.load(path + 'right_runloop_5.png'),
]

animations = [
	left_begin_run,
	right_begin_run,
	left_idle,
	right_idle,
	left_jump,
	right_jump,
	left_runloop,
	right_runloop
]

animations = [pyglet.image.Animation.from_image_sequence(images, 0.1) for images in animations]
[animation.add_to_texture_bin(bin) for animation in animations]
sprites = [pyglet.sprite.Sprite(animation) for animation in animations]
print animations
print sprites

@window.event
def on_draw():
	window.clear()

	sprites[7].draw()

	batch.draw()

	fps.draw()
	#image.blit(0,0)

# log all events (including mouse movement, which can get quite annoying)
# window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run()
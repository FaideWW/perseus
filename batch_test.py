import pyglet


window = pyglet.window.Window()


fps = pyglet.clock.ClockDisplay()

batch = pyglet.graphics.Batch()

vertex_list = batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
	[0,1,2,1,2,3],
    ('v2i', (100, 150, 100, 350, 300, 150, 300, 350)),
    ('c3B', (0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0,))
)

@window.event
def on_draw():
	window.clear()

	batch.draw()

	fps.draw()
	#image.blit(0,0)

# log all events (including mouse movement, which can get quite annoying)
# window.push_handlers(pyglet.window.event.WindowEventLogger())

pyglet.app.run()
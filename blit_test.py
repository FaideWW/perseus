import pyglet

window = pyglet.window.Window()
image = pyglet.image.Texture.create(256,128)
img1 = pyglet.image.load('bridge.png')
img2 = pyglet.image.load('bush.png')
image.blit_into(img1,0,0,0)
image.blit_into(img2,128,0,0)
@window.event
def on_draw():
    window.clear()
    image.blit(0,0)

pyglet.app.run()
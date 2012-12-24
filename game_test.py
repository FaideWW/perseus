import pyglet
from pyglet.window import key

from gameobject.gameobject import GameObject
from collision.collisionmanager import CollisionManager
from collision.axisalignedboundingbox import AxisAlignedBoundingBox
from collision.colliders import ElasticCollider
from components.forces import Gravity
import render.functions as render

window = pyglet.window.Window()

print window.get_size()[1]

cm = CollisionManager()
g = Gravity()

object1 = GameObject(0)
img1 = 'icon.png'
bb1 = AxisAlignedBoundingBox(24, 24)
cc1 = ElasticCollider(1)

object1.setSprite(img1)
object1.setBoundingBox(bb1)
object1.setCollider(cc1)
object1.setPosition(60,60)
object1.setVelocity(0,0)
object1.setSize(24,24)

floor = GameObject(1)
bb2 = AxisAlignedBoundingBox((window.get_size()[0]) / 2,10)
floor.setBoundingBox(bb2)
floor.setPosition((window.get_size()[0] / 2), 10)

img1 = pyglet.resource.image(object1.getSprite())

@window.event
def on_draw():
	window.clear()
	img1.blit(object1.getPosition().x, object1.getPosition().y)

	
	#draw separating axes
	for axis in cm.getSeparatingAxes(bb1, object1.getPosition()):
		x1 = axis.point.x
		y1 = axis.point.y
		x2 = int(axis.point.x + axis.direction.x)
		y2 = int(axis.point.y + axis.direction.y)
		print x1, y1, x2, y2
		pyglet.gl.glColor4f(0,1.0,0,1.0)
		pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x1,y1,x2,y2)))
		pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

	#draw bounding box
	v1 = object1.getBoundingVertices()
	for vertex in range(len(v1)):
		pos = object1.getPosition()
		origin = object1.getSize()
		v1[vertex] = v1[vertex] + pos + origin
		v1[vertex].x = int(v1[vertex].x)
		v1[vertex].y = int(v1[vertex].y)

	c = [1.0, 0, 0, 1.0]
	render.drawPolygonOutline(v1,c)

	#draw floor
	pyglet.gl.glColor4f(1.0,0,0,1.0)
	pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 1, 2, 3],
    ('v2i', (0, 20,
             window.get_size()[0], 20,
             0, 0,
             window.get_size()[0], 0)))

	pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

def update(dt):
	#apply gravity
	#object1.setAcceleration(object1.getAcceleration().x, g.g())
	object1.update()

	collision = cm.performSAT(bb1, bb2, object1.getPosition(), floor.getPosition())
	

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.UP:
		object1.setVelocityY(4)
	elif symbol == key.DOWN:
		object1.setVelocityY(-4)
	elif symbol == key.RIGHT:
		object1.setVelocityX(4)
	elif symbol == key.LEFT:
		object1.setVelocityX(-4)

@window.event
def on_key_release(symbol, modifiers):
	if symbol == key.UP:
		object1.setVelocityY(0)
	elif symbol == key.DOWN:
		object1.setVelocityY(0)
	elif symbol == key.RIGHT:
		object1.setVelocityX(0)
	elif symbol == key.LEFT:
		object1.setVelocityX(0)




#set the update interval to 120fps
pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
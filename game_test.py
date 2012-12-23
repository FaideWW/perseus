import pyglet
import sys
import pprint

from pyglet.window import key

pprint.pprint(sys.path)

from gameobject.gameobject import GameObject
from collision.collisionmanager import CollisionManager
from collision.axisalignedboundingbox import AxisAlignedBoundingBox
from collision.colliders import ElasticCollider

window = pyglet.window.Window()

cm = CollisionManager()


object1 = GameObject(0)
img1 = 'icon.png'
bb1 = AxisAlignedBoundingBox(24, 24)
cc1 = ElasticCollider(1)

object1.setSprite(img1)
object1.setBoundingBox(bb1)
object1.setCollider(cc1)
object1.setPosition(0,0)
object1.setVelocity(0,0)

img1 = pyglet.resource.image(object1.getSprite())

@window.event
def on_draw():
	window.clear()
	img1.blit(object1.getPosition().x, object1.getPosition().y)

def update(dt):
	object1.update()

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
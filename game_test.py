import pyglet
import time
import sys
from pyglet.window import key

from gameobject.gameobject import GameObject
from gameobject.player import Player
from collision.collisionmanager import CollisionManager
from collision.axisalignedboundingbox import AxisAlignedBoundingBox
from collision.colliders import ElasticCollider
from components.coordinate import Coordinate
from components.vector import Vector
from components.forces import Gravity
from render.functions import Renderer
from maps.maps import Map


window = pyglet.window.Window()

window_res = Vector(window.get_size())

print window_res

movementSpeed = 4
fps = pyglet.clock.ClockDisplay()
render = Renderer()

mapPath = '/'.join(sys.argv[0].rsplit('/')[:-1])
m = Map(mapPath + '/maps/map1')


cm = CollisionManager()
g = Gravity()

player = Player(0)
img1 = 'icon.png'
bb1 = AxisAlignedBoundingBox(24, 24)
cc1 = ElasticCollider(1)

player.setSprite(img1)
player.setBoundingBox(bb1)
player.setCollider(cc1)
player.setPosition(100,100)
player.setVelocity(0,0)
player.setSize(48,48)

floor = GameObject(1)
bb2 = AxisAlignedBoundingBox((window.get_size()[0]) / 2,10)
floor.setBoundingBox(bb2)
floor.setPosition(0,0)
floor.setSize(window.get_size()[0], 20)

img1 = pyglet.resource.image(player.getSprite())

vec1 = Vector([0,0])

ob1Pos = pyglet.text.Label(str(player.getPosition()),
	font_name='Times New Roman',
	font_size=12,
	x=player.getPosition().x, y=player.getPosition().y,
	anchor_x='center', anchor_y='center')

m = render.prepareMap(m, window_res, [1.0,1.0,1.0,1.0])

@window.event
def on_draw():
	window.clear()

	render.batcher.draw()
	img1.blit(player.getPosition().x, player.getPosition().y)
	#draw floor
	pyglet.gl.glColor4f(1.0,0,0,1.0)
	pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 1, 2, 3],
    ('v2i', (floor.getPosition().x - floor.getSize().x, 20,
            floor.getPosition().x + floor.getSize().x, 20,
             0, 0,
             floor.getPosition().x + floor.getSize().x, 0)))

	pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)
	#draw separating axes
	for axis in cm.getSeparatingAxes(bb1):
		origin = player.getWorldPosition()
		render.drawVector(axis, origin, [0,1.0,0,1.0])

	for axis in cm.getSeparatingAxes(bb2):
		origin = floor.getWorldPosition()
		render.drawVector(axis, origin, [0,1.0,0,1.0])

	#get separation
	separatingVector = player.getWorldPosition() - floor.getWorldPosition()
	
	#draw projections
	for axis in cm.getSeparatingAxes(bb2):
		projection = separatingVector.project(axis)
		projectedVector = axis.normalize() * projection
		#render.drawVector(projectedVector, floor.getWorldPosition(), [1.0,0,1.0,1.0])	



	render.renderAll()

	fps.draw()


	#draw player info


def genVectorLabel(vector, origin, x='left', y='top'):
	label = pyglet.text.Label(str(vector),
	font_name='Times New Roman',
	font_size=12,
	x=(origin + vector / 2).x, y=(origin + vector / 2).y,
	anchor_x=x, anchor_y=y)
	return label



def update(dt):
	#apply gravity

	player.update(dt)
	collision = cm.performSAT(bb2, bb1, floor.getWorldPosition(), (player.getWorldPosition() + player.getActualVelocityVector()), render)

	if collision != -1:
		player.land()


@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.UP:
		player.jump()
	elif symbol == key.RIGHT:
		player.move([movementSpeed,0])
	elif symbol == key.LEFT:
		player.move([-movementSpeed,0])

@window.event
def on_key_release(symbol, modifiers):
	if symbol == key.DOWN:
		player.move([0,movementSpeed])
	elif symbol == key.RIGHT:
		player.move([-movementSpeed,0])
	elif symbol == key.LEFT:
		player.move([movementSpeed,0])




#set the update interval to 120fps
pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
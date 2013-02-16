import pyglet
import time
import sys

import animation.animation as animation
import collision.collision as collision
import camera.camera as camera
import component.component as component
import gameobject.gameobject as gameobject
import render.render as render

window = pyglet.window.Window()

window_res = component.Vector(window.get_size())

print window_res

fps = pyglet.clock.ClockDisplay()
last_frame = pyglet.clock.tick()
r = render.Render()
c = camera.Camera(component.Vector(window_res))
c.setPosition(component.Position.zero())
r.setCamera(c)
asset_path = '/'.join(sys.argv[0].rsplit('/')[:-1]) + 'assets/'
walk_sheet = asset_path + 'player/walk_sheet.png'
walk_info = asset_path + 'player/walk_sheet.tile'

player_size = component.Vector([72,93])

a = animation.Animation(walk_sheet, walk_info, 1)
b = collision.BoundingPoly.fromSize(player_size)
o = player_size / 2
p = component.Position([50,50])

g = gameobject.GameObject(
    id=0, 
    position=p, 
    boundingpoly=b,
    collider=collision.PlayerCollidable(),
    type='Player',
    sprite=a,
    size=player_size,
    origin=o)

g.showBoundingPoly()
r.addToBatch(g.getRenderables())
print pyglet.window.get_platform().get_default_display().get_default_screen()

@window.event
def on_draw():
    window.clear()
    fps.draw()
    this_frame = pyglet.clock.tick()
    try:
        dt = this_frame - last_frame
    except UnboundLocalError:
        dt = this_frame


    r.draw(dt)


    last_frame = this_frame


def update(dt):
    dt *= 1000
    a.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
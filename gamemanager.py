import pyglet
import sys

import animation.animation as animation
import collision.collision
import collision.collider
import camera.camera as camera
import component.component as component
import component.unit as unit
import gameobject.player
import render.render as render
import maps.map as maps
import playercontroller.playercontroller as playercontroller

window = pyglet.window.Window()

unit.Unit.ppu = 70

window_res = unit.Unit.toUnits(component.Vector(window.get_size()))


fps = pyglet.clock.ClockDisplay()
last_frame = pyglet.clock.tick()
r = render.Render()
print window_res
c = camera.Camera(component.Vector(window_res), id='cam1')
r.setCamera(c)
file_path = '/'.join(sys.argv[0].split('/')[:-1])
print file_path
asset_path = '/'.join([file_path, 'assets/'])
asset_path2 = ''.join([file_path, 'assets/'])
walk_sheet = asset_path + 'player/walk_sheet.png'
walk_info = asset_path + 'player/walk_sheet.tile'

#obviously this only contains one tile

player_size = unit.Unit.toUnits(component.Vector([72, 93]))

print 'psize', player_size
try:
    a = animation.Animation(walk_sheet, walk_info, 20)
except IOError, e:
    asset_path = asset_path2
    walk_sheet = asset_path + 'player/walk_sheet.png'
    walk_info = asset_path + 'player/walk_sheet.tile'
    a = animation.Animation(walk_sheet, walk_info, 20)

map_sheet = asset_path + 'maps/map1.map'
map_tiles = asset_path + 'png/block.png'
map_info = asset_path + 'maps/map1.td'
print walk_sheet, walk_info, map_sheet

b = collision.collision.BoundingPoly.fromSize(player_size / 2)
o = player_size / 2
p = component.Position([2, 2])

c.setPosition(p)

g = gameobject.player.Player(
    id=0,
    position=p,
    boundingpoly=b,
    collider=collision.collision.PlayerCollidable(),
    type='Player',
    sprite=a,
    size=player_size,
    origin=o)

pc = playercontroller.PlayerController(g)

#c.setTarget(g);
print c.getWorldSpacePosition()
print g.getWorldSpacePosition()
g.showBoundingPoly()
print g.getToRender()
g.addRenderables(r.generateRenderables(g.getToRender()))
print pyglet.window.get_platform().get_default_display().get_default_screen()

m = maps.Map(map_sheet, map_tiles, map_info, component.Vector([1, 1]))
#print m
r.addToBlit(m.mapAsSprite())
print g.getRenderables()

cd = collision.collider.Collider(unit.Unit.ppu)

objs = m.getTileList()
for o in objs:
    o.showBoundingPoly(r)
objs.append(g)
last_frame = 0


@window.event
def on_draw():
    window.clear()
    this_frame = pyglet.clock.tick()
    try:
        dt = this_frame - last_frame
    except UnboundLocalError:
        dt = this_frame

    r.draw(dt)

    last_frame = this_frame

    fps.draw()


@window.event
def on_key_press(symbol, modifiers):
    pc.keyDown(symbol)


@window.event
def on_key_release(symbol, modifiers):
    pc.keyUp(symbol)

gravity = component.Velocity([0, -2])

key_state = pyglet.window.key.KeyStateHandler()
window.push_handlers(key_state)


def update(dt):

    pc.update(dt, key_state)
    g.accelerate(gravity)

    cd.detectCollisions(objs, m, dt)
    cd.resolveCollisions(cd.collision_queue, dt)

    g.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()

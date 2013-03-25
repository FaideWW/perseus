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
c = camera.Camera(component.Vector(window_res))
r.setCamera(c)
asset_path = '/'.join(sys.argv[0].rsplit('/')[:-1]) + 'assets/'
walk_sheet = asset_path + 'player/walk_sheet.png'
walk_info = asset_path + 'player/walk_sheet.tile'
map_sheet = asset_path + 'maps/map1.map'

#obviously this only contains one tile
map_tiles = asset_path + 'png/block.png'

map_info = asset_path + 'maps/map1.td'

player_size = unit.Unit.toUnits(component.Vector([72, 93]))

print 'psize', player_size
a = animation.Animation(walk_sheet, walk_info, 20)
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

cd = collision.collider.Collider()

objs = m.getTileList()
for o in objs:
    o.showBoundingPoly(r)
objs.append(g)

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


def update(dt):
    g.update(dt)
    cd.detectCollisions(objs, m)
    cd.resolveCollisions(cd.collision_queue)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()

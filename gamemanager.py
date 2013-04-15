import pyglet
import sys

import animation.animation as animation
import animation.animationfactory as animationfactory
import collision.collision
import collision.collider
import camera.camera as camera
import component.component as component
import component.unit as unit
import gameobject.player
import render.render as render
import maps.map as maps
import playercontroller.playercontroller as playercontroller

EXEC_MODE_DEBUG = False

window = pyglet.window.Window()

unit.Unit.ppu = 70

window_res = unit.Unit.toUnits(component.Vector(window.get_size()))

pyglet.gl.glClearColor(1, 1, 1, 1)

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

player_tilesheet = 'player/prototype1_character_sheet.png'
player_idle_info = 'player/prototype1_character_idle.tile'
player_lwalk_info = 'player/prototype1_character_lwalk.tile'
player_rwalk_info = 'player/prototype1_character_rwalk.tile'
walk_sheet = asset_path + 'player/walk_sheet.png'
walk_info = asset_path + 'player/walk_sheet.tile'

#obviously this only contains one tile

player_size = unit.Unit.toUnits(component.Vector([64, 64]))

#test the animation factory
af = animationfactory.AnimationFactory(asset_path, player_tilesheet)
new_player_idle = af.makeAnimation(0, player_rwalk_info)

print 'psize', player_size
try:
    a = animation.Animation(walk_sheet, walk_info)
except IOError, e:
    asset_path = asset_path2
    walk_sheet = asset_path + 'player/walk_sheet.png'
    walk_info = asset_path + 'player/walk_sheet.tile'
    a = animation.Animation(walk_sheet, walk_info)

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
    sprite=new_player_idle,
    size=player_size,
    origin=o)

pc = playercontroller.PlayerController(g)

#c.setTarget(g);
print c.getWorldSpacePosition()
print g.getWorldSpacePosition()
if EXEC_MODE_DEBUG:
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
if EXEC_MODE_DEBUG:
    for o in objs:
        o.showBoundingPoly(r)
objs.append(g)
last_frame = 0

debug_info = pyglet.text.Label()
player_info = pyglet.text.Label()

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

    debug_info.draw()
    player_info.draw()

    fps.draw()


@window.event
def on_key_press(symbol, modifiers):
    pc.keyDown(symbol)


@window.event
def on_key_release(symbol, modifiers):
    pc.keyUp(symbol)

gravity = component.Velocity([0, -3])

key_state = pyglet.window.key.KeyStateHandler()
window.push_handlers(key_state)


def update(dt):

    pc.update(dt, key_state)
    g.gravity(gravity)

    cd.detectCollisions(objs, m, dt)
    cd.resolveCollisions(cd.collision_queue, dt)

    g.update(dt)

    if EXEC_MODE_DEBUG:
        debug_info.text = 'Objects:' + str(len(r.getVertexList()))
        debug_info.text += ' Collisions:' + str(len(cd.collision_queue))
        debug_info.text += ' Player state:' + g.getMovementState()

        player_info.text = str(g.getWorldSpacePosition())
        player_info.x = unit.Unit.toPixels(g.getWorldSpacePosition().x)
        player_info.y = unit.Unit.toPixels(g.getWorldSpacePosition().y)


pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()

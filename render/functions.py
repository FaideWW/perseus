import pyglet.gl
import pyglet.graphics

def drawPolygonOutline(vertices, color):
	pyglet.gl.glColor4f(color[0], color[1],color[2],color[3])
	for p in range(len(vertices)):
		n = p + 1
		if n == len(vertices):
			n = 0
		point = vertices[p]
		next = vertices[n]
		pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (point.x, point.y, next.x, next.y)))
	pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)
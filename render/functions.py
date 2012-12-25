import pyglet.gl
import pyglet.graphics

from components.coordinate import Coordinate

class Renderer(object):

	def __init__(self):
		self.renderQueue = []

	def drawPolygonOutline(self, vertices, color):
		for p in range(len(vertices)):
			n = p + 1
			if n == len(vertices):
				n = 0
			point = vertices[p]
			next = vertices[n]
			self.renderQueue.append([color, 2, pyglet.gl.GL_LINES, ('v2f', (point.x, point.y, next.x, next.y))])
			#pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (point.x, point.y, next.x, next.y)))

		return len(self.renderQueue)

	def drawVector(self, vector, origin = Coordinate([0,0,0]), color = [1.0,1.0,1.0,1.0]):
		self.renderQueue.append([color, 2, pyglet.gl.GL_LINES, ('v2f', (origin.x, origin.y, origin.x + vector.x, origin.y + vector.y))])
		#pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (origin.x, origin.y, origin.x + vector.x, origin.y + vector.y)))
		return len(self.renderQueue)

	def setColor(self, color):
		pyglet.gl.glColor4f(color[0], color[1], color[2], color[3])

	def resetColor(self):
		pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

	def renderAll(self):
		for job in self.renderQueue:
			self.setColor(job[0])
			pyglet.graphics.draw(job[1], job[2], job[3])
			self.resetColor()
		self.renderQueue = []

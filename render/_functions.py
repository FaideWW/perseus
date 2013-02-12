import pyglet.gl
import pyglet.graphics

from components.coordinate import Coordinate

class Renderer(object):

	def __init__(self):
		self.renderQueue = []
		self.batcher = pyglet.graphics.Batch()

	def drawPolygonOutline(self, vertices, color):
		for p in range(len(vertices)):
			n = p + 1
			if n == len(vertices):
				n = 0
			point = vertices[p]
			next = vertices[n]
			self.renderQueue.append(['draw', color, 2, pyglet.gl.GL_LINES, ('v2f', (point.x, point.y, next.x, next.y))])
			#pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (point.x, point.y, next.x, next.y)))

		return len(self.renderQueue)

	def drawVector(self, vector, origin = Coordinate([0,0,0]), color = [1.0,1.0,1.0,1.0]):
		self.renderQueue.append(['draw', color, 2, pyglet.gl.GL_LINES, ('v2f', (origin.x, origin.y, origin.x + vector.x, origin.y + vector.y))])
		#pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (origin.x, origin.y, origin.x + vector.x, origin.y + vector.y)))
		return len(self.renderQueue)

	def drawTile(self, tile, position, tileSize, color):
		#print tile.tiletype
		if tile.tiletype == 'none':
			return
			
		print tile.tiletype, tile.char, position, tileSize
		pyglet.graphics.draw_indexed(
			4, 
			pyglet.gl.GL_TRIANGLES, 
			[0,1,2,1,2,3], 
			('v2i', 
				(position.x, position.y,
				position.x + tileSize.x, position.y,
				position.x, position.y + tileSize.y,
				position.x + tileSize.x, position.y + tileSize.y)))
		
	def drawMap(self, tilemap, window_res, color):
		tileSize = Coordinate([window_res.x / tilemap.width, window_res.y / tilemap.height])
		pyglet.gl.glColor4f(0,1.0,0,1.0)
		tile_x = 0
		tile_y = 0

		for tilerow in tilemap.mapData:
			for tile in tilerow:
				tilepos = Coordinate([tile_x * tileSize.x, tile_y * tileSize.y])
				self.drawTile(tile, tilepos, tileSize, color)
				tile_x += 1
			tile_x = 0
			tile_y += 1
		pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

	def prepareMap(self, tilemap, window_res, color):
		""" Index all of the map data and add it to the batch """
		tileSize = Coordinate([window_res.x / tilemap.width, window_res.y / tilemap.height])
		tile_x = 0
		tile_y = 0

		for tilerow in tilemap.mapData:
			for tile in tilerow:
				tilepos = Coordinate([tile_x * tileSize.x, tile_y * tileSize.y])
				if tile.tiletype != 'none':
					tilemap.mapIndex[tile_y][tile_x] = self.batcher.add_indexed(
						4, 
						pyglet.gl.GL_TRIANGLES, 
						None,
						[0,1,2,1,2,3], 
						('v2i', 
							(tilepos.x, tilepos.y,
							tilepos.x + tileSize.x, tilepos.y,
							tilepos.x, tilepos.y + tileSize.y,
							tilepos.x + tileSize.x, tilepos.y + tileSize.y)),
						('c3B', (50,0,0,50,0,0,50,0,0,50,0,0,))
						)
				tile_x += 1
			tile_x = 0
			tile_y += 1

		return tilemap

	def setColor(self, color):
		pyglet.gl.glColor4f(color[0], color[1], color[2], color[3])

	def resetColor(self):
		pyglet.gl.glColor4f(1.0,1.0,1.0,1.0)

	def renderAll(self, cam=None):
		if cam != None:
			x = cam.translateToCamSpace(Coordinate.zero()).x
			y = cam.translateToCamSpace(Coordinate.zero()).y
			z = 0
		else:
			x = 0
			y = 0
			z = 0
		pyglet.gl.glPushMatrix()
		pyglet.gl.glTranslatef(x, y, z)
		for job in self.renderQueue:
		 	self.setColor(job[1])
		 	if job[0] == 'draw':
		 		pyglet.graphics.draw(job[2], job[3], job[4])
		 	self.resetColor()
		self.batcher.draw()
		self.renderQueue = []
		pyglet.gl.glPopMatrix()
		glTranslatef()
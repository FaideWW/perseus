from components.position import Position
from components.velocity import Velocity
import math

class GameObject:
	def __init__(self, global_id):
		self.gid = global_id
		self.pos = Position(0,0)
		self.vel = Velocity(0,0)
		self.acc = Velocity(0,0)
		#terminal velocity from gravity
		self.termV = -20

		self.size = Position(0,0)

	def initialize(self, img_path, boundingbox, collider):
		#not sure if I actually need this function.
		#probably not, it's mostly for convenience
		#maybe in the future for modding, etc...
		pass

	def setSize(self, x, y):
		self.size = Position(x, y)

	def getSize(self):
		return self.size

	def setSprite(self, img_path):
		self.sprite = img_path

	def getSprite(self):
		return self.sprite

	def setBoundingBox(self, boundingbox):
		self.bounding_box = boundingbox

	def getBoundingBox(self):
		return self.boundingbox

	def getBoundingVertices(self):
		return self.bounding_box.getVertices()

	def setCollider(self, collider):
		self.collider = collider

	def getCollider(self):
		return self.collider

	def getPosition(self):
		return self.pos

	def setPosition(self, x, y, z=0):
		return self.pos.set(x, y, z)

	def getVelocity(self):
		return self.vel

	def setVelocity(self, x, y):
		if self.vel.y < self.termV:
			y = self.termV
		return self.vel.set(x, y, 0)

	def setVelocityX(self, x):
		return self.setVelocity(x, self.getVelocity().y)

	def setVelocityY(self, y):
		return self.setVelocity(self.getVelocity().x, y)

	def getID(self):
		return self.gid

	def getAcceleration(self):
		return self.acc

	def setAcceleration(self, x, y):
		return self.acc.set(x, y)

	def update(self):
		#acceleration first
		self.vel += self.acc

		#then position
		self.pos += self.vel
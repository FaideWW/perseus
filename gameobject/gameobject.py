from components.position import Position
from components.velocity import Velocity
import math

class GameObject(object):
	def __init__(self, global_id):
		self.gid = global_id
		self.pos = Position([0,0])
		self.vel = Velocity([0,0])
		self.acc = Velocity([0,0])
		#terminal velocity from gravity
		self.termV = -20
		self.max_speed = 4

		self.size = Position([0,0])

	def initialize(self, img_path, boundingbox, collider):
		#not sure if I actually need this function.
		#probably not, it's mostly for convenience
		#maybe in the future for modding, etc...
		pass

	def setSize(self, x, y):
		self.size = Position([x, y])

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

	def getWorldPosition(self):
		return self.pos + (self.size / 2)

	def setPosition(self, x, y, z=0):
		self.pos = Position([x,y,z])

	def getVelocityVector(self):
		return self.vel

	def getActualVelocityVector(self):
		if self.vel.mag() > self.max_speed:
			return self.vel.normalize() * self.max_speed
		else:
			return self.vel

	def setVelocity(self, x, y):
		if self.vel.y < self.termV:
			y = self.termV
		self.vel = Velocity([x,y])

	def setVelocityX(self, x):
		return self.setVelocity(x, self.getVelocityVector().y)

	def setVelocityY(self, y):
		return self.setVelocity(self.getVelocityVector().x, y)

	def addVelocity(self, x, y):
		if self.vel.y < self.termV:
			y = self.termV
		self.vel += Velocity([x, y])

	def addVelocityX(self, x):
		return self.addVelocity(x, 0)

	def addVelocityY(self, y):
		return self.addVelocity(0, y)

	def getID(self):
		return self.gid

	def getAcceleration(self):
		return self.acc

	def setAcceleration(self, acc):
		self.acc = Velocity(acc)

	def update(self):
		#acceleration first
		self.vel += self.acc

		if self.vel.mag() > self.max_speed:
			#cap speed at the predefined value
			v = self.vel.normalize() * self.max_speed
		else:
			v = self.vel

		#then position
		self.pos += v

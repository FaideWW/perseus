from components import Position
import math

class GameObject:
	self.gid
	self.pos
	self.sprite
	self.animation_state
	self.bounding_box
	self.collider

	def __init__(self, global_id):
		self.gid = global_id
		self.pos = Position()

	def initialize(self, img_path, boundingbox, collider):
		pass

	def setSprite(self, img_path):
		self.sprite = img_path

	def getSprite(self):
		return self.sprite

	def setBoundingBox(self, boundingbox):
		self.bounding_box = boundingbox

	def getBoundingBox(self):
		return self.boundingbox

	def setCollider(self, collider):
		self.collider = collider

	def getCollider(self):
		return self.collider

	def move(self, direction, velocity):
		""" 
			Move the object (direction is degrees with 0 pointing east and moving 
			anticlockwise) and return its new position. 

			To do this we construct a right triangle with hypotenuse 'velocity' and 
			move along the perimeter 'direction' degrees, then using trigonometry,
			calculate the x and y components of the move.
		"""
		rad_dir = math.radians(direction)
		x = velocity * math.cos(rad_dir)
		y = velocity * math.sin(rad_dir)

		return self.pos.rel(x, y)

	def getPosition(self):
		return self.pos

	def setPosition(self, x, y, z=0):
		return self.pos.abs(x, y, z)

	def getID(self):
		return self.gid


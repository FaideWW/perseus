import gameobject
from components.forces import Gravity

class Player(gameobject.GameObject):
	max_speed = 4

	def __init__(self, gid):
		super(Player, self).__init__(gid)
		self.onGround = False
		self.g = Gravity()

	def move(self, movement_vector):
		self.vel += movement_vector

	def land(self):
		self.setAcceleration([self.getAcceleration().x, 0])
		self.vel.y = 0
		self.onGround = True

	def jump(self):
		if self.onGround:
			self.addVelocityY(5)
			self.onGround = False

	def update(self, dt):
		if not self.onGround:
			self.setAcceleration([self.getAcceleration().x, self.g.g()])
		else:
			self.setAcceleration([self.getAcceleration().x, 0])
		#acceleration first
		self.vel += self.acc

		# if self.vel.mag() > self.max_speed:
		# 	#cap speed at the predefined value
		# 	v = self.vel.normalize() * self.max_speed
		# else:
		# 	v = self.vel

		v = self.vel

		if self.onGround:
			self.setVelocityY(0)
			v.y = 0

		#then position
		self.pos += v

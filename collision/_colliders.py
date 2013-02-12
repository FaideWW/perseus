import math

from components.velocity import Velocity

class Collider:
	""" 
		Collider interface class.  Defines behavior for an object as it experiences a
		collision.
	"""
	def __init__(self):
		pass

	def collide(self, collisionAngle, velocity):
		raise NotImplementedError('Collider type is an interface')


class ElasticCollider(Collider):

	def __init__(self, bF=1):
		self.bounceFactor = bF

	def collide(self, collisionAngle, velocity):
		""" 
			Behaves like a bouncing ball; velocity parallel to the 
			collision is reversed. 
		"""

		#to simplify this we'll rotate the velocity vectors to
		# the collision angle's frame of reference (so the angle
		# will be 0), then perform the collision and rotate back

		collisionAngle = math.radians(collisionAngle % 360)

		if collisionAngle != 0:
			x = velocity.x * math.cos(collisionAngle) - velocity.y * math.sin(collisionAngle)
			y = velocity.x * math.sin(collisionAngle) + velocity.y * math.cos(collisionAngle)
		
			y *= bF * -1

			velocity.x = x * math.cos(collisionAngle*-1) - y * math.sin(collisionAngle*-1)
			velocity.y = x * math.sin(collisionAngle*-1) + y * math.cos(collisionAngle*-1)

		else:
			velocity.y *= bF * -1

		return velocity
		
class PlayerCollider(Collider):
	""" Player specific collision mechanics"""
	def __init__(self):
		pass

	def collide(self, collisionAngle, velocity):
		"""
			For now we're just copy-pasting the behavior from elastic collisions but 
			instead of reflecting velocity we stop it in the perpendicular direction
		"""

		collisionAngle = math.radians(collisionAngle % 360)

		if collisionAngle != 0:
			x = velocity.x * math.cos(collisionAngle) - velocity.y * math.sin(collisionAngle)
			y = velocity.x * math.sin(collisionAngle) + velocity.y * math.cos(collisionAngle)
		
			y = 0

			velocity.x = x * math.cos(collisionAngle*-1) - y * math.sin(collisionAngle*-1)
			velocity.y = x * math.sin(collisionAngle*-1) + y * math.cos(collisionAngle*-1)

		else:
			velocity.y = 0

		return velocity
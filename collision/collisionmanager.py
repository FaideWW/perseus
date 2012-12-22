import math

import AxisAlignedBoundingBox
import BoundingSphere
from gameobject import GameObject

class CollisionManager:
	self.boundingArray

	def __init__(self):
		self.boundingArray = 
		[
			'none'
			'aabb',
			'sphere'
		]

	def checkForCollision(self, o1, o2):
		t1 = 0
		t2 = 0

		for type in range(len(boundingArray)):
			if o1.getBoundingBox().getBoundType == boundingArray[type]:
				t1 = type
			if o2.getBoundingBox()getBoundType == boundingArray[type]:
				t2 = type

		if t1 == 0 or t2 == 0:
			return false

		return __collisionMap(o1, o2, t1, t2)

	def __collisionMap(self, o1, o2, t1, t2):
		""" 
			Perform the collision detection 

			Note that because collisions are commutative (A collides 
			with B = B collides with A) we do a little shuffling to 
			ensure that the object higher in the array,	i.e. the newer 
			bounder, masters the collision here because the flow statement
			is simpler this way
		"""

		if t1 >= t2:
			bounder1 = o1.getBoundingBox()
			bounder2 = o2.getBoundingBox()
			pos1 = o1.getPosition()
			pos2 = o2.getPosition()
		else:
			bounder1 = o2
			bounder2 = o1
			pos1 = o2.getPosition()
			pos2 = o1.getPosition()

		# incoming huge switch statement (or Py equivalent)
		# there's probably a better way to do this...

		if bounder1.getBoundType() == 'aabb':
			""" AABB """

			if bounder2.getBoundType() == 'aabb':
				"""AABB collides with AABB"""
				#aka "The Fast and Loose version"
				#if the centers of the boxes intersect on both axes,
				# there is a collision. (edge-unaware)

				return math.abs(pos1.x - pos2.x) < (bounder1.half_width + bounder2.half_width) and math.abs(pos1.y - pos2.y) < (bounder1.half_height + bounder2.half_height)
			
		elif bounder1.getBoundType() == 'sphere':
			""" Sphere """
			if bounder2.getBoundType() == 'aabb':
				"""Sphere collides with AABB"""
				#get the square of the sqdistance from the box's closest 
				# edge to the center of the sphere
				#if the sphere's radius squared is greater than sqdist^2,
				# there is a collision 
				#via Pythagorean theorem

				sqdist = 0

				if pos1.x < pos2.x - bounder2.half_width:
					#sphere is to the left of box
					s = pos1.x - (pos2.x - bounder2.half_width)
				elif pos1.x > pos2.x + bounder2.half_width:
					#sphere is to the right of box
					s = pos1.x - (pos2.x + bounder2.half_width)
				sqdist += s*s

				if pos1.y < pos2.y - bounder2.half_height:
					#sphere is below box
					s = pos1.y - (pos2.y - bounder2.half_height)
				elif pos1.y > pos2.y + bounder2.half_height:
					#sphere is above box
					s = pos1.y - (pos2.y + bounder2.half_height)
				sqdist += s*s

				return bounder1.radius**2 >= sqdist
			
			elif bounder2.getBoundType == 'sphere':
				"""Sphere collides with Sphere"""
				#if distance between centers (via Pythagoras) is
				# less than the sum of radii, there is a collision

				sqdist = math.abs(pos1.x - pos2.x)**2 + math.abs(pos1.y - pos2.y)**2
				return (bounder1.radius + bounder2.radius)**2 >= sqdist

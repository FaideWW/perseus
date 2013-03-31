import math

from axisalignedboundingbox import AxisAlignedBoundingBox
from boundingsphere import BoundingSphere
from gameobject.gameobject import GameObject
from components.vector import Vector
from components.position import Ray

import render.functions as render

class CollisionManager:
	def __init__(self):
		self.boundingArray = [
			'none',
			'aabb',
			'polygon',
			'sphere'
		]

		self.bounderShapes = [
			'convex',
			'concave'
		]

	def sweepCollisionTest(self, bb1, bb2, p1, p2, v1, v2):
		""" 
			Where p1 and p2 are position vectors 
			and v1 and v2 are velocity vectors

			NOTE: sweep tests are only supported for 
			AABB-AABB.  SAT sweeps are a little outside my 
			expertise.
		"""
		type1 = 0
		type2 = 0

		for type in range(len(self.boundingArray)):
			if bb1.getBoundType == self.boundingArray[type]:
				type1 = type
			if bb1.getBoundType == self.boundingArray[type]:
				type2 = type

		if type1 == 1 and type2 == 1:
			"""Simple AABB collision"""

			#bb1 controls the collision: translate movement to bb2's frame of reference

			rvel = v1 - v2

			#sweep for a collision

			#check x path
			if rvel.x != 0:
				t_min_x = ((p2.x - bb2.half_width) - p1.x) / rvel.x
				t_max_x = ((p2.x + bb2.half_width) - p1.x) / rvel.x
			else:
				if (p2.x - bb2.half_width) <= (p1.x + bb1.half_width) or (p2.x + bb2.half_width) >= (p1.x - bb1.half_width):
					#if they have the same x velocity but still intersect on the x axis...
					t_min_x = t_max_x = 0
				else:
					t_min_x = 2
					t_max_x = -2

			#check y path
			if rvel.y != 0:
				t_min_y = ((p2.y - bb2.half_height) - p1.y) / rvel.y
				t_max_y = ((p2.y + bb2.half_height) - p1.y) / rvel.y
			else:
				if (p2.y - bb2.half_height) <= (p1.y + bb1.half_height) or (p2.y + bb2.half_height) >= (p1.y - bb1.half_height):
					#if they have the same x velocity but still intersect on the x axis...
					t_min_y = t_max_y = 0
				else:
					t_min_y = 2
					t_max_y = -2

			if t_min_x <= t_max_x and t_min_y <= t_max_y:
				intersect_time = math.max(t_min_x, t_min_y)
			else:
				intersect_time = -1
			return intersect_time				

		else:
			raise TypeError('Sweep tests are not supported for non-AABB collisions')

	def checkForCollision(self, o1, o2):
		t1 = 0
		t2 = 0

		for type in range(len(self.boundingArray)):
			if o1.getBoundingBox().getBoundType == self.boundingArray[type]:
				t1 = type
			if o2.getBoundingBox().getBoundType == self.boundingArray[type]:
				t2 = type

		if t1 == 0 or t2 == 0:
			return False

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
	def performSAT(self, bb1, bb2, origin1, origin2, r):
		"""
			Separating axis theorem:
			determines overlap between two convex polygons and on which faces
			(for concave polygons see pointInPoly())

			Procedure:
				for every separating axis in bb1:
					for every vertex in bb1:
						project the vertex onto the axis
						if the vertex is an extrema, save it as max or min
					repeat for bb2
					if bb1.max < bb2.min or bb1.min > bb2.max (aka the projections do not overlap):
						return False
					else
						if the overlap is smaller than the previous overlap save as collision_axis
						continue
				if this point is reached there is a collision on collision_axis
		"""
		collision_axis = 0
		collision_depth = -1
		axes = self.getSeparatingAxes(bb1)
		for i in range(len(axes)):
			axis = axes[i]
			projections = []
			for vertex in bb1.getVertices():

				projection_point = (vertex).scalar_project(axis)
				projections.append(projection_point)
			bb1_min = min(projections)
			bb1_max = max(projections)


			projections = []
			for vertex in bb2.getVertices():
				projection_point = (vertex + origin2 - origin1).scalar_project(axis)
				projections.append(projection_point)
				r.drawVector(axis.normalize() * projection_point, (origin1))
			bb2_min = min(projections)
			bb2_max = max(projections)

			if bb1_max < bb2_min or bb1_min > bb2_max:
				#no collision
				return -1
			else:
				if bb1_max > bb2_max:
					overlap = ((bb1_max - bb1_min) + (bb2_max - bb2_min)) - (bb1_max - bb2_min)
				else:
					overlap = ((bb1_max - bb1_min) + (bb2_max - bb2_min)) - (bb2_max - bb1_min)
				if overlap < collision_depth or collision_depth == -1:
					collision_axis = i
					collision_depth = overlap
		return i



		
	def getSeparatingAxes(self, boundingbox):
		vertices = boundingbox.getVertices()
		axes = []
		for vec in range(len(vertices)):
			n = vec + 1
			if n == len(vertices):
				n = 0
			v = (vertices[vec] - vertices[n]).rot(90)

			#check if we have two of the same axis (always the case with parallelograms)
			hasAxis = False
			for x in axes:
				if v.isParallel(x):
					hasAxis = True
			if not hasAxis:
				axes.append(v)

		return axes
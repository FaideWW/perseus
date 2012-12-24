import math

from axisalignedboundingbox import AxisAlignedBoundingBox
from boundingsphere import BoundingSphere
from gameobject.gameobject import GameObject
from components.vector import Vec2

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

	def performSAT(self, bb1, bb2, p1, p2):
		if bb1.getBoundShape() != 'convex' or bb2.getBoundShape() != 'convex':
			raise TypeError('SAT collision detection is invalid for non-convex shapes')

		if bb1.getBoundType() == 'sphere' or bb2.getBoundType == 'sphere':
			#special case for spheres
			pass
		else:

			print 'bb1:', bb1
			print 'bb2:', bb2
			print 'p1:', p1
			print 'p2:', p2



			#check for the less complex shape to be the collider
			if len(bb1.getVertices()) <= len(bb1.getVertices()):
				collider = bb1.getVertices()
				collider_p = p1
				collidee = bb2.getVertices()
				collidee_p = p2
			else:
				collider = bb2.getVertices()
				collider_p = p2
				collidee = bb1.getVertices()
				collidee_p = p1

			# frame bounding objects in world space
			# also generate vectors for separating axes

			
			axes = []
			next = 0
			
			for vertex in range(len(collider)):
				collider[vertex] += collider_p
				next = vertex + 1								
				if next == len(collider): 					
					next = 0					
					dir_to_next = collider[next] - collider[vertex]
				else:
					dir_to_next = collider[next]
				vec = Vec2(collider[vertex], dir_to_next)
				axes.append(vec.rotate(90))
			for vertex in range(len(collidee)):
				collidee[vertex] += collidee_p
			print 'collider:'
			for x in collider:
				print x
			print 'collidee:'
			for x in collidee:
				print x


			collision_axis = -1
			last_depth = -1
			for i in range(len(axes)):
				#project both bounding objects onto axis to obtain projection vector
				#if projection vectors overlap, continue
				#if projection vectors do not overlap, exit.  there is no collision
				#if all projection vectors overlap, we have a collision

				axis = axes[i]
				collider_vector_min = collider_vector_max = collidee_vector_min = collidee_vector_max = -1

				for point in collider:
					#get the dot product of point and axis to find its projection
					
					axisPos = point.x * axis.direction.x + point.y * axis.direction.y

					if collider_vector_min == -1 and collider_vector_max == -1:
						#first point
						collider_vector_min = collider_vector_max = axisPos
					elif axisPos < collider_vector_min:
						#new min
						collider_vector_min = axisPos
					elif axisPos > collider_vector_max:
						#new max
						collider_vector_max = axisPos

				for point in collidee:
					#same drill as before
					axisPos = point.x * axis.direction.x + point.y * axis.direction.y
					if collidee_vector_min == -1 and collidee_vector_max == -1:
						collidee_vector_min = collidee_vector_max = axisPos
					elif axisPos < collidee_vector_min:
						collider_vector_min = axisPos
					elif axisPos > collidee_vector_max:
						collidee_vector_max = axisPos

				#check for a lack of overlap
				if collider_vector_min < collidee_vector_max and collider_vector_max > collidee_vector_min:
					#there's no intersection along this axis; therefore no collision
					break
				else:
					#determine the depth of this overlap
					if collider_vector_min <= collidee_vector_min:
						depth = (collider_vector_max - collider_vector_min) + (collidee_vector_max - collidee_vector_min) - (collidee_vector_max - collider_vector_min)
					else:
						depth = (collider_vector_max - collider_vector_min) + (collidee_vector_max - collidee_vector_min) - (collider_vector_max - collidee_vector_min)
					if last_depth < 0 or last_depth > depth:
						last_depth = depth
						collision_axis = i
						print 'collision!'
						print 'axis', collision_axis
						print 'depth:', depth
			return collision_axis

	def getSeparatingAxes(self, boundingbox, position):
		vertices = boundingbox.getVertices()
		axes = []
		for side in range(len(vertices)):
			n = side + 1
			if n == len(vertices):
				n = 0
			direction = vertices[n] - vertices[side]
			vec = Vec2(position, direction)
			axes.append(vec.rotate(90))
		return axes
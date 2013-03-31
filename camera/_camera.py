from components.position import Position
from gameobject.gameobject import GameObject
import components.enum as enum

Chasers = enum.enum(
	'TARGET_SNAP', 
	'TARGET_SNAP_X', 
	'TARGET_SNAP_Y',
	'TARGET_CHASE',
	'TARGET_CHASE_X',
	'TARGET_CHASE_Y',
	'FREE_SNAP',
	'FREE_SNAP_X',
	'FREE_SNAP_Y',
	'FREE_CHASE',
	'FREE_CHASE_X',
	'FREE_CHASE_Y'	)



class Camera(GameObject):
	def __init__(self, globalID, width, height, target = None, camPos = Position([0,0])):
		global Chasers
		super(Camera, self).__init__(globalID)
		self.viewport = Position([width, height])
		self.cam_target = target
		self.chase_type = Chasers.TARGET_SNAP
		self.min_snap = 5

		self.camPos = camPos

	def update(self, dt):
		self.camPos = self.pos
		super(Camera, self).update(dt)
		if self.cam_target != None:
			destination = self.cam_target.getWorldPosition()
			print destination)
		else:
			destination = self.dest
		self.moveToTarget(destination)

		print self.camPos)

		self.dest = self.camPos

	def moveToTarget(self, dest):
		global Chasers
		if self.chase_type == Chasers.TARGET_SNAP or self.chase_type == Chasers.REE_SNAP:
			self.pos = dest
			self.vel = self.vel.zero()
		elif self.chase_type == Chasers.ARGET_CHASE or self.chase_type == Chasers.FREE_CHASE:
			"""
				If the distance to the target is > camera's maxV, move maxV.
				If it's less than maxV but greater than min_snap, move 0.75 of the distance.
				If it's less than min_snap, snap to the target location
			"""
			dist = self.getWorldPosition.distTo(dest)
			direc = self.getWorldPosition.dirTo(dest)

			if dist >= self.max_speed:
				self.vel = direc * self.max_speed
			elif dist < self.max_speed and dist > self.min_snap:
				self.vel = direc * (dist * 0.75)
			else:
				self.pos = dest
				self.vel = self.vel.zero()
			
	def getPosition(self):
		return self.camPos

	def translateToCamSpace(self, pos):
		return self.camPos - pos + (self.viewport / 2)
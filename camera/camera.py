from components.position import Position
from gameobject.gameobject import GameObject

class Camera(GameObject):
	TARGET_SNAP = 0	#camera always snaps immediately to target position
	TARGET_CHASE = 1 #camera follows a predefined amount of steps behind target position
	FREE_SNAP = 2
	FREE_CHASE = 3

	def __init__(self, globalID, width, height, target = None, camPos = Position([0,0])):
		super(Camera, self).__init__(globalID)
		self.viewport_width = width
		self.viewport_height = height
		self.cam_target = target
		self.chase_type = "SNAP"

		self.camPos = camPos

	def update(self, dt):
		if self.cam_target != None:
			destination = self.cam_target.getWorldPosition()
		else:
			destination = self.dest



		self.dest = self.camPos
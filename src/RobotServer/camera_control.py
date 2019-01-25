#!/usr/bin/env python
'''
**********************************************************************
* Filename    : CameraControl
* Description : Control the Servo motors for Panning and Tilting 
				the Camera
* Author      : Cody Trombley
* Update      :  
**********************************************************************
'''
from SunFounder_PCA9685 import Servo

class Camera_Control(object):
	CAMERA_PAN_CHANNEL = 1
	CAMERA_TILT_CHANNEL = 2
	
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "camera_mover.py" -'
	
	def __init__(self, debug=_DEBUG, bus_number = 1, pan_channel = CAMERA_PAN_CHANNEL, tilt_channel = CAMERA_TILT_CHANNEL):
		
		self._pan_channel = pan_channel
		self._tilt_channel = tilt_channel
		self._straight_tilt_angle = 90
		self._straight_pan_angle = 90
		self.panning_max = 45
		self.tilting_max = 45
		self._turning_offset = 0
		
		#Objects for controlling tilt and pan Servo motors
		self.pan = Servo.Servo(self._pan_channel, bus_number = bus_number, offset = 0)
		self.tilt = Servo.Servo(self._tilt_channel, bus_number = bus_number, offset = 0)
		
		
		self.debug = debug
		if self._DEBUG:
			print("{} Camera Pan PWM channel: {}".format(self._DEBUG_INFO, self._pan_channel))
			print("{} Camera Tilt PWN channel: {}".format(self._DEBUG_INFO, self._tilt_channel))
			print("{} Camera Pan offset value: {}".format(self._DEBUG_INFO, self.turning_offset))
			
		if self._DEBUG:
			print("{} \n\tLeft pan angle: {}\n \tStraight pan angle: {}\n \tRight pan angle: {}".format(self._DEBUG_INFO, self._pan_angle["left"], self._pan_angle["straight"], self._pan_angle["right"]))
			print("{} \n\tDown tilt angle: {}\n \tFlat tilt angle: {}\n \tUp tilt angle: {}".format(self._DEBUG_INFO, self._tilt_angle["down"], self._tilt_angle["flat"], self._tilt_angle["up"]))
				
	def pan_left(self):
		if self._DEBUG:
			print("{} Execute left pan.".format(self._DEBUG_INFO))
		self.pan.write(self._pan_angle["left"])

	def pan_straight(self):
		if self._DEBUG:
			print("{} Execute straight pan.".format(self._DEBUG_INFO))
		self.pan.write(self._pan_angle["straight"])

	def pan_right(self):
		
		if self._DEBUG:
			print("{} Execute right pan.".format(self._DEBUG_INFO))
		self.pan.write(self._pan_angle["right"])

	def pan_to(self, angle):
		#Pan camera to given horizontal angle
		if self._DEBUG:
			print self._DEBUG_INFO, "Pan to", angle
		if angle < self._pan_angle["left"]:
			angle = self._pan_angle["left"]
		if angle > self._pan_angle["right"]:
			angle = self._pan_angle["right"]
		self.pan.write(angle)
		
	def tilt_up(self):
		if self._DEBUG:
			print(self._DEBUG_INFO, "Tilt up")
		self.tilt.write(self._tilt_angle["up"])
		
	def tilt_flat(self):
		if self._DEBUG:
			print(self._DEBUG_INFO, "Tilt flat")
		self.tilt.write(self._tilt_angle["flat"])
		
	def tilt_down(self):
		if self._DEBUG:
			print(self._DEBUG_INFO, "Tilt down")
		self.tilt.write(self._tilt_angle["down"])
		
	def tilt_to(self, angle):
		#Tilt camera to given angle
		if self._DEBUG:
			print("{} Tilt to {}".format(self._DEBUG_INFO, angle))
		if angle < self._tilt_angle["down"]:
			angle = self._tilt_angle["down"]
		if angle > self._tilt_angle["up"]:
			angle = self._tilt_angle["up"]
		self.tilt.write(angle)
		
	@property
	def pan_channel(self):
		return self._pan_channel
		
	@pan_channel.setter
	def pan_channel(self, chn):
		self._pan_channel = chn

	@property
	def tilt_channel(self):
		return self._tilt_channel
	
	@tilt_channel.setter
	def tilt_channel(self, chn):
		self._tilt_channel = chn

	@property
	def panning_max(self):
		return self._panning_max

	@panning_max.setter
	def panning_max(self, angle):
		self._panning_max = angle
		self._min_pan_angle = self._straight_pan_angle - angle
		self._max_pan_angle = self._straight_pan_angle + angle
		self._pan_angle = {"left":self._min_pan_angle, "straight":self._straight_pan_angle, "right":self._max_pan_angle}
		
	@property
	def tilting_max(self):
		return self._tilting_max
		
	@tilting_max.setter
	def tilting_max(self, angle):
		self._tilting_max = angle
		self._min_tilt_angle = self._straight_tilt_angle - angle
		self._max_tilt_angle = self._straight_tilt_angle + angle
		self._tilt_angle = {"down":self._min_tilt_angle, "flat":self._straight_tilt_angle, "up":self._max_tilt_angle}

	@property
	def turning_offset(self):
		return self._turning_offset

	@turning_offset.setter
	def turning_offset(self, value):
		if not isinstance(value, int):
			raise TypeError('"turning_offset" must be "int"')
		self._turning_offset = value
		self.db.set('turning_offset', value)
		self.pan.offset = value
		self.turn_straight()

	@property
	def debug(self):
		return self._DEBUG
 
	@debug.setter
	def debug(self, debug):
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug error')
        
    
      
def test():
	import picar
	picar.setup()
	
	camera = Camera_Control(debug = True)
	try:
		while True:
	
			test_pan_angle = input("Enter a pan value: ")
			test_tilt_angle = input("Enter a tilt value: ")
		
			camera.pan_to(test_pan_angle)
			camera.tilt_to(test_tilt_angle)
	except KeyboardInterrupt:
		camera.pan_straight()
		camera.tilt_flat()
		
		
    
if __name__ == '__main__':
  test() 
      
      
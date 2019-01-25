#/usr/bin/env python3
'''
**********************************************************************
* Filename    : TB6612.py
* Description : A driver module for TB6612
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cody Trombley	2019-01-23    Python 3 port
				Cavon    		2016-09-23    New release
**********************************************************************
'''
import RPi.GPIO as GPIO

class Motor(object):
	''' 
		Motor driver class
		Set direction_channel to the GPIO channel which connect to MA, 
		Set motor_B to the GPIO channel which connect to MB,
		Both GPIO channel use BCM numbering;
		Set pwm_channel to the PWM channel which connect to PWMA,
		Set pwm_B to the PWM channel which connect to PWMB;
		PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
		Set debug to True to print out debug informations.
	'''
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "TB6612_3.py": '
	_GPIO_WARNINGS = False
	
	def __init__(self, direction_channel, pwm = None, offset = True):
		''' Initialize a motor on given direction channel and PWM channel '''
		if self._DEBUG:
			print(f'{self._DEBUG_INFO} Debug on.')
		self.direction_channel = direction_channel
		self._pwm = pwm
		self._offset = offset
		self.forward_offset = self._offset
		
		self.backward_offset = not self.forward_offset
		self._speed = 0
		
		GPIO.setwarnings(self._GPIO_WARNINGS)
		GPIO.setmode(GPIO.BCM)
		
		if self._DEBUG:
			print(f'{self._DEBUG_INFO} Setup motor direction channel on {direction_channel}')
			print(f'{self._DEBUG_INFO} Setup motor pwm channel as {self._pwm.__name__}')
		GPIO.setup(self.direction_channel, GPIO.OUT)
		
	@property
	def speed(self):
		return self._speed
		
	@speed.setter
	def speed(self, speed):
		''' Set speed with given value '''
		if speed not in range (0, 101):
			raise ValueError('Speed values must be between 0 and 100. Input value: "{0}"'.format(speed))
		if not callable(self._pwm):
			raise ValueError('PWM is not callable, set Motor.pwm to a pwm control function with only 1 variable speed')
		if self._DEBUG:
			print(f'{self._DEBUG_INFO} Set speed to: {speed}')
		self._speed = speed
		self._pwm(self._speed)
	
	def forward(self):
		''' Set the motor direction to forward '''
		GPIO.output(self.direction_channel, self.forward_offset)
		self.speed = self._speed
		if self._DEBUG:
			print(f'{self._DEBUG_INFO Motor moving backwards: {self.backward_offset}')
	
	def backward(self):
		''' Set the motor direction to backward '''
		GPIO.output(self.direction_channel, self.backward_offset)
		self.speed = self._speed
		if self._DEBUG:
			print(f'{self._DEBUG_INFO} Motor moving backwards: {self.backward_offset}')
			
	def stop(self):
		''' Stop motors by setting speed to 0 '''
		if self._DEBUG:
			print(f'{self._DEBUG} Motor stop.')
		self.speed = 0
		
	@property 
	def offset(self):
		return self._offset
		
	@offset.setter
	def offset(self, value):
		''' Set offset in a user-friendly manner '''
			if value not in (True, False):
				raise ValueError('Offset value must be Boolean value.')
			self.forward_offset = value
			self.backward_offset = not self.forward_offset
			if self._DEBUG:
				print(f'{self._DEBUG_INFO} Set offset to {value}.')
	
	@property
	def debug(self):
		return self._DEBUG
	
	@debug.setter
	def debug(self, debug):
		if debug not in (True, False):
			raise ValueError('Debug must be set to True or False.')
		else:
			self._DEBUG = debug
		
		if self._DEBUG
			print(f'{self._DEBUG_INFO} Set debug on.')
		else:
			print(f'{self._DEBUG_INFO} Set debug off.')
	
	@property
	def pwm(self):
		return self._pwm
		
	@pwm.setter
	def pwm(self, pwm):
		if self._DEBUG:
			print(f'{self._DEBUG_INFO} PWM set.')
		self._pwm = pwm
		
		
def test():
	import time

	print("********************************************")
	print("*                                          *")
	print("*           SunFounder TB6612              *")
	print("*                                          *")
	print("*          Connect MA to BCM17             *")
	print("*          Connect MB to BCM18             *")
	print("*         Connect PWMA to BCM27            *")
	print("*         Connect PWMB to BCM12            *")
	print("*                                          *")
	print("********************************************")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup((27, 22), GPIO.OUT)
	a = GPIO.PWM(27, 60)
	b = GPIO.PWM(22, 60)
	a.start(0)
	b.start(0)

	def a_speed(value):
		a.ChangeDutyCycle(value)

	def b_speed(value):
		b.ChangeDutyCycle(value)

	motorA = Motor(23)
	motorB = Motor(24)
	motorA.debug = True
	motorB.debug = True
	motorA.pwm = a_speed
	motorB.pwm = b_speed

	delay = 0.05

	motorA.forward()
	for i in range(0, 101):
		motorA.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.speed = i
		time.sleep(delay)

	motorA.backward()
	for i in range(0, 101):
		motorA.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.speed = i
		time.sleep(delay)

	motorB.forward()
	for i in range(0, 101):
		motorB.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.speed = i
		time.sleep(delay)

	motorB.backward()
	for i in range(0, 101):
		motorB.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.speed = i
		time.sleep(delay)


if __name__ == '__main__':
	test()
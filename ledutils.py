#!/usr/bin/env python2
import pigpio
from struct import pack, unpack
class RGBStrip:
	def __init__(self, rpin, gpin, bpin):
		self.pi = pigpio.pi()
		self.pins = {'red':   rpin,
		             'green': gpin,
		             'blue':  bpin}
		for pin in self.pins.values():
			self.pi.set_mode(pin, pigpio.OUTPUT)
		self.color = {'red':        255,
		              'green':      255,
		              'blue':       255,
		              'brightness': 255}
		self.status = False

	def getBrightness(self):
		if self.status:
			return str(int(max(self.color['red'], self.color['green'], self.color['blue']) / 255.0 * 100.0))
		else:
			return str(0)

	def on(self):
		self.status = True
		self.update()

	def off(self):
		self.status = False
		self.update()

	def setColor(self, r, g, b):
		self.color['red'] = r
		self.color['green'] = g
		self.color['blue'] = b
		self.update()

	def getColor(self):
		return str(pack('BBB', *(self.color['red'], self.color['green'], self.color['blue'])).encode('hex'))

	def setHEX(self, hexcolor):
		self.setColor(*unpack('BBB', hexcolor.decode('hex')))

	def update(self):
		if self.status:
			self.pi.set_PWM_dutycycle(self.pins['red'], self.color['red'])
			self.pi.set_PWM_dutycycle(self.pins['green'], self.color['green'])
			self.pi.set_PWM_dutycycle(self.pins['blue'], self.color['blue'])
		else:
			self.pi.set_PWM_dutycycle(self.pins['red'], 0)
			self.pi.set_PWM_dutycycle(self.pins['green'], 0)
			self.pi.set_PWM_dutycycle(self.pins['blue'], 0)

	def getStatus(self):
		return str(int(self.status))

#!/usr/bin/env python2
import pigpio
from struct import pack, unpack
from threading import Thread
from time import sleep


class RGBLed:
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
		self.stopFade = False
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

	def fadeworker(self):
		while True:
			if self.status:
				c = [255, 0, 0]
				for decColor in range(3):
					if decColor == 2:
						incColor = 0
					else:
						incColor = decColor + 1
					for _ in range(255):
						c[decColor] -= 1
						c[incColor] += 1
						self.setColor(c[0], c[1], c[2])
						if self.stopFade:
							self.setHEX("000000")
							self.stopFade = False
							return
						sleep(0.005)

	def fade(self):
		Thread(target=self.fadeworker).start()

	def noFade(self):
		self.stopFade = True
		while self.stopFade:
			sleep(0.000001)

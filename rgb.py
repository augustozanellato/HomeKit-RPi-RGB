#!/usr/bin/env python

from flask import Flask
import pigpio
from struct import unpack, pack
from platform import machine

if machine() == 'x86_64' or machine() == 'i386':
	pi = pigpio.pi('192.168.1.21')
else:
	pi = pigpio.pi()

app = Flask(__name__)

# Explorer HAT uses GPIO 27 = red, 4 = blue, 5 = green
# Pibrella uses GPIO 27 = red, 17 = yellow, 4 = green


# Map of LED names and associated GPIO pins
leds = {
	'red':        0,
	'blue':       0,
	'green':      0,
	'brightness': 0,
	'status':     False
}
pins = {
	'red':   10,
	'green': 9,
	'blue':  11
}


# for color in leds.keys():
#	GPIO.setup(leds[color], GPIO.OUT)

def ledUpdate():
	global pins
	global leds
	global pi
	if leds['status']:
		pi.set_PWM_dutycycle(pins['red'], leds['red'])
		pi.set_PWM_dutycycle(pins['green'], leds['green'])
		pi.set_PWM_dutycycle(pins['blue'], leds['blue'])
	else:
		pi.set_PWM_dutycycle(pins['red'], 0)
		pi.set_PWM_dutycycle(pins['green'], 0)
		pi.set_PWM_dutycycle(pins['blue'], 0)


@app.route("/led/set/<color>")
def setColor(color):
	try:
		leds['red'], leds['green'], leds['blue'] = unpack('BBB', color.decode('hex'))
		ledUpdate()
		return 'Successfully set color: {}'.format(color)
	except:
		return 'Invalid color: {}'.format(color)


@app.route("/led/get/color")
def getColor():
	global leds
	return pack('BBB', *(leds['red'], leds['green'], leds['blue'])).encode('hex')


@app.route("/led/set/b/<brightness>")
def setBrightness(b):
	leds['brightness'] = b
	ledUpdate()
	return "Successfully set brightness: {}".format(leds['brightness'])


@app.route('/led/get/brightness')
def getBrightness():
	global leds
	return str(leds['brightness'])


@app.route('/led/get/status')
def getStatus():
	global leds
	if leds['status']:
		return 'on'
	else:
		return 'off'


@app.route('/led/off')
def ledOff():
	global leds
	leds['status'] = False
	ledUpdate()
	return 'off'


@app.route('/led/on')
def ledOn():
	global leds
	leds['status'] = True
	ledUpdate()
	return 'on'

app.add_url_rule("/", "index", lambda: 'Hello World!')

if __name__ == "__main__":
	app.run(host='0.0.0.0')

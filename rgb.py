#!/usr/bin/env python2

from flask import Flask, request
import pigpio
from struct import unpack, pack
from platform import machine

pi = pigpio.pi()

app = Flask(__name__)

# Array used for storing led values
leds = {
	'red':        0,
	'blue':       0,
	'green':      0,
	'brightness': 0,
	'status':     False
}
# Led pin mapping
pins = {
	'red':   10,
	'green': 9,
	'blue':  11
}

for pin in pins.values():
	pi.set_mode(pin, pigpio.OUTPUT)

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


@app.route("/led/webset/colorset.html")
def setColorWeb():
        try:
                leds['red'], leds['green'], leds['blue'] = unpack('BBB', str(request.args.get('color')).decode('hex'))
                ledUpdate()
                return 'Successfully set color: {}'.format(request.args.get('color'))
        except:
                return 'Invalid color: {}'.format(request.args.get('color'))

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

@app.route('/')
def index():
	return app.send_static_file('newui.html')

@app.route('/newui.html')
def ui():
        
        return app.send_static_file('newui.html')

@app.route('/jscolor.js')
def js():
	return app.send_static_file('jscolor.js')

#app.add_url_rule("/", "index", lambda: 'Hello World!')

if __name__ == "__main__":
	app.run(host='0.0.0.0')

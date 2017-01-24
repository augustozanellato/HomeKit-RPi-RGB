#!/usr/bin/env python2

from flask import Flask, request
from struct import unpack, pack
import ledutils
app = Flask(__name__)

app.config['CACHE_TYPE'] = "null"

LEDStrip = ledutils.RGBStrip(10, 9, 11)

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
def setBrightness(brightness):
	leds['brightness'] = brightness
	ledUpdate()
	return "Successfully set brightness: {}".format(leds['brightness'])

@app.route('/led/get/brightness')
def getBrightness():
	return LEDStrip.getBrightness()

@app.route('/led/get/status')
def getStatus():
	global leds
	if leds['status']:
		return '1'
	else:
		return '0'

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
	try:
		leds['red'], leds['green'], leds['blue'] = unpack('BBB', str(request.args.get('color')).decode('hex'))
		ledUpdate()
	except:
		pass
	try:
		if request.args.get('status') == 'on':
			leds['status'] = True
		elif request.args.get('status') == 'off':
			leds['status'] = False
		ledUpdate()
	except:
		pass
	return app.send_static_file('newui.html')

@app.route('/jscolor.js')
def js():
	return app.send_static_file('jscolor.js')

@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
	r.headers["Pragma"] = "no-cache"
	r.headers['Expires'] = "0"
	return r

if __name__ == "__main__":
	app.run(host='0.0.0.0')

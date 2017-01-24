#!/usr/bin/env python2

from flask import Flask, request
import ledutils

app = Flask(__name__)

app.config['CACHE_TYPE'] = "null"

ledstrip = ledutils.RGBStrip(10, 9, 11)

@app.route("/led/set/<color>")
def setColor(color):
	try:
		ledstrip.setHEX(color)
		return 'Successfully set color: {}'.format(color)
	except:
		return 'Invalid color: {}'.format(color)

@app.route("/led/get/color")
def getColor():
	return ledstrip.getColor()

@app.route('/led/get/brightness')
def getBrightness():
	return ledstrip.getBrightness()

@app.route('/led/get/status')
def getStatus():
	return ledstrip.getStatus()

@app.route('/led/off')
def ledOff():
	ledstrip.status = False
	ledstrip.update()
	return getStatus()

@app.route('/led/on')
def ledOn():
	ledstrip.status = True
	ledstrip.update()
	return getStatus()

@app.route('/')
def index():
	return app.send_static_file('newui.html')

@app.route('/newui.html')
def ui():
	try:
		ledstrip.setHEX(str(request.args.get('color')))
	except:
		pass
	try:
		if request.args.get('status') == 'on':
			ledstrip.status = True
		elif request.args.get('status') == 'off':
			ledstrip.status = False
		ledstrip.update()
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

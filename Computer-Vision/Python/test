# *****************************************************************************
# Copyright (c) 2016 TechBubble Technologies and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html 
#
# Contributors:
#   Adam Milton-Barker - TechBubble Technologies Limited
#   Andrej Petelin - TechBubble Technologies Limited
# *****************************************************************************

import cv2
import sys
import os

import time
import json

from datetime import datetime

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import ssl

import numpy as np

import techbubbleiotjumpwaymqtt.device
from TASSCore import TassCore
frame = ''
TassCore = TassCore()
		
class Handler(BaseHTTPRequestHandler):
	
	def do_GET(self):

		global frame

		

		self.send_response(200)
		self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
		self.end_headers()
		
		while True:

			r, buf = cv2.imencode(".jpg",frame,(cv2.IMWRITE_JPEG_QUALITY,100))
			self.wfile.write(bytes("--jpgboundary\r\n", "utf-8"))
			self.send_header('Content-type','image/jpeg')
			self.send_header('Content-length',str(len(buf)))
			self.end_headers()
			self.wfile.write(bytearray(buf))
			self.wfile.write(bytes("\r\n", "utf-8"))
			time.sleep(1)

		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class TASS():
	
	def __init__(self):
		
		self.JumpWayMQTTClient = ""
		self.configs = {}
		self.train = 0
		
		with open('config.json') as configs:
			self.configs = json.loads(configs.read())
			
		self.startMQTT()

		self.OpenCVCapture = cv2.VideoCapture(0)
		self.OpenCVCapture.set(5, 60) 
		self.OpenCVCapture.set(3,1280)
		self.OpenCVCapture.set(4,720)

		self.model = cv2.face.createEigenFaceRecognizer(threshold=self.configs["ClassifierSettings"]["predictionThreshold"])
		self.model.load(self.configs["ClassifierSettings"]["Model"])
		
	def deviceCommandsCallback(self,topic,payload):
		
		print("Received command data: %s" % (payload))
		newSettings = json.loads(payload.decode("utf-8"))
		
	def startMQTT(self):
		
		try:
			
			self.JumpWayMQTTClient = techbubbleiotjumpwaymqtt.device.JumpWayPythonMQTTDeviceConnection({
				"locationID": self.configs["IoTJumpWaySettings"]["SystemLocation"],  
				"zoneID": self.configs["IoTJumpWaySettings"]["SystemZone"], 
				"deviceId": self.configs["IoTJumpWaySettings"]["SystemDeviceID"], 
				"deviceName": self.configs["IoTJumpWaySettings"]["SystemDeviceName"], 
				"username": self.configs["IoTJumpWayMQTTSettings"]["username"], 
				"password": self.configs["IoTJumpWayMQTTSettings"]["password"]
			})
			
		except Exception as e:
			print(str(e))
			sys.exit()
			
		self.JumpWayMQTTClient.connectToDevice()
		
		self.JumpWayMQTTClient.subscribeToDeviceChannel("Commands")
		self.JumpWayMQTTClient.deviceCommandsCallback = self.deviceCommandsCallback

	def start_server(self):

		httpd = ThreadedHTTPServer(('0.0.0.0', TASS.configs["StreamSettings"]["streamPort"]), Handler)
		httpd.socket = ssl.wrap_socket (httpd.socket, certfile=os.getcwd()+"/certs/crt.crt", keyfile=os.getcwd()+"/certs/key.key", server_side=True)
		print("Server Started")
		httpd.serve_forever()
		
TASS = TASS()
	
Server = threading.Thread(name='Server', target=TASS.start_server)
Server.start()

while True:
	
	ret, frame = TASS.OpenCVCapture.read()
	if not ret: continue
	currentImage,detected = TassCore.captureAndDetect(frame)
	if detected is None:
		continue
		
	image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	x, y, w, h = detected
	crop = TassCore.resize(TassCore.crop(image, x, y, w, h))
	label,confidence = TASS.model.predict(crop)

	if label:

		print("Person " + str(label) + " Confidence " +str(confidence))

		TASS.JumpWayMQTTClient.publishToDeviceChannel(
			"Sensors",
			{
				"Sensor":"CCTV",
				"SensorID":TASS.configs["IoTJumpWaySettings"]["SystemCameraID"],
				"SensorValue":"USER: " + str(label)
			}
		)

	else:

		print("Person not recognised " + str(label) + " Confidence "+str(confidence));

		TASS.JumpWayMQTTClient.publishToDeviceChannel(
			"Sensors",
			{
				"Sensor":"CCTV",
				"SensorID":TASS.configs["IoTJumpWaySettings"]["SystemCameraID"],
				"SensorValue":"NOT RECOGNISED"
			}
		)

		TASS.JumpWayMQTTClient.publishToDeviceChannel(
			"Warnings",
			{
				"WarningType":"CCTV",
				"WarningOrigin":TASS.configs["IoTJumpWaySettings"]["SystemCameraID"],
				"WarningValue":"Intruder",
				"WarningMessage":"An intruder has been detected"
			}
		)

TASS.OpenCVCapture.release()
cv2.destroyAllWindows()
TASS.JumpWayMQTTClient.disconnectFromDevice()

# *****************************************************************************
# Copyright (c) 2016 and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#   Adam Milton-Barker - Limited
# *****************************************************************************

import cv2
import sys
import os

import time
import json

from datetime import datetime

import JumpWayMQTT.Device as JWMQTTdevice
from TASSCore import TassCore

TassCore = TassCore()

class TASS():

	def __init__(self):

		self.jumpwayClient = ""
		self.configs = {}
		self.train = 0

		with open('required/config.json') as configs:
			self.configs = json.loads(configs.read())

		self.startMQTT()

		print("LOADING VIDEO CAMERA")

		#self.OpenCVCapture = cv2.VideoCapture(0)
		self.OpenCVCapture = cv2.VideoCapture('http://'+self.configs["StreamSettings"]["streamIP"]+':'+self.configs["StreamSettings"]["streamPort"]+'/stream.mjpg')

		#self.OpenCVCapture.set(5, 30)
		#self.OpenCVCapture.set(3,640)
		#self.OpenCVCapture.set(4,480)

	def deviceCommandsCallback(self,topic,payload):

		print("Received command data: %s" % (payload))
		newSettings = json.loads(payload.decode("utf-8"))

	def startMQTT(self):

		try:

            self.jumpwayClient = JWMQTTdevice.DeviceConnection({
                "locationID": self.configs["IoTJumpWay"]["Location"],
                "zoneID": self.configs["IoTJumpWay"]["Zone"],
                "deviceId": self.configs["IoTJumpWay"]["Device"],
                "deviceName": self.configs["IoTJumpWay"]["DeviceName"],
                "username": self.configs["IoTJumpWayMQTT"]["MQTTUsername"],
                "password": self.configs["IoTJumpWayMQTT"]["MQTTPassword"]
            })

		except Exception as e:
			print(str(e))
			sys.exit()

        self.jumpwayClient.connectToDevice()
        self.jumpwayClient.subscribeToDeviceChannel("Commands")
        self.jumpwayClient.deviceCommandsCallback = self.deviceCommandsCallback

TASS = TASS()
model = cv2.face.createEigenFaceRecognizer(threshold=TASS.configs["ClassifierSettings"]["predictionThreshold"])
model.load(TASS.configs["ClassifierSettings"]["Model"])
print("LOADED STREAM & MODEL")
while True:

	if(TASS.train==1):

		print("TRAINING MODE")
		TassCore.processTrainingData()
		TassCore.trainModel()
		TASS.train=0

	elif(TASS.configs["AppSettings"]["armed"]==1):

		try:

			ret, frame = TASS.OpenCVCapture.read()
			if not ret: continue

			currentImage,detected = TassCore.captureAndDetect(frame)
			if detected is None:
				continue

			image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			x, y, w, h = detected
			crop = TassCore.resize(TassCore.crop(image, x, y, w, h))
			label,confidence = model.predict(crop)

			if label:

				print("Person " + str(label) + " Confidence " +str(confidence))

				TASS.jumpwayClient.publishToDeviceChannel(
					"Sensors",
					{
						"Sensor":"CCTV",
						"SensorID":TASS.configs["IoTJumpWaySettings"]["SystemCameraID"],
						"SensorValue":"USER: " + str(label)
					}
				)

			else:

				print("Person not recognised " + str(label) + " Confidence "+str(confidence));

				TASS.jumpwayClient.publishToDeviceChannel(
					"Sensors",
					{
						"Sensor":"CCTV",
						"SensorID":TASS.configs["IoTJumpWaySettings"]["SystemCameraID"],
						"SensorValue":"NOT RECOGNISED"
					}
				)

				TASS.jumpwayClient.publishToDeviceChannel(
					"Warnings",
					{
						"WarningType":"CCTV",
						"WarningOrigin":TASS.configs["IoTJumpWaySettings"]["SystemCameraID"],
						"WarningValue":"Intruder",
						"WarningMessage":"An intruder has been detected"
					}
				)

			time.sleep(1)

		except cv2.error as e:
			print(e)

TASS.OpenCVCapture.release()
cv2.destroyAllWindows()
TASS.jumpwayClient.disconnectFromDevice()

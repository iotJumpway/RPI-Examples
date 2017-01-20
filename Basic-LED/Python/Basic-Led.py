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
# *****************************************************************************

import time
import sys
import json

import RPi.GPIO as GPIO
import techbubbleiotjumpwaymqtt.device

class BasicLED():
    
    def __init__(self):
        
        self.JumpWayMQTTClient = ""
        self.configs = {}
        
        with open('config.json') as configs:
            self.configs = json.loads(configs.read())
            
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(
            self.configs["Sensors"]["LED"]["PIN"],
            GPIO.OUT
        )
        
        self.startMQTT()
        
    def deviceCommandsCallback(self,topic,payload):
        
        print("Received command data: %s" % (payload))
        
        jsonData = json.loads(payload.decode("utf-8"))
        
        if jsonData['ActuatorID']==self.configs["Sensors"]["LED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='ON':
            
            GPIO.output(
                self.configs["Sensors"]["LED"]["PIN"],
                GPIO.HIGH
            )

        elif jsonData['ActuatorID']==self.configs["Sensors"]["LED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='OFF':
            
            GPIO.output(
                self.configs["Sensors"]["LED"]["PIN"],
                GPIO.LOW
            )
            
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
        
BasicLED = BasicLED()

while True:
    
    BasicLED.JumpWayMQTTClient.publishToDeviceChannel(
		"Commands",
		{
			"Actuator":"LED",
			"ActuatorID":str(BasicLED.configs["Sensors"]["LED"]["ID"]),
			"Command":"TOGGLE",
			"CommandValue":"ON"
		}
    )
    
    time.sleep(5)
    
    BasicLED.JumpWayMQTTClient.publishToDeviceChannel(
		"Commands",
		{
			"Actuator":"LED",
			"ActuatorID":str(BasicLED.configs["Sensors"]["LED"]["ID"]),
			"Command":"TOGGLE",
			"CommandValue":"OFF"
		}
    )
    
    time.sleep(5)
    
BasicLED.JumpWayMQTTClient.disconnectFromDevice()
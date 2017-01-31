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

import techbubbleiotjumpwaymqtt.application

class BasicLedApplication():
    
    def __init__(self):
        
        self.JumpWayMQTTClient = ""
        self.configs = {}
        
        with open('config.json') as configs:
            self.configs = json.loads(configs.read())
        
        self.startMQTT()
            
    def startMQTT(self):
        
        try:
            
            self.JumpWayMQTTClient = techbubbleiotjumpwaymqtt.application.JumpWayPythonMQTTApplicationConnection({
				"locationID": self.configs["IoTJumpWaySettings"]["SystemLocation"],  
				"applicationID": self.configs["IoTJumpWaySettings"]["SystemApplicationID"], 
				"applicationName": self.configs["IoTJumpWaySettings"]["SystemApplicationName"], 
				"username": self.configs["IoTJumpWayMQTTSettings"]["applicationUsername"], 
				"password": self.configs["IoTJumpWayMQTTSettings"]["applicationPassword"]
			})
            
        except Exception as e:
            print(str(e))
            sys.exit()
            
        self.JumpWayMQTTClient.connectToApplication()
        
BasicLedApplication = BasicLedApplication()

while True:
    
    BasicLedApplication.JumpWayMQTTClient.publishToDeviceChannel(
		"Commands",
		BasicLedApplication.configs["IoTJumpWaySettings"]["SystemZone"],
		BasicLedApplication.configs["IoTJumpWaySettings"]["SystemDeviceID"],
		{
			"Actuator":"LED",
			"ActuatorID":BasicLedApplication.configs["Actuators"]["LED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"ON"
		}
    )
    
    time.sleep(5)
    
    BasicLedApplication.JumpWayMQTTClient.publishToDeviceChannel(
		"Commands",
		BasicLedApplication.configs["IoTJumpWaySettings"]["SystemZone"],
		BasicLedApplication.configs["IoTJumpWaySettings"]["SystemDeviceID"],
		{
			"Actuator":"LED",
			"ActuatorID":BasicLedApplication.configs["Actuators"]["LED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"OFF"
		}
    )
    
    time.sleep(5)
    
BasicLedApplication.JumpWayMQTTClient.disconnectFromApplication()
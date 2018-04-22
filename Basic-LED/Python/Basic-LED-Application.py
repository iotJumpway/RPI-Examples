############################################################################################
# Title: IoT JumpWay Raspberry Pi Basic LED Application
# Description: Application for connecting to IoT connected LED using Raspberry Pi.
# Last Modified: 2018-04-22
############################################################################################

import time, sys, json

import JumpWayMQTT.Device as JWMQTTdevice

class BasicLedApplication():

    def __init__(self):

        self.jumpwayClient = None
        self.configs = {}

        with open('required/confs.json') as configs:
            self.configs = json.loads(configs.read())

        self.startMQTT()

    def startMQTT(self):

        try:

            self.jumpwayClient = JWMQTTdevice.DeviceConnection({
                "locationID": self.configs["IoTJumpWay"]["Location"],
                "applicationID": self.configs["IoTJumpWay"]["App"],
                "applicationName": self.configs["IoTJumpWay"]["AppName"],
                "username": self.configs["IoTJumpWayMQTT"]["AppMQTTUsername"],
                "password": self.configs["IoTJumpWayMQTT"]["AppMQTTPassword"]
            })

        except Exception as e:
            print(str(e))
            sys.exit()

        self.jumpwayClient.connectToApplication()

BasicLedApplication = BasicLedApplication()

while True:

    BasicLedApplication.jumpwayClient.publishToDeviceChannel(
		"Commands",
		BasicLedApplication.configs["IoTJumpWay"]["Zone"],
		BasicLedApplication.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":BasicLedApplication.configs["Actuators"]["LED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"ON"
		}
    )

    time.sleep(5)

    BasicLedApplication.jumpwayClient.publishToDeviceChannel(
		"Commands",
		BasicLedApplication.configs["IoTJumpWay"]["Zone"],
		BasicLedApplication.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":BasicLedApplication.configs["Actuators"]["LED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"OFF"
		}
    )

    time.sleep(5)

BasicLedApplication.jumpwayClient.disconnectFromApplication()
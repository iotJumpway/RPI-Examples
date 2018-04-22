############################################################################################
# Title: IoT JumpWay Raspberry Pi Dev Kit Alarm Application
# Description: Application for connecting to IoT connected alarm using Raspberry Pi.
# Last Modified: 2018-04-22
############################################################################################

import time, sys, json

import JumpWayMQTT.Application as JWMQTTapplication

class Application():

    def __init__(self):

        self.jumpwayClient = None
        self.configs = {}

        with open('required/confs.json') as configs:
            self.configs = json.loads(configs.read())

        self.startMQTT()

    def startMQTT(self):

        try:

            self.jumpwayClient = JWMQTTapplication.ApplicationConnection({
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

Application = Application()

while True:

    Application.jumpwayClient.publishToDeviceChannel(
		"Commands",
		Application.configs["IoTJumpWay"]["Zone"],
		Application.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":Application.configs["Actuators"]["trueLED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"ON"
		}
    )

    time.sleep(5)

    Application.jumpwayClient.publishToDeviceChannel(
		"Commands",
		Application.configs["IoTJumpWay"]["Zone"],
		Application.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":Application.configs["Actuators"]["trueLED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"OFF"
		}
    )

    time.sleep(5)

    Application.jumpwayClient.publishToDeviceChannel(
		"Commands",
		Application.configs["IoTJumpWay"]["Zone"],
		Application.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":Application.configs["Actuators"]["falseLED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"ON"
		}
    )

    time.sleep(5)

    Application.jumpwayClient.publishToDeviceChannel(
		"Commands",
		Application.configs["IoTJumpWay"]["Zone"],
		Application.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":Application.configs["Actuators"]["falseLED"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"OFF"
		}
    )

    time.sleep(5)

    Application.jumpwayClient.publishToDeviceChannel(
		"Commands",
		Application.configs["IoTJumpWay"]["Zone"],
		Application.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":Application.configs["Actuators"]["Buzzer"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"ON"
		}
    )

    time.sleep(5)

    Application.jumpwayClient.publishToDeviceChannel(
		"Commands",
		Application.configs["IoTJumpWay"]["Zone"],
		Application.configs["IoTJumpWay"]["Device"],
		{
			"Actuator":"LED",
			"ActuatorID":Application.configs["Actuators"]["Buzzer"]["ID"],
			"Command":"TOGGLE",
			"CommandValue":"OFF"
		}
    )

    time.sleep(5)

Application.jumpwayClient.disconnectFromApplication()
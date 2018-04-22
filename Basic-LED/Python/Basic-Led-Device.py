############################################################################################
# Title: IoT JumpWay Raspberry Pi Basic LED
# Description: IoT connected LED using Raspberry Pi.
# Last Modified: 2018-04-22
############################################################################################

import time
import sys
import json

import RPi.GPIO as GPIO
import JumpWayMQTT.Device as JWMQTTdevice

class BasicLED():

    def __init__(self):

        self.JumpWayMQTTClient = ""
        self.configs = {}

        with open('config.json') as configs:
            self.configs = json.loads(configs.read())

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(
            self.configs["Actuators"]["LED"]["PIN"],
            GPIO.OUT
        )

        self.startMQTT()

    def deviceCommandsCallback(self,topic,payload):

        print("Received command data: %s" % (payload))

        jsonData = json.loads(payload.decode("utf-8"))

        if jsonData['ActuatorID']==self.configs["Actuators"]["LED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='ON':

            GPIO.output(
                self.configs["Actuators"]["LED"]["PIN"],
                GPIO.HIGH
            )

        elif jsonData['ActuatorID']==self.configs["Actuators"]["LED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='OFF':

            GPIO.output(
                self.configs["Actuators"]["LED"]["PIN"],
                GPIO.LOW
            )

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

BasicLED = BasicLED()

while True:

    pass

BasicLED.jumpwayClient.disconnectFromDevice()
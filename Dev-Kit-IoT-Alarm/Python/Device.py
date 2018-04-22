############################################################################################
# Title: IoT JumpWay Raspberry Pi Dev Kit Alarm
# Description: IoT connected alarm system for Raspberry Pi and Grove IoT Kit.
# Last Modified: 2018/04/19
############################################################################################

print("")
print("")
print("!! Welcome to the IoT JumpWay Raspberry Pi Dev Kit Alarm, please wait while the program initiates !!")
print("")

import time, sys, json, grovepi

import JumpWayMQTT.Device as JWMQTTdevice

print("-- Running on Python "+sys.version)
print("")

class Device():

    def __init__(self):

        self.jumpwayClient = None
        self.configs = {}

        with open('required/confs.json') as configs:
            self.configs = json.loads(configs.read())

        self.startMQTT()

        print("")
        print("-- IoT JumpWay Raspberry Pi Dev Kit Alarm Initiated")
        print("")

    def commandsCallback(self,topic,payload):

        print("Received command data: %s" % (payload))

        jsonData = json.loads(payload.decode("utf-8"))

        if int(jsonData['ActuatorID'])==self.configs["Actuators"]["trueLED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='ON':

            grovepi.digitalWrite(self.configs["Actuators"]["trueLED"]["PIN"],1)

        elif int(jsonData['ActuatorID'])==self.configs["Actuators"]["falseLED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='ON':

            grovepi.digitalWrite(self.configs["Actuators"]["falseLED"]["PIN"],1)

        elif int(jsonData['ActuatorID'])==self.configs["Actuators"]["Buzzer"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='ON':

            grovepi.digitalWrite(self.configs["Actuators"]["Buzzer"]["PIN"],1)

        elif int(jsonData['ActuatorID'])==self.configs["Actuators"]["trueLED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='OFF':

            grovepi.digitalWrite(self.configs["Actuators"]["trueLED"]["PIN"],0)

        elif int(jsonData['ActuatorID'])==self.configs["Actuators"]["falseLED"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='OFF':

            grovepi.digitalWrite(self.configs["Actuators"]["falseLED"]["PIN"],0)

        elif int(jsonData['ActuatorID'])==self.configs["Actuators"]["Buzzer"]["ID"] and jsonData['Command']=='TOGGLE' and jsonData['CommandValue']=='OFF':

            grovepi.digitalWrite(self.configs["Actuators"]["Buzzer"]["PIN"],0)

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
        self.jumpwayClient.deviceCommandsCallback = self.commandsCallback

        print("-- IoT JumpWay Initiated")

Device = Device()

grovepi.pinMode(Device.configs["Actuators"]["trueLED"]["PIN"],"OUTPUT")
grovepi.pinMode(Device.configs["Actuators"]["falseLED"]["PIN"],"OUTPUT")
grovepi.pinMode(Device.configs["Actuators"]["Buzzer"]["PIN"],"OUTPUT")

grovepi.digitalWrite(Device.configs["Actuators"]["trueLED"]["PIN"],0)
grovepi.digitalWrite(Device.configs["Actuators"]["falseLED"]["PIN"],0)
grovepi.digitalWrite(Device.configs["Actuators"]["Buzzer"]["PIN"],0)

while True:

    #grovepi.digitalWrite(Device.configs["Actuators"]["trueLED"]["PIN"],1)
    #grovepi.digitalWrite(Device.configs["Actuators"]["falseLED"]["PIN"],1)
    #grovepi.digitalWrite(Device.configs["Actuators"]["Buzzer"]["PIN"],1)
    #time.sleep(2)
    #grovepi.digitalWrite(Device.configs["Actuators"]["trueLED"]["PIN"],0)
    #grovepi.digitalWrite(Device.configs["Actuators"]["falseLED"]["PIN"],0)
    #grovepi.digitalWrite(Device.configs["Actuators"]["Buzzer"]["PIN"],0)
    #time.sleep(2)
    pass

Device.jumpwayClient.disconnectFromDevice()
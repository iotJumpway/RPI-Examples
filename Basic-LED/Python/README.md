# IoT JumpWay Raspberry Pi Examples

![TechBubble IoT JumpWay Docs](../../images/main/IoT-Jumpway.jpg)  

## Introduction

Here you will find sample device scripts for connecting Raspberry Pi to the TechBubble Technologies IoT JumpWay using the Python MQTT Library. The codes allow you to set up a basic device that allows control of an LED. Once you understand how it works you are free to add as many actuators and sensors to your device and modify your code accordingly.

## Before You Begin

If this is the first time you have used the TechBubble IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following link and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications.

[TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs")

## Python Versions

- 2.7
- 3

## Hardware requirements

1. Raspberry Pi.
2. 1 x LED.
3. 1 x Breadboard

## Software requirements

1. TechBubbleIoTJumpWayMQTT  
2. JSon

## Preparing Your Raspberry Pi

Take some time to ensure your Raspberry Pi firmware and packages are up to date.

- Update Raspberry Pi Firmware

```
    [root@localhost ~]# sudo rpi-update
```

- Update Raspberry Pi Trusted Certificates

```
    [root@localhost ~]# sudo apt-get install ca-certificates
```

- Update Raspberry Pi Packages

```
    [root@localhost ~]# sudo apt-get update
    
    [root@localhost ~]# sudo apt-get upgrade
    
    [root@localhost ~]# sudo apt-get dist-upgrade
```

## Install Requirements

    ```
    $ pip install --upgrade pip
    $ pip install -r requirements.txt
    ```

## Setting Up Your Raspberry Pi

- First of all you need to connect up an LED to your Raspberry Pi. To connect the LED you will need a breadboard, 1 LED, 1 resistor and two jumper wires. Connect the LED to pin 18 of your Raspberry Pi and add the sensor ID for the LED that you attached to your device in the Sensors->LED->ID value in config.json. 

```
	"Sensors": {
		"LED": {
			"ID": 0,
			"PIN": 18
		}
	}
```

## Connection Credentials

Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs") to retrieve your connection credentials and update the config.json file with your new credentials.


```
	"IoTJumpWaySettings": {
		"SystemLocation": 0,
		"SystemZone": 0,
		"SystemDeviceID": 0,
		"SystemDeviceName" : "Your Device Name"
	}
```


```
	"IoTJumpWayMQTTSettings": {
		"host": "https://iot.techbubbletechnologies.com",
		"port": "8883",
		"username": "Your MQTT Username",
		"password": "Your MQTT Password"
	}
```


## Execute The Program

    ```
    $ sudo python/python3 Basic-Led.py
    ```

## IoT JumpWay Raspberry Pi Examples Bugs/Issues

Please feel free to create issues for bugs and general issues you come accross whilst using the IoT JumpWay Raspberry Pi Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Raspberry Pi Examples in your IoT projects.
# IoT JumpWay Raspberry Pi Computer Vision Example (TASS)

![TechBubble Autonomous Sight System](img/TASS-Banner.png) 

## Introduction

Here you will find sample device scripts for connecting a Raspberry Pi 3 to the TechBubble Technologies IoT JumpWay using the Python MQTT Library for communication and OpenCV for computer vision. 

The codes allow you to set up a basic device that allows you to train a Haarcascades model, detect recognised / unknown people, optionally monitor the camera in near realtime via a stream, and communicate with the IoT JumpWay sending sensor and warning messages. Once you understand how it works you are free to add as many actuators and sensors to your device and modify your code accordingly.

This example was our original version of TASS, since our move forward with more advanced computer vision libraries and frameworks, we decided to open up the source code.

## Python Versions

- 2.7
- 3.4 or above

## Software requirements

1. Jessie
2. TechBubbleIoTJumpWayMQTT  
3. JSon
4. Flask
5. Flask-Basicauth

## Hardware requirements

![IoT JumpWay Raspberry Pi Computer Vision Example Docs](../../images/Computer-Vision/Hardware.jpg)  

1. Raspberry Pi.
2. Linux Compatible Webcam

## Before You Begin

If this is the first time you have used the TechBubble IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following link and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications.

[TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs")

## Preparing Your Raspberry Pi 3

Take some time to ensure your Raspberry Pi firmware and packages are up to date, and that your device is secure by following the guide below.

[Raspberry Pi 3 Preparation Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/1-Raspberry-Pi-Prep.md "Raspberry Pi 3 Preparation Doc")

## Cloning The Repo

You will need to clone this repository to a location on your Raspberry Pi 3. Navigate to the directory you would like to download it to and issue the following commands.

    $ git clone https://github.com/TechBubbleTechnologies/IoT-JumpWay-RPI-Examples.git

## Installing Open CV

You will need to install OpenCV for this example to work, please follow the document below to install OpenCV on your Raspberry Pi 3.

[Raspberry Pi 3 OpenCV Installation Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/2-Installing-OpenCV.md "Raspberry Pi 3 OpenCV Installation Doc")

## Install Requirements

Next you will need to navigate to the Computer-Vision directory and install the requirements

    $ cd IoT-JumpWay-RPI-Examples/Computer-Vision/Python
    $ pip install --upgrade pip
    $ pip install -r requirements.txt

## Connection Credentials & Sensor Settings

- Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc-](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc") to set up your device. 

![IoT JumpWay Raspberry Pi Computer Vision Example Docs](../../images/Computer-Vision/Device-Creation.png)  

- Retrieve your connection credentials and update the config.json file with your new connection credentials and camera setting.

```
	"IoTJumpWaySettings": {
		"SystemLocation": 0,
		"SystemZone": 0,
		"SystemDeviceID": 0,
		"SystemDeviceName" : "Your Device Name",
		"SystemCameraID":0
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

## Video Stream

The video stream is off by default, to turn on the video stream update the AppServerSettings settings in config.json. The video stream requires SSL, follow the next step that explains how to set up your domain name and SSL to point to your Raspberry Pi 3. 

```
	"AppServerSettings":{
		"serverOn":1,
		"serverIP":"YOUR RPI 3 IP",
		"serverUser":"YOUR SERVER USERNAME",
		"serverPassword":"YOUR SERVER PASSWORD"
	}
```

## Setup Domain Name For Your Raspberry Pi 3

COMING SOON

## Training Your Data

Now that the basics are set up, it is time to train your model with your own photos. When you download this repo, there will already be a trained model and processed images in the processed folder, but this model will not recognise you. You should make a good selection of photos of yourself in different positions and lighting. The more photos you train your model on, the more accurate it will be, if your device is not identifying you you simply need to train it with more images of yourself. 

You can add as many images as you like (Dependant on the space available on your RPI 3), for as many people as you like. To add training data navigate to the training folder and create a directory, the directory should be a number, and not a number that is already in the processed folder. 

Once you have built up your folder of images, head over to TASS.py and change line 34 (self.train = 0) to self.train = 1 and the start the program. The program will loop through your images and if it detects a face it will recreate an image in the format required for the model, save it to a matching folder in the processed directory, and delete the original image to save space. If it does not detect a face it will simply delete the original image as it is useless for the facial recognition. 

Once the processing stage has finished, your new model will automatically start training, once training is finished, it will automatically run the main facial recognition program. Put your face in front of your connected webcam and watch the output of the program as it tries to identify who you are. 

## Viewing Your Data  

Each time your device detects a person or an intruder, it will send data to the [TechBubble IoT JumpWay](https://iot.techbubbletechnologies.com/ "TechBubble IoT JumpWay"). You will be able to access the data in the [TechBubble IoT JumpWay Developers Area](https://iot.techbubbletechnologies.com/developers/dashboard/ "TechBubble IoT JumpWay Developers Area"). Once you have logged into the Developers Area, visit the [TechBubble IoT JumpWay Location Devices Page](https://iot.techbubbletechnologies.com/developers/location-devices "Location Devices page"), find your device and then visit the Sensor/Actuator page and the Warnings page to view the data sent from your device.

![IoT JumpWay Raspberry Pi Computer Vision Example Docs](../../images/Computer-Vision/SensorData.png)

![IoT JumpWay Raspberry Pi Computer Vision Example Docs](../../images/Computer-Vision/WarningData.png)

## Autonomous Device Communication

COMING SOON

## Executing The Program

    $ sudo python/python3 TASS.py 

## IoT JumpWay Raspberry Pi Computer Vision Example Bugs/Issues

Please feel free to create issues for bugs and general issues you come accross whilst using the IoT JumpWay Raspberry Pi Computer Vision Example. You may also use the issues area to ask for general help whilst using the IoT JumpWay Raspberry Pi Computer Vision Example in your IoT projects.




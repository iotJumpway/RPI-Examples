# IoT JumpWay Raspberry Pi Computer Vision Example (TASS)

![TechBubble Autonomous Sight System](img/TASS-Banner.png) 

## Introduction

Here you will find sample device scripts for connecting Raspberry Pi to the TechBubble Technologies IoT JumpWay using the Python MQTT Library and OpenCV for computer vision. The codes allow you to set up a basic device that allows you to train a Haarcascades model, detect recognised / unknown people, monitor the camera in near realtime via a stream, and communicate with the IoT JumpWay sending sensor and warning messages. Once you understand how it works you are free to add as many actuators and sensors to your device and modify your code accordingly.

This example was our original version of TASS, since our move forward with more advanced computer vision libraries and frameworks, we decided to open up the source code.

## Before You Begin

If this is the first time you have used the TechBubble IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following link and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications.

[TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs")

You will need to setup your Raspberry Pi 3 in a certain way to be able to use this example, please follow the document below to prepare your Raspberry Pi 3.

[Raspberry Pi 3 Preparation Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/1-Raspberry-Pi-Prep.md "Raspberry Pi 3 Preparation Doc")

You will need to install OpenCV for this example to work, please follow the document below to install OpenCV on your Raspberry Pi 3.

[Raspberry Pi 3 OpenCV Installation Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/2-Installing-OpenCV.md "Raspberry Pi 3 OpenCV Installation Doc")

The video stream requires SSL, it would be irresponsible to provide options for insecure projects using our platform, below you will find a document that explains how to set up your domain name and SSL to point to your Raspberry Pi 3. 

COMING SOON
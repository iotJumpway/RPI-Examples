# Installation Of Linux Motion On Raspberry Pi

![TechBubble IoT JumpWay Docs](../images/main/Raspberry-Pi-Documentation.png)

## Introduction

The following information will help you install Linux Motion on your Raspberry Pi.

PLEASE NOTE: 

- This is a basic tutorial that will result in an insecure stream, in project tutorials where we use Linux Motion, we will take you through creating a secure stream. 
- Motion will store images and videos on your Raspberry Pi, if you do not keep on top of them your diskspace will quickly fill up, check out section 10 of this guide for more info. 

## Hardware Requirements

1. Raspberry Pi

## Guide

1. Update your packages and install Motion:

    ```
        $ sudo apt-get update
        $ sudo apt-get upgrade
        $ sudo apt-get install motion
    ```

2. Execute the following to open up the configuration file:

    ```
        $ sudo nano /etc/motion/motion.conf
    ```

3. Make the following changes:

    ```
        DAEMON = OFF
        stream_localhost off
    ```
    
4. If you want to change the port that the webcam is streamed to change the following value. It is a good idea to change the port so that it does not use the default port.

    ```
        stream_port = 8081
    ```

5. In my case I am using a camera that is 1280 x 780, motion may not work if you do not have the correct resolution set for your camera, to modify the dimensions find and edit the following in the config file:

    ```
        width 640 
        height 380
    ```

6. If you want to change the quality of the images and video stream, change the following line:

    ```
        quality 90
        stream_quality 90
    ```

7. We want our stream to be as fast possible, in order to do so, find and modify the following line, I use 30 as my camera is 30 fps:

    ```
        framerate 2
        stream_maxrate 1
    ```

8. If you want to be able to see where it picks up motion on the stream, set the following to on:

    ```
        locate_motion_mode off
    ```

9. If you want to change the location that the images and videos are saved to, change the following location:

    ```
        target_dir 
    ```

    If you change this value you should make sure you have given the correct permissions for Motion:

    ```
        chgrp motion PATH_TO_YOUR_DIRECTORY
        chmod g+rwx PATH_TO_YOUR_DIRECTORY
        chmod -R g+w PATH_TO_YOUR_DIRECTORY
    ```

10. Using Motion with the default settings will result in images being saved to the target_dir which will eventually use up all of your diskspace. If you would like to turn this feature off so that only videos are saved, find and edit the following line: 

    ```
        output_pictures off
    ```

11. Close the file and save your changes.

12. Execute the following to open up the daemon configuration:  

    ```
        $ sudo nano /etc/default/motion
    ```

13. Make the following change: 

    ```
        start_motion_daemon = yes
    ```

14. Check Linux Motion is working, execute the following command and then navigate to YOUR_RPI_IP:8081 

    ```
        sudo service motion start
    ```

These are just some settings that we think will be useful to you, review the full motion.conf file for all possible settings.

## IoT JumpWay Intel® Edison Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../images/main/Intel-Software-Innovator.jpg)  
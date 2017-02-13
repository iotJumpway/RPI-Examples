# Installation Of OpenCV 3.2.0 On Raspberry Pi

![TechBubble IoT JumpWay Docs](../images/main/Raspberry-Pi-Documentation.png)

## Introduction

The following information will help you install the latest version of OpenCV, 3.2.0, on your Raspberry Pi. This installation includes the additional modules required for facial identification.

## Hardware Requirements

1. Raspberry Pi.
2. 16 GB Card

## Software Requirements

1. Jessie

## Guide

1. Update apt-get:

    ```
    $ sudo rpi-update
    $ sudo apt-get update
    $ sudo apt-get upgrade
    ```

2. Install developer tools:

    ```
    $ sudo apt-get install build-essential cmake cmake-curses-gui pkg-config
    ```

3. Install required libraries:

    ```
    $ sudo apt-get install \
        libjpeg-dev \
        libtiff5-dev \
        libjasper-dev \
        libpng12-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libeigen3-dev \
        libxvidcore-dev \
        libx264-dev \
        libgtk2.0-dev
    ```

4. Install libraries used to optimize OpenCV:

    ```
    $ sudo apt-get install libatlas-base-dev gfortran
    ```

5. Install Python development libraries & Numpy:

    ```
    $ sudo apt-get install python2.7-dev
    $ sudo apt-get install python3-dev
    ```

6. Install Numpy:

    ```
    $ pip install numpy
    $ pip3 install numpy
    ```

7. Create a directory to home OpenCV and enter it:

    ```
    $ mkdir opencv && cd opencv
    ```

8. Checkout current OpenCV 3.2.0 & the contribs:

    ```
    $ wget https://github.com/opencv/opencv/archive/3.2.0.zip -O opencv_source.zip
    $ wget https://github.com/opencv/opencv_contrib/archive/3.2.0.zip -O opencv_contrib.zip
    ```

9. Unzip the code:

    ```
    $ unzip opencv_source.zip
    $ unzip opencv_contrib.zip
    ```

10. Move into the 3.2.0 directory, make the build dir and move into it:

    ```
    $ cd ~/opencv/opencv-3.2.0 && mkdir build && cd build
    ```

11. Configure the build:

    ```
    $ sudo cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D BUILD_WITH_DEBUG_INFO=OFF \
        -D BUILD_DOCS=OFF \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_TESTS=OFF \
        -D BUILD_opencv_ts=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=ON \
        -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.2.0/modules \
        -D ENABLE_NEON=ON \
        -D WITH_LIBV4L=ON \
            ../
    ```
12. If everything went ok you should see the following:

    ```
    -- Configuring done
    -- Generating done
    ```

13. Build OpenCV, grab a beer as this will take a while, come back and check at intervals to see if there has been any errors:

    ```
    $ sudo make -j4
    ```

14. Once complete you should see the following: 

    ```
    [100%] Built target ...
    ```

15. Install OpenCV:

    ```
    $ sudo make install
    $ sudo ldconfig
    ```

16. Test the installation:

    ```
    $ python/python3
    >> import cv2
    >> print (cv2.__version__)
    >> import face
    ```

17. If you do not see any errors here, congratulations, you have successfully installed the latest version of OpenCV on your Raspberry Pi, grab another beer to celebrate your accomplishment.

## IoT JumpWay Raspberry Pi Documentation & Tutorials Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Raspberry Pi Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Raspberry Pi Examples in your IoT projects.

## IoT JumpWay Raspberry Pi Documentation & Tutorials Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../images/main/Intel-Software-Innovator.jpg)  
    

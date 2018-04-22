# Installation Of SECURE Nginx Server For Motion On Raspberry Pi

![IoT JumpWay Docs](../images/main/Raspberry-Pi-Documentation.png)

## Introduction

The following information will help you install a secure Nginx server for your Motion stream on your Raspberry Pi.

## Hardware Requirements

1. Raspberry Pi

## Before You Begin

Before you begin you should follow the tutorials below as this tutorial is for securing the Linux Motion stream, you should follow the [Installing Linux Motion On Your Raspberry Pi](https://github.com/iotJumpway/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/4-Securing-Your-Raspberry-Pi-With-IPTables.md "Installing Linux Motion On Your Raspberry Pi") tutorial first. This tutorial will not work without following the [Setup Domain Name & SSL For Your Raspberry Pi](https://github.com/iotJumpway/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/3-Raspberry-Pi-Domain-And-SSL.md "Setup Domain Name & SSL For Your Raspberry Pi") tutorial.

- [Installing Linux Motion On Your Raspberry Pi](https://github.com/iotJumpway/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/4-Securing-Your-Raspberry-Pi-With-IPTables.md "Installing Linux Motion On Your Raspberry Pi")

- [Setup Domain Name & SSL For Your Raspberry Pi](https://github.com/iotJumpway/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/3-Raspberry-Pi-Domain-And-SSL.md "Setup Domain Name & SSL For Your Raspberry Pi")

- [Securing Your Raspberry Pi With IPTables](https://github.com/iotJumpway/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/4-Securing-Your-Raspberry-Pi-With-IPTables.md "Securing Your Raspberry Pi With IPTables")

## Guide

1. Update your packages and install Nginx:

    ```
        $ sudo apt-get update
        $ sudo apt-get upgrade
        $ sudo apt-get install nginx
    ```

2. Start Nginx and check it is working by visting the IP address of your Raspberry Pi:

    ```
        $ sudo service nginx start
    ```

3. Execute the followin commands, this will take some time so kick back with a beer.

    ```
        $ cd /etc/nginx
        $ sudo openssl dhparam -out dh2048.pem 2048
    ```

4. After following the [Setup Domain Name & SSL For Your Raspberry Pi](https://github.com/iotJumpway/IoT-JumpWay-RPI-Examples/blob/master/_DOCS/3-Raspberry-Pi-Domain-And-SSL.md "Setup Domain Name & SSL For Your Raspberry Pi") tutorial, place your ca.crt, crt.crt and key.key files into the /etc/nginx folder.

5. Execute the following to open up the configuration file:

    ```
        $ sudo nano /etc/nginx/sites-enabled/default
    ```

6. Replace its contents with the following:

    ```
        server {
        listen 80;
        return 301 https://$host$request_uri;
        }
        server {
            listen 443 ssl;
            server_name YOUR_DOMAIN_NAME;

            add_header Strict-Transport-Security max-age=31536000;
            ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
            ssl_ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS;
            ssl_buffer_size 8k;
            ssl_prefer_server_ciphers on;
            ssl_session_cache shared:SSL:30m;
            ssl_session_timeout 30m;

            ssl_certificate          /etc/nginx/crt.crt;
            ssl_certificate_key      /etc/nginx/key.key;

            ssl_stapling on;
            resolver 8.8.8.8;
            ssl_stapling_verify on;

            ssl_dhparam  /etc/nginx/dh2048.pem;
            ssl_trusted_certificate  /etc/nginx/ca.crt;

            location / {
                proxy_pass http://YOUR_RPI_IP:YOUR_MOTION_STREAM_PORT;
            }

        }
    ```

7. Replace the following in the above script:

    ```
        YOUR_DOMAIN_NAME -> Your SSL secured domain name
        YOUR_RPI_IP -> Your Raspberry Pi IP address
        YOUR_MOTION_STREAM_PORT -> The port on your Raspberry Pi that you set Motion to stream to
    ```

8. Reload / Restart Nginx:

    ```
        sudo service nginx reload
    ```

10. Commands to reload / start / stop the Nginx server:

    ```
        sudo service nginx start
        sudo service nginx stop
        sudo service nginx reload
    ```

## Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Raspberry Pi Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Raspberry Pi Examples in your IoT projects.

## Contributors

[![Adam Milton-Barker, Intel® Software Innovator](../images/main/Intel-Software-Innovator.jpg)](https://github.com/AdamMiltonBarker)
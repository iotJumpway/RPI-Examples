
# Setup Domain Name & SSL For Your Raspberry Pi 3

![TechBubble IoT JumpWay Docs](../images/main/IoT-Jumpway.jpg)  

## Introduction

To help ensure that data passed between your Raspberry Pi 3 and any connecting web services is encrypted an important thing to do is to add SSL encryption to your requests. The following information will help you setup a domain name for your Raspberry Pi, forward the domain to your device IP, and secure the connection with SSL.

## Guide

1. Ensure your local network has a static IP, you will be able to purchase one from your ISP. You can use service such as no-ip.com but this is not the preferred method and is out of the scope of this tutorial.

2. Ensure all ports are closed on your router with the exception of ones that you need for your applications.

3. Purchase a domain name and install it on a web server, I get mine from NameCheap.com. In the following steps we will use subdomain of this domain to point towards your local network.

4. Purchase your SSL certificate, I get mine from NameCheap.com, when you buy a domain name from Namecheap you can get an SSL for $1.99 for the first year.

5. Once your domain is installed on your server, find and edit the domain zone file to include a sub domain that uses an A record to point to the static IP of your local network.

6. Set up a port forward from your router to the local IP address of your Raspberry Pi 3.

7. Login to your Raspberry Pi via SSH and generate an RSA key and a CSR that will be used to activate your SSL certificate. Use the following command to generate your RSA key:

    ```
    $ openssl genrsa -out ~/PATH_TO_YOUR_CERT_FOLDER/YOUR_KEY_FILE.key 2048
    ```

8. Use the following command to generate your CSR:

    ```
    $ openssl req -new -sha256 -key ~/PATH_TO_YOUR_CERT_FOLDER/YOUR_KEY_FILE.key -out ~/PATH_TO_YOUR_CERT_FOLDER/YOUR_CSR_FILE.csr
    ```


9. You will be asked a few questions at this stage, complete them all but ensure to not enter a password when prompted to, just hit enter.

10. Head over to where you bought the SSL certificate from and activate your SSL cert using the CSR you generated on your Raspberry Pi, once verified you will receive your SSL certificate files.

11. Connect to your Raspberry Pi using SFTP, for this I always WinSCP on Windows but you can use FileZilla or the FTP client of your choice. Once connected upload your SSL cert files to your certs folder specified in the related guide for the project you are setting up.
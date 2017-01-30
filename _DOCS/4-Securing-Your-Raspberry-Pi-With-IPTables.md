# Securing Your Raspberry Pi With IPTables

![TechBubble IoT JumpWay Docs](../images/main/IoT-Jumpway.jpg)  

## Introduction

If youa re going to have your Raspberry Pi accessible via the outside world, the minimum security step you should take is to ensure that only ports that you absolutely require to be open are open. IPTables allows you to specify which ports are accessible on your Raspberry Pi by blocking them all and allowing access to only the ports that you white list. IPTables has a lot of features and methods here are the basics:

## Guide

1. Check that IPTables is installed using the following command, if it is, you will see a message saying so, if it is not, it will be installed:

    ```
    $ sudo apt-get install iptables
    ```
    
2. If/once installed you can check your current configs by running one of the following commands:

    ```
    $ sudo iptables -L
    ```
    or

    ```
    $ sudo iptables -L -v
    ```

3. Next, create a new config file for IPTables and modify the code to your liking. This will block all traffic to your Raspberry Pi except SSH and the specified ports you white list. To create your new config file you would issue the following command: (I am using nano but you can use your favorite text editor)

    ```
    $ sudo nano /etc/iptables
    ```

4. Next, add the following code and modify to your preference (You may need to remove indentation and whitespace):

    ```
    *filter

    # Allow all loopback (lo0) traffic and drop all traffic to 127/8 that doesn't use lo0

    -A INPUT -i lo -j ACCEPT

    -A INPUT -d 127.0.0.0/8 -j REJECT

    # Accept all established inbound connections

    -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

    # Allow all outbound traffic - you can modify this to only allow certain traffic

    -A OUTPUT -j ACCEPT

    # Allow HTTP and HTTPS connections from the port number you specified in your project config.json file, replace YOUR PORT NUMBER with your specified port number.

    -A INPUT -p tcp --dport YOUR PORT NUMBER -j ACCEPT

    # Allow SSH connections, the -dport number should be the same port number you set in sshd_config

    -A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT

    # Allow ping

    -A INPUT -p icmp -j ACCEPT

    # Log iptables denied calls

    -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

    # Drop all other inbound - default deny unless explicitly allowed policy

    -A INPUT -j DROP

    -A FORWARD -j DROP

    COMMIT
    ```

5. Once you have modified and saved your config file, add a rule to /etc/network/interfaces by opening it:
  
    ```
        $ sudo nano /etc/network/interfaces
    ```

6. To ensure that the firewall is loaded each and everytime you boot up your Raspberry Pi, add the following line to the end of the file then save:
  
    ```
        pre-up iptables-restore < /etc/network/iptables
    ```

7. Load the new rules:
  
    ```
        $ sudo iptables-restore /etc/network/iptables
    ```

8. Check if it has worked, you should see the rules you added in the output of the following command.
  
    ```
        $ sudo iptables-save
  
    ```

9. Reboot your Raspberry Pi and your firewall should boot up on startup everytime now.
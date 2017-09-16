# Robot_Project
Entry-level Mobile Robot
This project is meant to document my projects in robotics. I do not provide enough information on to how everything should be set up as a basic README file wouldn't be comprehensive enough.

A. Software prerequisites 
  1. pigpio by Joan. Download the python library at http://abyz.co.uk/rpi/pigpio/download.html;
  2. Python 3.X (latest version);
  3. FileZila, VNC viewer and Putty (or any other similar programs) on a PC.
  
B. Hardware prerequisites
  1. Raspberry Pi 2/3 model B;
  2. Two DC motors (no encoders are required);
  3. H-bridge based motor controller;
  4. HC-SR04;
  5. Servo motor;
  6. 7.4V Battery with 5V voltage regulators;
  7. 1k and 600 ohms resistors;
  8. Jumper wires;
  9. Wifi Dongle for the RPi.

C. Installation

  0. Connect your RPi to wifi and make sure you can remotely ssh and VNC into it.
  1. Transfer all the files of the repository to a folder in your RPi with FileZila or git clone https://github.com/ferasboulala/Robot_Project/tree/master/Robot_Project_GUI;
  2. Connect all the hardware together. You should refer to Robot.py to know where to connect the GPIOs. Mount the Ultrasonic Sensor on top of the servo. We assume a general knowledge of how to power up everything (i.e. not connecting directly the 7.4V battery to the RPi but using voltage regulators instead, making sure the voltage regulators can give enough current without melting, etc.)
  3. Open Robot.py with Python 3 (IDLE) and press F5;
  4. Follow the instructions on screen.

![Alt text](IMG_20170823_213321905.jpg?raw=true "Mobile_Robot")

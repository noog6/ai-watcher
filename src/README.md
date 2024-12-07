# AI-Watcher
A Python-based framework for a stationary robot that observes its environment. Runs on a Raspberry Pi Zero W (1.1 or 2) controller.

## Description
This project is currently in its early stages, but it is following a microservice architecture and endpoints have already been started for low level hardware. The rest we can figure out along the way...

## Quick Start
To launch the application use the following:
```
git clone https://github.com/noog6/ai-watcher.git
cd ai-watcher
python api.py
```

If you are looking for the web interfaces, the following activities can be found here:

Dashboard:
http://rpi-hostname:5000/

## Installation
### Hardware

* Download and print the structural components (https://github.com/noog6/MicroQuad)
* Assemble mechanical and electrical systems - Add Link to guide

### Software

* Download and install Linux onto a SD card using RPimager ([Find Raspberry Pi OS (Legacy) Lite 32-bit - Bullseye](https://www.raspberrypi.com/software/operating-systems/))
* RPimager can also pre-setup network connection, hostname, user account/password and enable SSH
* Insert SD card in-to RPi Zero W and boot --> if you are lucky and it connects to your wifi, then you can SSH into the system
* Login using the pi account with the password configured earlier
* Open the Raspberry Pi configuration application and enable the interface hardware listed below:
```
sudo raspi-config
```
* section 3 - Interface Options, enable I2C --> Yes
* section 3 - Interface Options, enable Serial Port -> Yes
* exit out of the raspi-config app (esc), then run:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip python3-smbus git libasound-dev portaudio19-dev python-all-dev libsndfile1 joystick ffmpeg python3-picamera2
```
Now we can setup the Audo Hat (Mic+ v2 RaspiAudio.com): (from https://forum.raspiaudio.com/t/mic-installation-guide/17)
```
wget -O - mic.raspiaudio.com | bash
```
* Say yes to install the software
* Say yes a second time for the reboot
* After the system reboots, log back in and run the following command test to verify the audio installation is functioning:
```
wget -O - test.raspiaudio.com | bash
```
You will have to push the onboard audio board button to test. You should hear “Front Left ... front Right”, then the audio recorded sequence by the microphone.

Now you can grab the git repo:
```
git config --global credential.helper store
git config --global user.name 'noog6'
git config --global user.password 'use_token_from_github'
git clone https://github.com/noog6/ai-watcher.git
```
Then we can continue with our setup:
```
cd ai-watcher
pip install -r requirements.txt
```
Adjust the default.yaml configuration file to match your robot's specifications:
```
vi config/default.yaml
```
Save the above file.
Now we can start the ai-watcher application:
```
python api.py
```

## Calibration and Setup
* Ensure proper servo ids are mapped to specific joints - Add Link to guide
* Calibrate Servos - Add Link to guide
* Servo Calibration Interface - http://rpi-hostname:5000/calibrate


## Configure Automatic Startup with System

(From ai-watcher/ai-watcher.daemon.service)
To setup the ai-watcher application so that it automatically starts on system startup:

1) Copy the service file into the systemd area
```
sudo cp ai-watcher.daemon.service /lib/systemd/system/
```
2) Refresh system cache for services
```
sudo systemctl daemon-reload
```
3) Make our service start on boot
```
sudo systemctl enable ai-watcher.daemon.service
```
4) Force ai-watcher Engine to start now
```
sudo service ai-watcher.daemon start
```

# Quick Reference for interacting with the service:

start service
```
sudo service ai-watcher.daemon start
```

restart service
```
sudo service ai-watcher.daemon restart
```

stop service
```
sudo service ai-watcher.daemon stop
```

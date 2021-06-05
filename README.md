# python_snippets_for_raspberry_pi
Should run on all Raspberry Pi verisons, tested on Pi Model 3 B + and Model 4

# Prepare Raspberry Pi Environment
Open Terminal respectively your command line tool

Update
```
sudo apt-get update && sudo apt-get upgrade
```
Activate I2C
```
sudo raspi-config
```
Restart
```
sudo reboot
```
Install packages
```
sudo apt-get install python3 python3-pip
pip3 install smbus2
```
run script in command line
```
python3 script.py
```

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
sudo apt-get install python3 python3-pip i2c-tools
pip3 install smbus2
```
Check if your sensor is detected
```
sudo i2cdetect -y -r 1 
```
run script in command line
```
python3 script.py
```

# Directly communicate with a SFM3019 using i2c tools
```
i2cdetect  -y 1
i2cset -y 1 0x2e 0x36 0x61
i2ctransfer -y 1 w3@0x2e 0x36 0x61 r9
i2ctransfer -y 1 w1@0x2e 0x00 r9
```

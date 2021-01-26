#!/usr/bin/python
# (c) Copyright 2020 Sensirion AG, Switzerland

# Example to use a Sensirion SFM3019 with a Raspbery Pi
# 
# Prerequisites: 
#
# - open the command line tool
#
# - Enable the i2c interface on your Raspbery Pi
# using 'sudo raspi-config'
#
# - Install python3 and pip3 and some tools
# 'sudo apt-get install python3 python3-pip i2c-dev i2c-tools wget'
#
# - Install the smbus2 library
# 'pip3 install smbus2'
#
# - Check if the sensor is recognized on the i2c bus
# executing the command 'i2cdetect -y 1'
# the result should look like this:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- 2e -- 
#
# - Retrieve this example file from github
# 'wget -L https://raw.githubusercontent.com/Fototux/python_snippets_for_raspberry_pi/main/sfm3019.py'
#
# - Run the example 'python3 sfm3019.py'

import time
from smbus2 import SMBus, i2c_msg

# I2C bus 1 on a Raspberry Pi 3B+
# SDA on GPIO2=Pin3 and SCL on GPIO3=Pin5
# sensor +5V at Pin2 and GND at Pin6
DEVICE_BUS = 1

# device address SFM3019
DEVICE_ADDR = 0x2e

# init I2C
bus = SMBus(DEVICE_BUS)

#wait 1 s for sensor start up (> 2 ms according to datasheet)
time.sleep(1)

# offset and scale factor needed to convert sensor flow raw data
# could be also used from datasheet (scale = 170, offset = -24576)
# read offset and scale factor for Gas 1: Air
# command 0x36 0x61
# with parameter 0x36 0x08
# with crc for the two bytes parameter: 0xd0
msg = i2c_msg.write(DEVICE_ADDR, [0x36, 0x61, 0x36, 0x08, 0xd0])
bus.i2c_rdwr(msg)
# read 9 bytes, MSB, LSB, CRC -> scale factor, offset, unit
msg = i2c_msg.read(DEVICE_ADDR, 9)
bus.i2c_rdwr(msg)

scale = msg.buf[0][0]<<8 | msg.buf[1][0]
offset = msg.buf[3][0]<<8 | msg.buf[4][0]
# pyhton receives bytes as unsigned
# convert to signed value
offset = offset if offset < (1 << 16-1) else offset - (1 << 16)
print("Scale, Offset")
print (scale, offset)

# send start continuous measurement command to the sensor  (0x3608)
# start in continuous mode for Gas 1: Air
msg = i2c_msg.write(DEVICE_ADDR, [0x36, 0x08])
bus.i2c_rdwr(msg)

# repeat read out of sensor data
for i in range(10):
    # wait for  first measurement for 30 ms
    # after first measurement update rate can be set to a higher value
    time.sleep(1)
    # read 9 bytes, MSB, LSB, CRC -> flow, temperature, status
    msg = i2c_msg.read(DEVICE_ADDR, 6)
    bus.i2c_rdwr(msg)
    # merge byte 0 and byte 1 to integer
    flow_raw = msg.buf[0][0]<<8 | msg.buf[1][0]
    # convert from unsigned to signed
    flow_raw = flow_raw if flow_raw < (1 << 16-1) else flow_raw - (1 << 16)

    # calculate flow according to datasheet section 4.5.2
    # SFM3019: offset = -24576; scale 170
    # scale and offset values taken from i2c readout at the beginning
    flow = (flow_raw - offset)/scale

    # merge byte 3 and byte 4 to integer
    temperature = msg.buf[3][0]<<8 | msg.buf[4][0]
    # calculate temperature  according to sectino 4.5.3 in the datasheet
    scale = 200.
    temperature = temperature / scale
    print("{:.2f},{:.2f}".format(flow, temperature))

# stop the measurement
# if measurement has not been stopped,
# sending the start command again will result in i2c error
msg = i2c_msg.write(DEVICE_ADDR, [0x3F, 0xF9])
bus.i2c_rdwr(msg)

bus.close()



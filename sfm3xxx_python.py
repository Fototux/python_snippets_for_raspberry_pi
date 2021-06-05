#!/usr/bin/python
import time
from smbus2 import SMBus, i2c_msg

# I2C bus 1 on a Raspberry Pi 3B+
# SDA on GPIO2=Pin3 and SCL on GPIO3=Pin5
# sensor +5V at Pin2 and GND at Pin6
DEVICE_BUS = 1

# device address SFM3300
DEVICE_ADDR = 0x40

# init I2C
bus = SMBus(DEVICE_BUS)

#wait 1 s for sensor start up (> 100 ms according to datasheet)
time.sleep(1)

# send start continuous measurement command to the sensor  (0x1000)
msg = i2c_msg.write(DEVICE_ADDR, [0x10, 0x00])
bus.i2c_rdwr(msg)

# repeat read out of sensor data
for i in range(10):
    time.sleep(1)
    # read 3 bytes, MSB, LSB, CRC
    msg = i2c_msg.read(DEVICE_ADDR, 3)
    bus.i2c_rdwr(msg)
    # merge byte 0 and byte 1 to integer
    flow_raw = msg.buf[0][0]<<8 | msg.buf[1][0]
    # calculate flow according to datasheet section 2.3
    # SFM3300: offset = 32768; scale 120
    flow = (flow_raw - 32768)/120.
    print(flow)

bus.close()

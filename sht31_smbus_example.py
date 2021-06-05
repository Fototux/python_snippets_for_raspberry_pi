#!/usr/bin/python
import time
from smbus2 import SMBus, i2c_msg

# I2C bus 1 on a Raspberry Pi 3B+
# SDA on GPIO2=Pin3 and SCL on GPIO3=Pin5
# sensor +3V3 at Pin2 and GND at Pin6
DEVICE_BUS = 1

# device address SHT31
DEVICE_ADDR = 0x44

# init I2C
bus = SMBus(DEVICE_BUS)

#wait 1 s for sensor start up (> 1 ms according to datasheet)
time.sleep(1)

for _ in range(10):
    # send measurement command for non periodic high repeatability to the sensor (0x2400)
    msg = i2c_msg.write(DEVICE_ADDR, [0x24, 0x00])
    bus.i2c_rdwr(msg)

    # wait for measurement (15.5)
    time.sleep(1)

    # read 6 bytes; t: MSB, LSB, CRC; rh: MSB, LSB, CRC
    msg = i2c_msg.read(DEVICE_ADDR, 6)
    bus.i2c_rdwr(msg)

    # merge byte 0 and byte 1 to int16_t
    t_raw = msg.buf[0][0]<<8 | msg.buf[1][0]
    rh_raw = msg.buf[3][0]<<8 | msg.buf[4][0]

    # calculate according to datasheet section
    t = -45 + 175 * (t_raw/65535)
    rh = 100 * (rh_raw/65535)

    print(("{0:.1f}\t{1:.1f}").format(t, rh))

bus.close()

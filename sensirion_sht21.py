#!/usr/bin/python
"""
Created on Tue Nov 03 22:35:14 2015

@author:  dlehmann
"""

import smbus
import time
import io
import fcntl
from raspi_i2c import RaspiI2c

# measurement duration + 1ms (for security) for each resolution,
WAIT_TABLE = {0: 0.086, 1: 0.029}

OTP_START_ADDRESS   =   102
OTP_READ_SERIAL     =   123
OTP_READ_CALIB_IDX  =   125

SHT_ADDRESS = 0x40

class Sht21Driver():

    def __init__(self, i2c, bus):
        self.i2c = i2c
        self.bus = bus

    def measure_sample(self):
        self._start_measuring(type='temperature')
        time.sleep(WAIT_TABLE[0])
        temperature_adc = self._read_measuring()

        self._start_measuring(type='humidity')
        time.sleep(WAIT_TABLE[1])
    	humidity_adc = self._read_measuring()

        return self._humidity_conversion(humidity_adc), self._temperature_conversion(temperature_adc),


    def _start_measuring(self, type='temperature'):
        if type == 'temperature':
            command = 0xf3
        else:
            # humidity
            command = 0xf5
    	self.i2c.i2c_write(self.bus, SHT_ADDRESS, [command])

    def _read_measuring(self):
        result = self.i2c.i2c_read(self.bus,SHT_ADDRESS, 3)
        return  result[0] << 8 | result[1]

    def _humidity_conversion(self, humidity_adc):
        return -6.0 + 125.0/65536 * humidity_adc; 

    def _temperature_conversion(self, temperature_adc):
        return -46.85 + 175.72/65536 * temperature_adc;


if __name__ == "__main__":
    i2c = RaspiI2c()
    sht21 = Sht21Driver(i2c, bus=1)
    humidity, temperature = sht21.measure_sample()
    print humidity, temperature


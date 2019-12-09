#!/usr/bin/env python

import time
from pms5003 import PMS5003, ReadTimeoutError
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


#define pm

pms5003 = PMS5003()
readings = pms5003.read()

def pm1():
	return (readings.pm_ug_per_m3(1.0))
	

def pm25():
	pm25_reading = (readings.pm_ug_per_m3(2.5))
	return pm25_reading
	pm25_reading.flush()
	
def pm10():
	pm10_reading = (readings.pm_ug_per_m3(10.0))
	return pm10_reading
	pm10_reading.flush()



	
	#input from calling function acts as request for specific pm(2.5/1/10)
#e.g. pm25=pm(2.5)


#BME sensor function

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

def temp():
	return(bme280.get_temperature())


# main function

def main():
	while True:
		print(temp())
		time.sleep(5)
		
main()
	
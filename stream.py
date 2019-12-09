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
	readings = pms5003.read()
	pm1_reading = (readings.pm_ug_per_m3(1.0))
	pm1_reading = "{:.0f} PM 2.5".format(pm1_reading)
	return pm1_reading
	pm1_reading.flush()

def pm25():
	readings = pms5003.read()
	pm25_reading = (readings.pm_ug_per_m3(2.5))
	return pm25_reading
	pm25_reading.flush()
	
def pm10():
	readings = pms5003.read()
	pm10_reading = (readings.pm_ug_per_m3(10.0))
	return pm10_reading
	pm10_reading.flush()



	
	#input from calling function acts as request for specific pm(2.5/1/10)
#e.g. pm25=pm(2.5)


#BME sensor function

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

def temp():
	temperature = (bme280.get_temperature())
	temperature = "{:.1f} *C".format(temperature)
	return temperature
	
def humidity():
	humidity = bme280.get_humidity()
	humidity = "{:.0f} %".format(humidity)
	return humidity
	
def pressure():
	 pressure = bme280.get_pressure()
	 pressure = "{:.1f} hPa".format(pressure)
	 return pressure


# main function

def main():
	while True:
		print(pm1())
		print(pm25())
		print(pm10())
		print(temp())
		print(humidity())
		print(pressure())
		time.sleep(5)
		
main()
	
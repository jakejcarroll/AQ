#!/usr/bin/env python

def bme():
	import time
	from bme280 import BME280
	
	try:
	    from smbus2 import SMBus
	except ImportError:
	    from smbus import SMBus
	
	bus = SMBus(1)
	bme280 = BME280(i2c_dev=bus)
	
	temperature = bme280.get_temperature()
	pressure = bme280.get_pressure()
	humidity = bme280.get_humidity()

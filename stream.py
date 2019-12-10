#!/usr/bin/env python

import time
from pms5003 import PMS5003, ReadTimeoutError
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
    
import atexit
import ads1015
import RPi.GPIO as GPIO

from ISStreamer.Streamer import Streamer

from enviroplus import gas

# --------- User Settings ---------
BUCKET_NAME = "Monitoring"
BUCKET_KEY = "6Q4MFAKM3HPD"
ACCESS_KEY = "ist_cE0zFD5C1Y5DSKWsSGxIBcTRIOVqPO_x"
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)


#define pm functions

pms5003 = PMS5003()

def pm1():
	readings = pms5003.read()
	pm1_reading = (readings.pm_ug_per_m3(1.0))
	pm1_reading = "{:.0f}".format(pm1_reading)
	return pm1_reading
	pm1_reading.flush()

def pm25():
	readings = pms5003.read()
	pm25_reading = (readings.pm_ug_per_m3(2.5))
	pm25_reading = "{:.0f}".format(pm25_reading)
	return pm25_reading
	pm25_reading.flush()
	
def pm10():
	readings = pms5003.read()
	pm10_reading = (readings.pm_ug_per_m3(10.0))
	pm10_reading = "{:.0f} ".format(pm10_reading)
	return pm10_reading
	pm10_reading.flush()


#BME sensor functions

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

def temp():
	temperature = (bme280.get_temperature())
	temperature = "{:.1f} *C".format(temperature)
	return temperature
	temperature.flush()
	
def humidity():
	humidity = bme280.get_humidity()
	humidity = "{:.0f} %".format(humidity)
	return humidity
	humidity.flush()
	
def pressure():
	 pressure = bme280.get_pressure()
	 pressure = "{:.1f} hPa".format(pressure)
	 return pressure
	 pressure.flush()

#gas functions

def nh3():
	gas_readings = gas.read_all()
	nh3 = gas_readings.nh3
	nh3 = (nh3/1000)
	nh3 = "{:.2f}".format(nh3)
	return nh3
	
def ox():
	gas_readings = gas.read_all()
	ox = gas_readings.oxidising
	ox = (ox/1000)
	ox = "{:.2f} ".format(ox)
	return ox
	
def red():
	gas_readings = gas.read_all()
	red = gas_readings.reducing
	red = (red/1000)
	red = "{:.2f}".format(red)
	return red
	
#CO / Carbon Monoxide 

def CO():
	co = 0.00
	red = 0
	gas_readings = gas.read_all()
	red = gas_readings.reducing
	red_ratio = (red / 74)
	co = ((red_ratio**-1.177)*4.4638)
	co = "{:.2f}".format(co)
	return co
	
def ethanol():
	gas_readings = gas.read_all()
	red = gas_readings.reducing
	print(red)
	red_ratio = (red / 74)
	print(red_ratio)
	ethanol = ((red_ratio**-1.58)*1.363)
	print("%.5f" % ethanol)
	ethanol = "{:.2f}".format(ethanol)
	print(ethanol + " PPM")
	return ethanol
	
def nh3_ethanol():
	gas_readings = gas.read_all()
	nh3 = gas_readings.nh3
	print(nh3 + " nh3")
	nh3_ratio = (nh3 / 72)
	print(nh3_ratio + " ratio")
	ethanol = ((nh3_ratio**-2.781)*0.2068)
	print("%.5f" % ethanol + " PPM")
	ethanol = "{:.2f}".format(ethanol)
	print(ethanol + " PPM")
	return ethanol

# main function

def main():
	while True:
		streamer.log("Temperature ", temp())
		streamer.log("PM1.0", pm1())
		streamer.log("PM2.5", pm25())
		streamer.log("PM10.0", pm10())
		streamer.log("Humidity", humidity())
		streamer.log("Pressure", pressure())
		streamer.log("NH3", nh3())
		streamer.log("Oxidising", ox())
		streamer.log("Reducing", red())
		streamer.log("Carbon Monoxide ", "PPM", CO())
		streamer.log("Ethanol ", "PPM", ethanol())
		time.sleep(2)
		
while True:
	ethanol()
	print("/")
	print("/")
	nh3_ethanol()
	time.sleep(2)
	
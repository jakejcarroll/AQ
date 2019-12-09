#!/usr/bin/env python

import time
from pms5003 import PMS5003, ReadTimeoutError
import logging

#define pm

pms5003 = PMS5003()
readings = pms5003.read()

def pm1():
	pm1_reading = (readings.pm_ug_per_m3(1.0))
	return pm1_reading

def pm25():
	pm25_reading = (readings.pm_ug_per_m3(2.5))
	return pm25_reading
	
def pm10():
	pm10_reading = (readings.pm_ug_per_m3(10.0))
	return pm10_reading

pm10()


	
	#input from calling function acts as request for specific pm(2.5/1/10)
#e.g. pm25=pm(2.5)


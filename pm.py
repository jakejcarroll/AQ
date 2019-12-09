#!/usr/bin/env python

import time
from pms5003 import PMS5003, ReadTimeoutError
import logging

pm1_reading = float

pms5003 = PMS5003()

readings = pms5003.read()

def pm1():
	pm1_reading = (readings.pm_ug_per_m3(1.0))
	return pm1_reading
	
print(pm1())
	
pm25 = (readings.pm_ug_per_m3(2.5))
pm10 = (readings.pm_ug_per_m3(10))
      

#!/usr/bin/env python

import time
from pms5003 import PMS5003, ReadTimeoutError
import logging

pms5003 = PMS5003()

readings = pms5003.read()

pm1 = (readings.pm_ug_per_m3(1.0))

print(pm1)
      

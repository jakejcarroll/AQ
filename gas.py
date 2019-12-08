#!/usr/bin/env python

import time
from enviroplus import gas
import logging


readings = gas.read_all()

print(readings)
        

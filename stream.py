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

# --------- User Settings ---------
BUCKET_NAME = "sensor"
BUCKET_KEY = "QCK8NUHE59FU"
ACCESS_KEY = "ist_cE0zFD5C1Y5DSKWsSGxIBcTRIOVqPO_x"
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

#gas global variables

MICS6814_HEATER_PIN = 24
MICS6814_GAIN = 6.144

ads1015.I2C_ADDRESS_DEFAULT = ads1015.I2C_ADDRESS_ALTERNATE
_is_setup = False
_adc_enabled = False
_adc_gain = 6.148


#define pm functions

pms5003 = PMS5003()

def pm1():
	readings = pms5003.read()
	pm1_reading = (readings.pm_ug_per_m3(1.0))
	pm1_reading = "{:.0f} PM1.0".format(pm1_reading)
	return pm1_reading
	pm1_reading.flush()

def pm25():
	readings = pms5003.read()
	pm25_reading = (readings.pm_ug_per_m3(2.5))
	pm25_reading = "{:.0f} PM2.5".format(pm25_reading)
	return pm25_reading
	pm25_reading.flush()
	
def pm10():
	readings = pms5003.read()
	pm10_reading = (readings.pm_ug_per_m3(10.0))
	pm10_reading = "{:.0f} PM10.0".format(pm10_reading)
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


#********************* GAS.py ************************

class Mics6814Reading(object):
    __slots__ = 'oxidising', 'reducing', 'nh3', 'adc'

    def __init__(self, ox, red, nh3, adc=None):
        self.oxidising = ox
        self.reducing = red
        self.nh3 = nh3
        self.adc = adc

    def __repr__(self):
        fmt = """Oxidising: {ox:05.02f} Ohms
Reducing: {red:05.02f} Ohms
NH3: {nh3:05.02f} Ohms"""
        if self.adc is not None:
            fmt += """
ADC: {adc:05.02f} Volts
"""
        return fmt.format(
            ox=self.oxidising,
            red=self.reducing,
            nh3=self.nh3,
            adc=self.adc)

    __str__ = __repr__


def setup():
    global adc, _is_setup
    if _is_setup:
        return
    _is_setup = True

    adc = ads1015.ADS1015(i2c_addr=0x49)
    adc.set_mode('single')
    adc.set_programmable_gain(MICS6814_GAIN)
    adc.set_sample_rate(1600)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MICS6814_HEATER_PIN, GPIO.OUT)
    GPIO.output(MICS6814_HEATER_PIN, 1)
    atexit.register(cleanup)


def enable_adc(value=True):
    """Enable reading from the additional ADC pin."""
    global _adc_enabled
    _adc_enabled = value


def set_adc_gain(value):
    """Set gain value for the additional ADC pin."""
    global _adc_gain
    _adc_gain = value


def cleanup():
    GPIO.output(MICS6814_HEATER_PIN, 0)


def read_all():
    """Return gas resistence for oxidising, reducing and NH3"""
    setup()
    ox = adc.get_voltage('in0/gnd')
    red = adc.get_voltage('in1/gnd')
    nh3 = adc.get_voltage('in2/gnd')

    try:
        ox = (ox * 56000) / (3.3 - ox)
    except ZeroDivisionError:
        ox = 0

    try:
        red = (red * 56000) / (3.3 - red)
    except ZeroDivisionError:
        red = 0

    try:
        nh3 = (nh3 * 56000) / (3.3 - nh3)
    except ZeroDivisionError:
        nh3 = 0

    analog = None

    if _adc_enabled:
        if _adc_gain == MICS6814_GAIN:
            analog = adc.get_voltage('ref/gnd')
        else:
            adc.set_programmable_gain(_adc_gain)
            time.sleep(0.05)
            analog = adc.get_voltage('ref/gnd')
            adc.set_programmable_gain(MICS6814_GAIN)

    return Mics6814Reading(ox, red, nh3, analog)


def read_oxidising():
    """Return gas resistance for oxidising gases.

    Eg chlorine, nitrous oxide
    """
    setup()
    return read_all().oxidising


def read_reducing():
    """Return gas resistance for reducing gases.

    Eg hydrogen, carbon monoxide
    """
    setup()
    return read_all().reducing


def read_nh3():
    """Return gas resistance for nh3/ammonia"""
    setup()
    return read_all().nh3


def read_adc():
    """Return spare ADC channel value"""
    setup()
    return read_all().adc

#********************* GAS.py ************************


# main function

def main():
	while True:
		streamer.log("Temperature ", temp())
		streamer.log("PM1.0", pm1())
		streamer.log("PM2.5", pm25())
		streamer.log("PM10.0", pm10())
		streamer.log("Humidity", humidity())
		streamer.log("Pressure", pressure())
		streamer.log("nh3", read_all().nh3)
		time.sleep(2)
		
main()
	
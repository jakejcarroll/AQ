import pm
import bme
import gas

while True:
	pm.pm1()
	print(pm1_reading)
	pm1_reading.flush()
	time.sleep(2)
	
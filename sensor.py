import pm
import bme
import gas

while True:
	print(pm.pm1_reading())
	pm1_reading.flush()
	time.sleep(2)
	
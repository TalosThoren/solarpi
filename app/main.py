#!/usr/bin/env python
import time
import logging
import RPi.GPIO as GPIO
from drivers.DFRobot_INA219 import INA219
from drivers.DFRobot_MAX17043 import MAX17043

#logging.basicConfig( filename="./testing.log" )

'''
Revise the following two paramters according to actual reading of the INA219 and the multimeter
for linearly calibration
'''
batteryGauge219_reading_mA = 1000
ext_meter_reading_mA = 1000
# Setup Watt Meter
wattMeter = INA219( 1, INA219.INA219_I2C_ADDRESS4 )
while not wattMeter.begin():
    print( 'Watt Meter Initialization Failure' )
    sleep( 2 )
wattMeter.linear_cal( batteryGauge219_reading_mA, ext_meter_reading_mA )

# Setup Battery Gauge
batteryGauge = MAX17043()

GPIO.setmode( GPIO.BOARD )
GPIO.setup( 18, GPIO.IN )

# Battery Gauge Interrupt
def interruptCallBack( channel ):
    batteryGauge.clearInterrupt()
    print( 'Low power alert interrupt triggered!' )

GPIO.add_event_detect( 18, GPIO.FALLING, callback = interruptCallBack, bouncetime = 5 )

rslt = batteryGauge.begin()

while rslt != 0:
    print( 'Battery Gauge Initialization Failure' )
    time.sleep( 2 )
    rslt = batteryGauge.begin()

batteryGauge.setInterrupt( 32 )

def main():
      time.sleep(1)
      print( 'voltage: ' + str(batteryGauge.readVoltage()) + 'mV' )
      print( 'percentage: ' + str(round( batteryGauge.readPercentage(), 2 )) + '%' )
      print( 'wattMeter: ' + str(_readSensorValues()) )

def _readSensorValues():
    sensorValues = {
        "ShuntVoltage": wattMeter.get_shunt_voltage_mV(),
        "BusVoltage": wattMeter.get_bus_voltage_V(),
        "CurrentMilliAmps": wattMeter.get_current_mA(),
        "PowerMilliWatts": wattMeter.get_power_mW()
    }
    return sensorValues

if __name__ == '__main__':
    main()

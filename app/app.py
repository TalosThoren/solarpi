import time
import logging
import json
import RPi.GPIO as GPIO
from drivers.DFRobot_INA219 import INA219
from drivers.DFRobot_MAX17043 import MAX17043
import paho.mqtt.client as mqtt

# Battery Gauge Interrupt
def interruptCallBack( channel ):
    batteryGauge.clearInterrupt()
    print( 'Low power alert interrupt triggered!' )

def on_publish( client, userdata, result ):
    print( 'INFO: Data published' )

class App:
    wattMeter = 0
    batteryGauge = 0

    broker = 'homeserver'
    port = 1883

    mqttClient = 0

    '''
    Revise the following two paramters according to actual reading of the INA219 and the multimeter
    for linearly calibration
    '''
    def __init__( self, intReadingMa = 1000, extReadingMa = 1000 ):
        # Setup Watt Meter
        self.wattMeter = INA219( 1, INA219.INA219_I2C_ADDRESS4 )
        while not self.wattMeter.begin():
            print( 'Watt Meter Initialization Failure' )
            sleep( 1 )
        self.wattMeter.linear_cal( intReadingMa, extReadingMa )

        # Setup Battery Gauge
        self.batteryGauge = MAX17043()

        GPIO.setmode( GPIO.BOARD )
        GPIO.setup( 18, GPIO.IN )

        GPIO.add_event_detect( 18, GPIO.FALLING, callback = interruptCallBack, bouncetime = 5 )

        while not self.batteryGauge.begin():
            print( 'Battery Gauge Initialization Failure' )
            time.sleep( 1 )

        self.batteryGauge.setInterrupt( 32 )

        # Set up mqtt client
        self.mqttClient = mqtt.Client()
        self.mqttClient.on_publish = on_publish
        self.mqttClient.connect( self.broker, self.port )

    def readSensorValues( self ):
        time.sleep( 1 )
        return {
            "wattMeter0": {
                "ShuntVoltage": self.wattMeter.get_shunt_voltage_mV(),
                "BusVoltage": self.wattMeter.get_bus_voltage_V(),
                "CurrentMilliAmps": self.wattMeter.get_current_mA(),
                "PowerMilliWatts": self.wattMeter.get_power_mW()
            },
            "batteryGauge": {
                "batteryPercentage": self.batteryGauge.readPercentage(),
                "batteryVoltage": self.batteryGauge.readVoltage()
            }
        }

    def publishMqttMsg( self, topic, msg ):
        return self.mqttClient.publish( topic, msg )

    def run( self ):
        while True:
            self.publishMqttMsg( 'solarpi/sensors', str(self.readSensorValues()) )

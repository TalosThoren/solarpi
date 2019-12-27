# Solar Pi Project

The solar pi project is a makeshift solar panel computer intended for
experimenting with solar power production and management. The codebase is in
alpha phases, and the prototype is a very cobbled together collection of wires,
sensors, and a raspberry pi zero w. Many components are literally glued
together.

As such, the alpha code will be very target specific. No attempts will be made
to support multiple chips and sensors at first, and if you're using something
different, I may need your help supporting it.

The solarpi-sensor-services tool is a service that polls the connected i2c
sensors. Our goal is to establish support for logging sensor readings,
displaying sensor readings to the screen on request, and regularly exporting
sensor readings to an MQTT broker.

## The Sensors

The prototype solarpi computer incorporates the following power sensor modules:

- DFR0563 (DFRobot module using the Maxim MAX17043 lithium-ion feul gauge chip)
- SEN0291 (DFRobot module using the TI INA219 wattmeter chip)

## Solar Power Manager

The prototype uses a DFRobot DFR0535 - 9V/12V/18V Solar Power Manager board. The
battery is actually somewhat paultry, a 2500 mAh lithium-ion from Adafruit.

# You may need to go into the driver for the rest of your hardware and comment out the 'Rain =' line. 
# If you are using the GW1000 driver and there is no rain sensor communicating with the GW1000, no change is needed.

import weewx
from weewx.engine import StdService
from gpiozero import Button
import datetime
import time
import logging

log = logging.getLogger(__name__)

DRIVER_NAME = "GPIORainGauge"
DRIVER_VERSION = "1.1"

class GpioRainGauge(StdService):
    def __init__(self, engine, config_dict):
        super(GpioRainGauge, self).__init__(engine, config_dict)
        d = config_dict.get('GPIORainGauge', {})
        self.gauge = RainGauge(**d)
        self.bind(weewx.NEW_LOOP_PACKET, self.load_data)

    def load_data(self, event):
        try:
            self.get_rain(event)
        except Exception as e:
            log.error("GPIORainGauge: cannot read value: %s" % e)

    # Get Rainfall data
    def get_rain(self, event):
        rainfall = round(self.gauge.get_rainfall(),5)
        if rainfall != 0.00000:
            log.info("Found rain value of %s mm" % rainfall)
        else:
            log.debug("Found rain value of %s mm" % rainfall)
        event.packet['rain'] = float(rainfall)
        
    # Cleanup the gpio pin if the Engine is shut down, or GPIOZero will throw error GPIOPinInUse when engine restarts
    def shutDown(self):
        self.gauge.release_pin()
        
class RainGauge(object):
    """ Object that represents a Wired Rain Gauge. """

    def __init__(self, **d):
        """ Initialize Object. """
        # Read from config the bucket size
        self.bucket_size = float(d.get('bucket_size'))
        self.rain_count = 0
        # Read from config which pin to use on the RPI GPIO
        self.rain_sensor = Button(d.get('pin_number'))
        log.debug("Rainbucket configured, GPIO pin: %s, bucket size: %s mm", d.get('pin_number'), d.get('bucket_size'))
        self.rain_sensor.when_pressed = self.bucket_tipped

    def bucket_tipped(self):
        self.rain_count = self.rain_count + 1
        log.debug("Rain bucket tipped, current count: %s", self.rain_count) 

    def get_rainfall(self):
        rainfall = (self.rain_count * self.bucket_size)
        self.reset_rainfall()
        return rainfall

    def reset_rainfall(self):
        self.rain_count = 0
        
    def release_pin(self):
        log.warning("Releasing GPIO pin %s with .close()", d.get('pin_number'))
        self.rain_sensor.close()

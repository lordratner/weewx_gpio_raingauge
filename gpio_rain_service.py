#You need to go into the driver for the rest of your hardware and comment out the 'Rain =' line.

import syslog
import weewx
from weewx.engine import StdService
from gpiozero import Button
import datetime
import time

DRIVER_NAME = "GPIORainGauge"
DRIVER_VERSION = "1.0"

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
            syslog.syslog(syslog.LOG_ERR, "GPIORainGauge: cannot read value: %s" % e) 

    # Get Rainfall data
    def get_rain(self, event):
        rainfall = round(self.gauge.get_rainfall(),2)
        syslog.syslog(syslog.LOG_DEBUG, "GPIORainGauge: found rain value of %s cm" % rainfall)
        event.packet['rain'] = float(rainfall)
    
    
class RainGauge(object):
    """ Object that represents a Wired Rain Gauge. """

    def __init__(self, **d):
        """ Initialize Object. """
        # Read from config the bucket size
        self.bucket_size = float(d.get('bucket_size'))
        self.rain_count = 0
        # Read from config which pin to use on the RPI GPIO
        self.rain_sensor = Button(d.get('pin_number'))
        self.rain_sensor.when_pressed = self.bucket_tipped
        
    def bucket_tipped(self):
        self.rain_count = self.rain_count + 1
        
    def get_rainfall(self):
        rainfall = (self.rain_count * self.bucket_size)
        self.reset_rainfall()
        return rainfall

    def reset_rainfall(self):
        self.rain_count = 0    


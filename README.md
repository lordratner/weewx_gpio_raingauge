# weewx_gpio_raingauge
Extra service for supporting wired rain gauges connected through GPIO pins on Weewx. This is a service, not a driver, so it will either supplement your existing weather station if there is no rain gauge, or replace the rain gauge only. 

### Requirements

1. Raspberry Pi
1. Weewx installed and configured
1. A wired rain gauge (such as the RainWise RAINEW111) with one wire connected to a GPIO pin, the other connected to ground.

### Installation Instructions

Copy gpio_rain_service.py into your user folder: /usr/share/weewx/user/

```wget https://github.com/lordratner/weewx_gpio_raingauge/blob/main/gpio_rain_service.py -O /usr/share/weewx/user/gpio_rain_service.py```

Open weewx.conf: ```nano /etc/weewx/weewx.conf```

Go to the [Engine] --> [[Services]] section and find ```"data-services = "```

Add " user.gpio_rain_service.GpioRainGauge". If there are already services listed, add a comma before adding the new entry. It should look something like this:
```
[Engine]

    # The following section specifies which services should be run and in what order.
    [[Services]]
        prep_services = weewx.engine.StdTimeSynch
        data_services = user.gpio_rain_service.GpioRainGauge,
        process_services = weewx.engine.StdConvert, weewx.engine.StdCalibrate, weewx.engine.StdQC, weewx.wxservices.StdWXCalculate
        xtype_services = weewx.wxxtypes.StdWXXTypes, weewx.wxxtypes.StdPressureCooker, weewx.wxxtypes.StdRainRater, weewx.wxxtypes.StdDelta
        archive_services = weewx.engine.StdArchive
        restful_services = weewx.restx.StdStationRegistry, weewx.restx.StdWunderground, weewx.restx.StdPWSweather, weewx.restx.StdCWOP, weewx.restx.StdWOW, $
        report_services = weewx.engine.StdPrint, weewx.engine.StdReport
```

Now add a section for the configuration variables and update them for your setup:
```
[GPIORainGauge]

    #Enter the size of your rain gauge's tipping bucket or spoon
    bucket_size = .1

    #GPIO pin for rain gauge wire. Other wire goes to GND
    pin_number = 6

    #You need to go into the driver for the rest of your hardware and comment out the 'Rain =' line.
```

This is the hardest part, you need to open your driver and comment out the rain reporting. This will be different for every driver, but you are looking for the line ```rain = ```. Just comment it out: ```#rain = ```.  The drivers are located in either ```/usr/share/weewx/weewx/drivers``` (changes here will not survive a WeeWx upgrade) or ```/usr/share/weewx/user``` (Changes here will be preserved in an upgrade).

Now just restart WeeWx: ```sudo systemctl restart weewx```

That should be it. 

Special thanks to these two repositories, used in constructing this service.
https://github.com/eyesnz/weewx_pi_sensors and https://github.com/jardiamj/BYOWS_RPi

# weewx_gpio_raingauge
Extra service for supporting wired rain gauges connected through GPIO pins on Weewx. This is a service, not a driver, so it will either supplement your existing weather station if there is no rain gauge, or replace the rain gauge only. 

### Requirements

1. Raspberry Pi
1. Weewx installed and configured
1. A wired rain gauge (such as the RainWise RAINEW111) with one wire connected to a GPIO pin, the other connected to ground.

### Installation Instructions

(Your folders may vary depending on the installation. This uses the Debian installation. Sudo may be required for certain commands)

Copy gpio_rain_service.py into your user folder: /usr/share/weewx/user/

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

    #Enter the size of your rain gauge's tipping bucket or spoon *in milimeters*
    bucket_size = .254

    #GPIO pin for rain gauge wire. Other wire goes to GND
    pin_number = 6

    #You need to go into the driver for the rest of your hardware and comment out the 'Rain =' line.
```

This is the hardest part, depending on the driver, you may need to open your driver and comment out the rain reporting. This will be different for every driver, but in the simulator you are looking for the line ```rain = ```. Just comment it out: ```#rain = ```.  The drivers are located in either ```/usr/share/weewx/weewx/drivers``` (changes here will not survive a WeeWx upgrade) or ```/usr/share/weewx/user``` (Changes here will be preserved in an upgrade).

For the GW1100 driver, if you have no rain equipment (that communicates with the GW1000/GW1100), no changes are required. If you are replacing a rain sensor with a wired gauge, you'll need to disable the rain sensor in the GW1100 setup. If you can't do that, you need to go into the driver and disable the rain functions, which is difficult. 

Now just restart WeeWx: ```sudo systemctl restart weewx```

That should be it. 

Special thanks to these two repositories, used in constructing this service.
https://github.com/eyesnz/weewx_pi_sensors and https://github.com/jardiamj/BYOWS_RPi

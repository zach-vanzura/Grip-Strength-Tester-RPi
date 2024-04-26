#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import time

try:
    hx711 = HX711(
        dout_pin=5,
        pd_sck_pin=6,
        channel='A',
        gain=64
    )

    hx711.reset()   # Before we start, reset the HX711 (not obligate)
    print("No strain applied")
    measures = hx711.get_raw_data(5)
    print(measures)
    print(max(measures))

    hx711.reset()
    time.sleep(3)


    print("1.2 ish kg (1200 grams)")
    strain_measures = hx711.get_raw_data(5)
    print(strain_measures)
    print(max(strain_measures))
    print("Difference:")
    print(max(strain_measures) - max(measures))

    hx711.reset()
    time.sleep(5)

    print("Zach's grip, about 46 - 47 kg")
    zach_strain = hx711.get_raw_data(5)
    print(zach_strain)
    print(max(zach_strain))
    print("Difference:")
    print(max(zach_strain) - max(measures))

finally:
    GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

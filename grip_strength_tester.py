#!/usr/bin/python3
from hx711 import HX711  # import the class HX711
import RPi.GPIO as GPIO  # import GPIO
import time

# global variables for HX711
VOutPin = 1
DataPin = 6
ClockPin = 5
NumReadings = 10
# this is roughly 8.3 million but i think I need to reduce it by a factor of 10
# this is the highest digital output that the ADC is capable of outputting
MAX_STRAIN = 0x7fffff
# optional offset constant if strain gauge is warped
# OFFSET = 17500
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def read_input():
    """
    - read input from load cell
    - polls every second for a minimum strain level of 100 grams before reading data
    - reads data for 5 seconds
    :return the max of the aggregate of readings
    :rtype float

    """
    hx = HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=128, channel='A')
    # rest HX711
    hx.reset()

    # poll every second for an applied strain
    strain_applied = hx.get_raw_data()
    # raw data min is 100 grams
    min_strain_needed = 100000
    # can add an offset constant if strain gauge is warped
    while (max(strain_applied)) < min_strain_needed:
        print("Waiting for min strain")
        time.sleep(1)
        strain_applied = hx.get_raw_data()

    raw_strain_data = []
    # read data for 5 seconds
    print("Reading strain.")
    end_time = time.time() + 5
    # maximize readings by processing after 5 seconds
    while time.time() < end_time:
        read = hx.get_raw_data()
        # get_raw_data returns a list, add each value to strain_data to prevent a list of lists
        raw_strain_data.append(read)
    # raw_strain_data is a list of lists, process to get one full list of data
    processed_data = []
    for index in raw_strain_data:
        for _ in index:
            processed_data.append(_)
    # max output is 0x7FFFFF which is around 8.3 million
    # since the change in voltage when strain is applied is pretty linear,
    # the reading we get is proportional to the

    # dividing by 1000 seems to get the right data in grams
    # but could be different when using actual strain gauge
    return max(processed_data) / 1000


if __name__ == '__main__':
    print("Reading Data")
    data = read_input()
    print(f'{data:.2f} grams')
    print(f'Which is {data * 0.0022046} pounds')

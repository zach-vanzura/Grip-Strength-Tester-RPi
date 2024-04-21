#!/usr/bin/python3
from hx711 import HX711  # import the class HX711
import RPi.GPIO as GPIO  # import GPIO
import time

# global variables for HX711
VOutPin = 1
DataPin = 6
ClockPin = 5
NumReadings = 10
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
    # make sure data is ready to be read

    hx = HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=128, channel='A')
    # poll every second for an applied strain
    # raw data is in milligrams, min is 100 grams
    strain_applied = hx.get_raw_data()
    min_strain_needed = 100000
    print("Waiting for min strain needed:")
    while max(strain_applied) < min_strain_needed:
        print("No strain applied.")
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
    # data is in milligrams, return max in grams
    return max(processed_data) / 1000


if __name__ == '__main__':
    print("Reading Data")
    data = read_input()
    print(data)

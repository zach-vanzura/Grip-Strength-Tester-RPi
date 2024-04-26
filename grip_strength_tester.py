#!/usr/bin/python3
from hx711 import HX711  # import the class HX711
import RPi.GPIO as GPIO  # import GPIO
import time

# global variables for HX711
DataPin = 6
ClockPin = 5
NumReadings = 10
# this is the highest digital output that the ADC is CAPABLE of outputting
MAX_STRAIN = 0x7fffff
# optional offset constant if strain gauge is warped( baseline numbers aren't close to 0)
# baseline output for 120 kg strain gauge is in the range of 155,000 - 163,000
OFFSET = 162000
# this is the max the ADC outputs with maximum strain applied
MAX_OUTPUT = 2637362.7362
MAX_STRAIN_KGS = 120
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

"""

NOTE: Calibration for your load cell will vary depending on its rated range.
for a 120 kg load cell, we are using Zach's grip strength of about 100 pounds, or about 45.4 kg as a reference
to calculate the max output from the chip you must find the ratio of your measurement to the maximum strain capacity
the output for Zach's grip is 1,160,668, accounting for the offset of about 160,000,
45.5 / 120 = 1,000,000 / max raw output. which comes out to be roughly 2,637,362.7362

Finally, to calculate the strain in KGs, one simply takes the ratio of measured output (minus offset) to the maximum output 
and multiplies by the maximum strain rating

"""

def read_input():
    """
    - read input from load cell
    - polls every second for a minimum strain level before reading data
    - reads data while strain is still applied
    :return the max of the aggregate of readings
    :rtype float

    """
    hx = HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=128, channel='A')
    # rest HX711
    hx.reset()

    # poll every second for an applied strain. Don't need more than one read
    strain_applied = hx.get_raw_data(1)
    # min strain is a bit higher than the offset  because it can vary a little bit depending on the handle position
    min_strain_needed = 200000
    while (strain_applied[0]) < min_strain_needed:
        print("Waiting for min strain")
        time.sleep(1)
        strain_applied = hx.get_raw_data(1)

    raw_strain_data = []
    # read data while strain is high enough
    print("Min Strain has been achieved.")
    strain_applied.get_raw_data(1)
    # maximize readings by processing after 5 seconds
    while strain_applied[0] > min_strain_needed:
        read = hx.get_raw_data(1)
        raw_strain_data.append(read[0])

    # account for offset, divide by load cell max output then multiply by max load capacity
    output_data = ((max(raw_strain_data) - OFFSET) / MAX_OUTPUT) * MAX_STRAIN_KGS
    return output_data


if __name__ == '__main__':
    data = read_input()
    print(f'{data:.2f} kilograms')
    print(f'Which is {(data * 2.2046):.2f} pounds')

#!/usr/bin/python3
from hx711 import HX711  # import the class HX711
import RPi.GPIO as GPIO  # import GPIO
import time

# global variables for HX711
DataPin = 6
ClockPin = 5
OFFSET = 157550
# maximum output value using a 120 kg load cell
MAX_OUTPUT = 2681856.82
MAX_STRAIN_KGS = 120
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

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
    strain_applied = hx.get_raw_data()
    # min strain is a bit higher than the offset  because it can vary a little bit depending on the handle position
    min_strain_needed = 200000
    while (max(strain_applied)) < min_strain_needed:
        print("Waiting for min strain")
        time.sleep(1)
        strain_applied = hx.get_raw_data()

    raw_strain_data = []
    # read data while strain is high enough
    print("Min Strain has been achieved.")

    strain_applied = hx.get_raw_data()
    while max(strain_applied) > min_strain_needed:
        raw_strain_data.append(max(strain_applied))
        strain_applied = hx.get_raw_data()

    # account for offset, divide by load cell max output then multiply by max load capacity
    output_data = ((max(raw_strain_data) - OFFSET) / MAX_OUTPUT) * MAX_STRAIN_KGS
    return output_data


if __name__ == '__main__':
    data = read_input()
    print(f'{data:.2f} kilograms')
    print(f'Which is {(data * 2.2046):.2f} pounds')

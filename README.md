# Grip Strength Tester Using a Raspberry Pi  
### By Zach Vanzura and Charlie Nix

## Summary
This project is a grip strength tester using a strain gauge and a Raspberry Pi. 
It uses an HX711 analog to digital signal converter to convert the strain gauge signal to digital signal which the pi can recognize. 
grip_strength_tester.py is a script written for a flask app in order to display the measured strain on a webpage but can be modified based on the demands of the project.

## The Code:
The code is pretty straight forward. It uses the HX711 python library (included in sources) to control the interaction between the strain gauge, ADC chip and the Pi.  

First, code polls the strain gauge for a minimum strain before recording and will be in an idle state until the minimum threshold has been reached. In the code, the threshold is set to 200,000 which is about 50,000 above the output when no strain is applied but this value will vary depending on the sensitivity of the load cell and how close the "zeroed" values are to zero.  

Then, the code aggregates strain data for as long as the user squeezes before returning the maximum.  
One thing to note is that the get_raw_data method in the HX711 library returns a list of data based on the number of readings which means that when aggregating data over time, you are adding lists to the list. In order to have the data all in one big list, each time data is received from the chip, the only value added to the list is the maximum. 


NOTE: The maximum output value of the hx711 is around 8.3 million. However, the actual outputs will vary based on the sensitivity of the load cell and so actual maximum output could be less.  

To interpret the raw data received, the ratio of strain:max strain should be equal to the ratio of raw data (with strain):real maximum raw output. Then, all you need to do is solve for the real max output as you have the other three values.

For a 120 kg load cell, we used a 25 lb weight (11.3398 kg) to calculate the max output from the chip.
The output for 11.4 kgs is about 410,000 including the offset of about 157,550. So,
11.3398 / 120 = 252,450 / max raw output which comes out to be roughly 2,681,856.82.

Finally, to calculate the strain, one simply takes the ratio of measured output (minus offset) to the maximum output (already excluding offset from prior calculations) 
and multiplies by the maximum strain rating in kgs or lbs depending on the desired unit.

##### Sources: https://github.com/mpibpc-mroose/hx711

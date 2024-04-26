# Grip Strength Tester Using a Raspberry Pi  
### By Zach Vanzura and Charlie Nix

## Summary
This project is a grip strength tester using a strain gauge and a Raspberry Pi. 
It uses an HX711 analogue to digital signal converter to convert the analogue strain gauge signal to digital which the pi can recognize. The end goal of the project is to have a strain gauge set up so that a user can squeeze to apply strain which will then be measured and displayed on a website. Ideally, we would like to add some entertainment functionality to the website as well. Such as a loading bar animation that fills up the harder it is squeezed or a display of the ranges of grip strength of animals and where the user falls into that category.

## The Code:
The Code is pretty straight forward. It uses the HX711 python library (included in sources) to control the interaction between the strain gauge, ADC chip and the Pi.  
First, code polls the strain gauge for a minimum strain before recording and will be in an idle state until the minimum threshold has been reached. In the code, the threshold is set to 100,000 which is 100 grams but can be changed according to the strain gauge used.  
Then, the code aggregates strain data for five seconds before returning the maximum.  
One thing to note is that the get_raw_data method in the HX711 library returns a list of data based on the number of readings which means that when aggregating data over time, you are adding lists to the list. In order to have the data all in one big list, after all data is aggregated, the code iterates through the list of lists and adds each value to one list.

##### Sources: https://github.com/mpibpc-mroose/hx711

# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 08:35:34 2017

@author: mkeranen
"""
#Acts as a GUI for the paired Arduino program. User can modify the PWM drive of the LED via GUI and serial com port.
import serial
import matplotlib.pyplot as plt
from time import sleep

#Serial communication with datastream
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4'
ser.open()

#This sets the length of data to be stored in each list, also controls
#the amount of data shown in the figure at once
pltHistoryLength = 20

#Turn on interactive plotting
plt.ion()

#This is an attempt at an input timeout. This function waits 1 second for
#user input (via keyboard interrupt and then input), if it doesnt receive it, 
#it exits the function and enters back into the main loop.
def changeDesiredIntensity():
    
    #Tell the user how to break the loop and enter their desired intensity
    try:
        print("Press 'Ctrl + C', then enter desired intensity: ")
        sleep(.5)
        print ("No input")
    #if user enters keyboard interrupt, prompt for input, and write to serial
    except KeyboardInterrupt:
        print("New input attempt")
        newIntensity = input("Enter desired intensity: ")
        ser.write(str(newIntensity).encode())
    return 0

#Loop to handle data sent in "X,Y,Z" by Arduino. 

def main():
    smoothIntensityList = []
    desiredIntensityList = []
    ledControlList = []
    xList = []
    x=0
    try:
        while x<40: #Change while condition for actual use
            #flush input buffer for fresh data to operate on each loop    
            ser.flushInput()
            line = str(ser.readline())      #read data from serial port
            ledList = line.split(",")     #split data via ','
            
            #Separate items, trim unnecessary characters, cast to float datatype
            smoothIntensity = ledList[0]
            smoothIntensity = float(smoothIntensity[2:])
            desiredIntensity = float(ledList[1])
            ledControl = ledList[2]
            ledControl = float(ledControl[:-5])
            x+=1
            
            #Build array until data reaches length set by 'pltHistoryLength' variable
            if x<pltHistoryLength:
                smoothIntensityList.append(smoothIntensity)
                desiredIntensityList.append(desiredIntensity)
                ledControlList.append(ledControl)
                xList.append(x)
            #Once enough data is captured, append the newest data point and 
            #delete the oldest
            else:
                smoothIntensityList.append(smoothIntensity)
                del smoothIntensityList[0]
                desiredIntensityList.append(desiredIntensity)
                del desiredIntensityList[0]
                ledControlList.append(ledControl)
                del ledControlList[0]
                xList.append(x)
                del xList[0]
            
            #Plot the data received, clear the figure for a fresh re-draw each loop
            plt.clf()
            plt.title('LED PID Control')
            plt.ylabel('Raw Counts')
            plt.xlabel('Data Point #')
            smoothIntLine = plt.plot(xList, smoothIntensityList, 'r-', label='Measured Intensity')
            desiredIntLine = plt.plot(xList, desiredIntensityList, 'b-', label='Desired Intensity')
            ledControlLine = plt.plot(xList, ledControlList, 'g-', label='LED Control')
            plt.legend(loc='upper left')
            plt.show()
            #Need this delay to allow for time to draw each figure
            plt.pause(0.05)
            
            #Check for new desired LED intensity
            changeDesiredIntensity()
            
    except KeyboardInterrupt:
        main()
        
#Start program
if __name__ == '__main__':
    main()
    
#Close the serial port and wait for user input to close figure and terminal
ser.close()
print("Press any key to exit: ")
input()

# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 08:35:34 2017

@author: mkeranen
"""

import serial
import matplotlib.pyplot as plt
#plt.switch_backend("QT5Agg")

#Serial communication with datastream
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM4'
ser.open()

#Initialize lists to store data for plotting
smoothIntensityList = []
desiredIntensityList = []
ledControlList = []
xList = [] 

#This sets the length of data to be stored in each list, also controls
#the amount of data shown in the figure at once
pltHistoryLength = 20

#Turn on interactive plotting
plt.ion()

#Loop to handle data sent in "X,Y,Z" by Arduino
x=0

#Change while condition for actual use
while x<40:
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
    plt.plot(xList, smoothIntensityList, 'r-')
    plt.plot(xList, desiredIntensityList, 'b-')
    plt.plot(xList, ledControlList, 'g-')
    plt.show()
    #Need this delay to allow for time to draw each figure
    plt.pause(0.05)
    
#print for debug
#print(xArray, ", ", smoothIntensityArray, ", ", desiredIntensityArray, ", ", ledControlArray)
#Close the serial port and wait for user input to close figure and terminal
ser.close()
print("Press any key to exit: ")
input()
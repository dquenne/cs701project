"""
Created on Sun Apr 16 18:03:29 2017

@author: Uriel uUlloa Adan
"""

import sys

def incrementPitch(increment):
    if len(sys.argv) > 1:
    	inputfile = open(sys.argv[1], 'r')
    else:
        inputfile = open('input.txt', 'r')
        
    outputfile = open('output-'+str(increment)+".txt", 'w')
        
    for line in inputfile:
        lineArr = line.split() 
        for section in lineArr:
            pitchIndex = section.find("p@")
            if pitchIndex > -1:
                pitch = int(section[pitchIndex+2:pitchIndex+5:])
                pitch = pitch + increment
                print(pitch)
                outputfile.write(section[0:pitchIndex+2])
                outputfile.write(str(pitch).zfill(3))
                outputfile.write(section[pitchIndex+5:]+" ")
            else:
                outputfile.write(section+" ")
        outputfile.write("\n")   
            
    inputfile.close()
    outputfile.close()
    
incrementPitch(-6)
incrementPitch(-5)
incrementPitch(-4)
incrementPitch(-3)
incrementPitch(-2)
incrementPitch(-1)
incrementPitch(1)
incrementPitch(2)
incrementPitch(3)
incrementPitch(4)
incrementPitch(5)
incrementPitch(6)

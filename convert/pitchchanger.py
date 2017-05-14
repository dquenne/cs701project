# pitchchanger.py
# takes in training data for the musical RNN and outputs multiple files
# transposed varying amounts. by default, uses -5, -3, -2, +2, +4, +5
# (line 40)
#
# by Dylan Quenneville, Vaasu Taneja, Uriel Ulloa for CS 701 spring 2017

import sys

usage = "usage:\n\
  python pitchchanger.py [in.txt]"


# for each note in the input file, output transposed note to output file
def incrementPitch(increment):

	#read and write file
	if len(sys.argv) > 1:
		inputfile = open(sys.argv[1], 'r')
		outputfile = open(sys.argv[1][:-4]+'-'+str(increment)+".txt", 'w')
	else:
		inname = input("Input file? ")
		inputfile = open(inname, 'r')
		outputfile = open(inname[:-4]+'-'+str(increment)+".txt", 'w')

	#begin reading through file
	for line in inputfile:
		lineArr = line.split()
		for section in lineArr:
			pitchIndex = section.find("p")
			if pitchIndex > -1 and section[pitchIndex+1] != 'o': # make sure it is not a 'tempo' line
				pitch = int(section[pitchIndex+1:pitchIndex+4:])
				pitch = pitch + increment
			   # print(pitch)
				outputfile.write(section[0:pitchIndex+1])
				outputfile.write(str(pitch).zfill(3))
				outputfile.write(section[pitchIndex+4:]+" ")
			else:
				outputfile.write(section+" ")
		outputfile.write("\n")

	inputfile.close()
	outputfile.close()


# uncomment lines to include additional transpositions

# incrementPitch(-6)
incrementPitch(-5)
# incrementPitch(-4)
incrementPitch(-3)
incrementPitch(-2)
# incrementPitch(-1)
# incrementPitch(1)
incrementPitch(2)
# incrementPitch(3)
incrementPitch(4)
incrementPitch(5)
# incrementPitch(6)

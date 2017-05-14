# outputconvert-batch.py
# convert entire folder of .txt files to .csv files arranged for conversion
# with MIDICSV http://www.fourmilab.ch/webtools/midicsv/
# optionally convert all resulting .csv files to .mid
#
# by Dylan Quenneville, Vaasu Taneja, Uriel Ulloa for CS 701 spring 2017

import os
import sys
import subprocess

usage = "usage:\n\
  python outputconvert-batch.py [options] in-directory out-directory\n\
options:\n\
  -m      expect newline characters between measures\n\
  -v      read velocity information in notes\n\
  -i      read note pitches as intervals instead of pitches\n\
  -voice  manually set output MIDI voice\n\
  -midi   after converting to .csv, use Csvmidi.exe to convert to MIDI"

if (len(sys.argv) < 3):
	print(usage)
	exit()

voice = 0
arg_num = 1
use_velocity = False
use_measure_break = False
use_intervals = False
in_dir = None
out_dir = None
use_midi = False

while (arg_num < len(sys.argv)):
	if (sys.argv[arg_num] == "-voice"): # manually set output MIDI voice
		arg_num += 1
		voice = sys.argv[arg_num]
	elif (sys.argv[arg_num] == "-v"): # include velocity values
		use_velocity = True
	elif (sys.argv[arg_num] == "-midi"): # after converting .txt -> .csv, convert to MIDI
		use_midi = True
	elif (sys.argv[arg_num] == "-m"): # put line break at end of each measure
		use_measure_break = True
	elif (sys.argv[arg_num] == "-i"): # use note intervals instead of pitches
		use_intervals = True
	elif (in_dir == None): # directory with input files
	    in_dir = sys.argv[arg_num]
	elif (out_dir == None): # directory for output files
	    out_dir = sys.argv[arg_num]
	arg_num += 1

for inName in os.scandir(in_dir):
	if inName.name[-4:] == ".txt":
		print('Found txt file: %s' % out_dir+"/"+inName.name)
		if use_intervals:
			os.system("python outputconvert.py " + in_dir+"/"+inName.name + " " + out_dir + "/"+inName.name[:-4]+".csv -i -voice " + voice)
		else:
			os.system("python outputconvert.py " + in_dir+"/"+inName.name + " " + out_dir + "/"+inName.name[:-4]+".csv -voice " + voice)
		if use_midi:
			os.system("Csvmidi.exe " + out_dir+"/"+inName.name[:-4]+".csv" + " " + out_dir + "/"+inName.name[:-4]+".mid")

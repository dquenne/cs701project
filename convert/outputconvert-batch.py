import os
import sys
import subprocess

arg_num = 1
use_velocity = False
use_measure_break = False
use_intervals = False
in_dir = None
out_dir = None

while (arg_num < len(sys.argv)):
	if (sys.argv[arg_num] == "-v"): # include velocity information
		use_velocity = True
	elif (sys.argv[arg_num] == "-m"): # put line break at end of each measure
		use_measure_break = True
	elif (sys.argv[arg_num] == "-i"): # use note intervals instead of pitches
		use_intervals = True
		# out_dir = "../blues-intervals"
	elif (in_dir == None):
	    in_dir = sys.argv[arg_num]
	elif (out_dir == None):
	    out_dir = sys.argv[arg_num]
	arg_num += 1

# if len(sys.argv) > 1:
# else:
# 	csv_dir = input("Input folder? ")

# csv_dir = raw_input("Test set name? ")
# print(os.listdir(csv_dir))
for inName in os.scandir(in_dir):
	print('Found txt file: %s' % out_dir+"/"+inName.name)
	if use_intervals:

		os.system("python outputconvert.py " + in_dir+"/"+inName.name + " " + out_dir + "/"+inName.name[:-4]+".csv -i")
	else:
		os.system("python outputconvert.py " + in_dir+"/"+inName.name + " " + out_dir + "/"+inName.name[:-4]+".csv")

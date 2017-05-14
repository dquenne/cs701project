# inputconvert-batch.py
# convert entire folder of .csv files to .txt files for RNN-training
# .csv files according to MIDICSV http://www.fourmilab.ch/webtools/midicsv/
#
# by Dylan Quenneville, Vaasu Taneja, Uriel Ulloa for CS 701 spring 2017

import os
import sys
import subprocess

usage = "usage:\n\
  python inputconvert-batch.py [options] in-directory out-directory\n\
options:\n\
  -m  write newline characters between measures\n\
  -v  include velocity information in notes\n\
  -i  read note pitches as intervals instead of pitches"

if (len(sys.argv) < 3):
	print(usage)
	exit()

arg_num = 1
use_velocity = False
use_measure_break = False
use_intervals = False
csv_dir = None#"../blues-csv"
out_dir = None#"../blues-txt"

while (arg_num < len(sys.argv)):
	if (sys.argv[arg_num] == "-v"): # include velocity information
		use_velocity = True
	elif (sys.argv[arg_num] == "-m"): # put line break at end of each measure
		use_measure_break = True
	elif (sys.argv[arg_num] == "-i"): # use note intervals instead of pitches
		use_intervals = True
	elif (csv_dir == None):
	    csv_dir = sys.argv[arg_num]
	elif (out_dir == None):
	    out_dir = sys.argv[arg_num]
	arg_num += 1

# if len(sys.argv) > 1:
# else:
# 	csv_dir = input("Input folder? ")

# csv_dir = raw_input("Test set name? ")
# print(os.listdir(csv_dir))
for csvName in os.scandir(csv_dir):
	if use_intervals:
		print('Found csv file: %s' % out_dir+"/"+csvName.name)
		os.system("python inputconvert.py " + csv_dir+"/"+csvName.name + " " + out_dir + "/"+csvName.name[:-4]+".txt -i")
	else:
		os.system("python inputconvert.py " + csv_dir+"/"+csvName.name + " " + out_dir + "/"+csvName.name[:-4]+".txt")

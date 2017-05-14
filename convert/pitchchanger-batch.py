# pitchchanger-batch.py
# calls pitchchanger.py on all files in input directory
# takes in training data for the musical RNN and outputs multiple files
# transposed varying amounts. by default, uses -5, -3, -2, +2, +4, +5
# (line 40)
#
# by Dylan Quenneville, Vaasu Taneja, Uriel Ulloa for CS 701 spring 2017

import os
import sys
import subprocess

usage = "usage:\n\
  python pitchchanger-batch.py [in-directory]"


if len(sys.argv) > 1:
	txt_dir = sys.argv[1]
else:
	txt_dir = input("Input directory? ")

# csv_dir = raw_input("Test set name? ")
# print(os.listdir(csv_dir))
for txtName in os.scandir(txt_dir):
	print('Found txt file: %s' % txtName.name)
	os.system("python pitchchanger.py " + txt_dir+"/"+txtName.name)

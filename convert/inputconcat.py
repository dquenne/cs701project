# inputconcat.py
# concatenate all .txt files in specified folder
#
# by Dylan Quenneville, Vaasu Taneja, Uriel Ulloa for CS 701 spring 2017

import musicdata
import os
import sys
import subprocess

if len(sys.argv) > 1:
	input_dir = sys.argv[1]
else:
	input_dir = input("Input folder? ")

output_file = open(input_dir+".txt", 'w')

# main input loop
for inputName in os.scandir(input_dir):
    input_file = open(input_dir+"/"+inputName.name)
    while (1==1):
        nextline = input_file.readline()
        output_file.write(nextline)
        if (nextline == ''): # End of File
            break
    output_file.write('\n')

input_file.close()
output_file.close()

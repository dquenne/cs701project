# inputconcat.py
# concatenate all input files
#

import musicdata
import os
import sys
import subprocess

if len(sys.argv) > 1:
	input_dir = sys.argv[1]#"../blues-txt"
else:
	input_dir = input("Input folder? ")

# input_dir = "../blues-intervals"
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

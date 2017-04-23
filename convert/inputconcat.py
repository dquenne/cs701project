# inputconcat.py
# concatenate all input files
#

import musicdata
import os
import sys
import subprocess


input_dir = "../blues-txt"
outputf = open("../blues-transposed.txt", 'w')
# main input loop

for inputName in os.scandir(input_dir):
    inputf = open(input_dir+"/"+inputName.name)
    while (1==1):
        nextline = inputf.readline()
        outputf.write(nextline)
        if (nextline == ''): # End of File
            break


inputf.close()
outputf.close()

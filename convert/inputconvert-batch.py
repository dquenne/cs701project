import os
import sys
import subprocess

# if len(sys.argv) > 1:
csv_dir = "../blues-csv"
out_dir = "../blues-txt"
# else:
# 	csv_dir = input("Input folder? ")

# csv_dir = raw_input("Test set name? ")
# print(os.listdir(csv_dir))
for csvName in os.scandir(csv_dir):
	print('Found csv file: %s' % csvName.name)
	os.system("python inputconvert.py " + csv_dir+"/"+csvName.name + " " + out_dir + "/"+csvName.name[:-4]+".txt")

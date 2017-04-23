import os
import sys
import subprocess

if len(sys.argv) > 1:
	txt_dir = sys.argv[1]#"../blues-txt"
else:
	txt_dir = input("Input folder? ")

# csv_dir = raw_input("Test set name? ")
# print(os.listdir(csv_dir))
for txtName in os.scandir(txt_dir):
	print('Found txt file: %s' % txtName.name)
	os.system("python pitchchanger.py " + txt_dir+"/"+txtName.name)

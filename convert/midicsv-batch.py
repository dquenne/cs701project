import os
import sys
import subprocess

# if len(sys.argv) > 1:
midi_dir = "../midi-filtered"
csv_dir = "../midi-filtered-csv"
# else:
# 	midi_dir = input("Input folder? ")

for midi in os.scandir(midi_dir):
	print('Found MIDI file: %s' % midi.name)
	os.system("Midicsv.exe " + midi_dir+"/"+midi.name + " " + csv_dir + "/"+midi.name[:-4]+".csv")

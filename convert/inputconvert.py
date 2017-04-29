# inputconvert.py
# converts CSV (comma-separated value) file to new format for training RNN
#
# TODO:
#  - more efficient note storage?

import musicdata
import sys
import math

usage = "usage:\n\
  python inputconvert.py [options] in.csv out.txt\n\
options:\n\
  -m  write newline characters between measures\n\
  -v  include velocity information in notes\n\
  -i  read note pitches as intervals instead of pitches"

if (len(sys.argv) < 3):
	print(usage)
	exit()


DEFAULT_QUARTER_SUBDIV = 12
# 2: 8th-note precision
# 6: 8th-note and quarter-note triplet precision
# 12: 8th-note triplet and 16th-note precision
quarter_sub = DEFAULT_QUARTER_SUBDIV


# output stores lists which each represent a measure
# within these lists are Note objects, unsorted within the measure
output = {}

# used for scanning through output while outputting
max_measure = 0

# add Note object to output sublist (indexed by measure)
def addNote(new_note):
    if new_note.measure() in output:
        output[new_note.measure()].append(new_note) # actually, we should insert in order
    else:
        output[new_note.measure()] = [new_note]
        global max_measure
        max_measure = max(new_note.measure(), max_measure)

arg_num = 1

use_velocity = False
use_measure_break = False
use_intervals = False
inputcsv = None
outputdata = None

while (arg_num < len(sys.argv)):
    if (sys.argv[arg_num] == "-v"): # include velocity information
        use_velocity = True
    elif (sys.argv[arg_num] == "-m"): # put line break at end of each measure
    	use_measure_break = True
    elif (sys.argv[arg_num] == "-i"): # use note intervals instead of pitches
        use_intervals = True
    elif (inputcsv == None):
        inputcsv = open(sys.argv[1], 'r')
    elif (outputdata == None):
        outputdata = open(sys.argv[2], 'w')
    arg_num += 1


# get input filename or use default
# if len(sys.argv) > 1:
# 	inputcsv = open(sys.argv[1], 'r')
# else:
#     inputcsv = open('testcsv.csv', 'r')


unfinishedpitches = {'p':set(), 'b':set(), 'd':set()} # this keeps track of which notes are unwritten
unfinishednotes = {'p':{}, 'b':{}, 'd':{}} # these are the actual unwritten notes
channeltoinstrument = {} # keep track of which channel goes to which instrument

# main input loop
while (1==1):
    nextline = inputcsv.readline()
    if (nextline == ''): # End of File
        break

    # either note on or note off message
    if ((nextline.find('Note_on_c') >= 0 or nextline.find('Note_off_c') >= 0) and int(nextline.split(", ")[3]) in channeltoinstrument):
        instr = channeltoinstrument[int(nextline.split(", ")[3])]
        if nextline.find('Note_on_c') >= 0 and int(nextline.split(", ")[5]) > 0: # velocity > 0, i.e. note ON
            # note pitch, start time, and velocity are stored, but duration is not known yet, so
            # add to 'unfinished notes' to be written once note_off message is found
            pitch = nextline.split(", ")[4]
            unfinishedpitches[instr].add(pitch)
            unfinishednotes[instr][pitch] = musicdata.Note(nextline, ppq)
            unfinishednotes[instr][pitch].instrument = instr
        else: # velocity = 0, i.e. note OFF
            # once a note off is found, the note's duration can be determined, and thus can be
            # written to the output list
            pitch = nextline.split(", ")[4]
            if pitch in unfinishedpitches[instr]:
                unfinishedpitches[instr].remove(pitch)
                unfinishednotes[instr][pitch].setEndTime(nextline.split(", ")[1])
                addNote(unfinishednotes[instr][pitch])
                unfinishednotes[instr][pitch] = None

    # Program_c message -> set channel's instrument value
    elif (nextline.find('Program_c') >= 0):
        midi_instrument = int(nextline.split(", ")[4])
        if midi_instrument <= 15: # piano and pitched percussion (e.g. vibraphone) categories
            channeltoinstrument[int(nextline.split(", ")[3])] = 'p'
            print('channel {0:d} goes to {1}'.format(int(nextline.split(", ")[3]), 'p'))

    # Header message -> get num clock pulses per quarter note (ppq)
    elif (nextline.find('Header') >= 0):
        linedata = nextline.split(", ")
        ppq = int(linedata[5])

    # Tempo message -> get num clock pulses per quarter note (ppq)
    elif (nextline.find('Tempo, ') >= 0):
        linedata = nextline.split(", ")
        tempo = int(60000000 / int(linedata[3]))

    # Time_signature message -> get time signature
    elif (nextline.find('Time_signature,') >= 0):
        timesig = nextline.split(", ")
        num = timesig[3]
        denom = timesig[4]
        clocksperbeat = timesig[5]

inputcsv.close()

print("writing output now")


# if len(sys.argv) > 2:
# 	outputdata = open(sys.argv[2], 'w')
# else:
#     outputdata = open('output.txt', 'w')

notecount = 0
outputdata.write('new song tempo {0}\n'.format(tempo))

# for each measure, go through each 'measure subdivision' (0..47) and print all
# notes at that measure and subdivision. between subdivisions, write '.' which
# encodes the note spacing
# note that a '.' is not like a rest in sheet music, but rather a time marker;
# notes do not have time value (this enables polyphony)

def pauseFromCount(pausecount):
    s = "_" * math.floor(pausecount / 4)
    s += "." * (pausecount % 4) + " "
    return s

print(max_measure, len(output), 'measures')
pausecount = 0
last_pitch = 60
for measure in range(max_measure+1):
    if measure in output:
        for spot in range(4*quarter_sub): # index by measure subdivision
            for note in output[measure]:
                if note.timeInMeasure() == spot and note.instrument == "p" and note.channel != 9:
                    notecount += 1
                    if (pausecount > 0):
                        outputdata.write(pauseFromCount(pausecount))
                        pausecount = 0
                    if (use_intervals):
                        outputdata.write(note.getTrainingDataNote(use_velocity, last_pitch)+" ")
                        last_pitch = note.getPitch()
                    else:
                        outputdata.write(note.getTrainingDataNote(use_velocity)+" ")
            # outputdata.write(". ")
            pausecount += 1
    else: # empty measure
        outputdata.write("____________")
    if use_measure_break:
        if (pausecount > 0):
            outputdata.write(pauseFromCount(pausecount))
            pausecount = 0
        outputdata.write("\n")

outputdata.close()
print("wrote", notecount, "notes")

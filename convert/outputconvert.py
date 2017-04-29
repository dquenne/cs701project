# outputconvert.py
# converts RNN-produced file to CSV (comma-separated value) to be used with MIDICSV
#
# TODO:

import musicdata
import sys
import heapq

usage = "usage:\n\
  python outputconvert.py [options] in.txt out.csv\n\
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

DEFAULT_PPQ = 384
DEFAULT_TRACKS = {'p':2, 'b':3, 'd':4}
DEFAULT_CHANNELS = {'p':0, 'b':1, 'd':9}

FILE_HEADER = '0, 0, Header, 1, 4, {ppq}\n\
1, 0, Start_track\n\
1, 0, Tempo, {tempo}\n\
1, 0, Time_signature, 4, 2, 24, 8\n\
1, 0, Key_signature, 0, "major"\n\
1, 0, End_track\n'

TRACK_HEADER = '{track}, 0, Start_track\n\
{track}, 0, Text_t, "{track_info}"\n\
{track}, 0, Copyright_t, "{copyright}"\n\
{track}, 0, MIDI_port, 0\n\
{track}, 0, Title_t, "{title}"\n\
{track}, 0, Program_c, {channel}, 0\n\
{track}, 0, Control_c, {channel}, 7, 127\n\
{track}, 0, Control_c, {channel}, 10, 64\n'

END_OF_TRACK = '{track}, {final_time}, End_track\n'

END_OF_FILE = '0, 0, End_of_file\n'

output = {}
max_measure = 0


# get MIDI clock time from measure and submeasure
def getClockTime(measure, submeasure):
	return int(DEFAULT_PPQ*(measure*4+submeasure/quarter_sub))

# get MIDI clock time from measure and submeasure plus duration
def getOffClockTime(measure, submeasure, duration):
	return int(DEFAULT_PPQ*(measure*4+(submeasure+duration)/quarter_sub))

# get actual MIDI/CSV message for a note_on
def getCSVNoteOn(measure, submeasure, pitch, instrument, velocity):
	return '{track}, {time:d}, Note_on_c, {channel}, {pitch:d}, {velocity}\n'.format(
		track=DEFAULT_TRACKS[instrument],
		time=int(DEFAULT_PPQ*(measure*4+submeasure/quarter_sub)),
		channel=DEFAULT_CHANNELS[instrument],
		pitch=pitch,
		velocity=velocity
	)

# get actual MIDI/CSV message for a note_off
def getCSVNoteOff(measure, submeasure, pitch, instrument, duration):
	return '{track}, {time:d}, Note_on_c, {channel}, {pitch:d}, 0\n'.format(
		track=DEFAULT_TRACKS[instrument],
		time=int(DEFAULT_PPQ*(measure*4+(submeasure+duration)/quarter_sub)),
		channel=DEFAULT_CHANNELS[instrument],
		pitch=pitch
	)

# add all note_off messages with time value before 'time'
def fillNoteEndings(outputfile, noteoffs, time):
	while len(noteoffs) > 0 and noteoffs[0][0] <= time:
		outputfile.write(heapq.heappop(noteoffs)[1])

arg_num = 1
use_velocity = False
use_measure_break = False
use_intervals = False
inputfile = None
outputfile = None

while (arg_num < len(sys.argv)):
	if (sys.argv[arg_num] == "-v"):
		use_velocity = True
	elif (sys.argv[arg_num] == "-m"):
		use_measure_break = True
	elif (sys.argv[arg_num] == "-i"): # use note intervals instead of pitches
		use_intervals = True
	elif (inputfile == None):
		inputfile = open(sys.argv[1], 'r')
	elif (outputfile == None):
		outputfile = open(sys.argv[2], 'w')
	arg_num += 1


# # get input filename or use default
# if len(sys.argv) > 1:
# 	inputfile = open(sys.argv[1], 'r')
# else:
# 	inputfile = open('output.txt', 'r')
#
# # get output filename or use default
# if len(sys.argv) > 2:
# 	outputfile = open(sys.argv[2], 'w')
# else:
# 	outputfile = open('finaloutput.csv', 'w')


# heap used to store note_off messages to be written (sorted by midi clock time)
noteoffs = []

# read header, scan for tempo
header = inputfile.readline()
tempo = int(header.split(" ")[3])

measure_ct = 0 # current measure
last_time = 0 # time to be used for End_track message (always last note_off time)
last_pitch = 60 # for use if note pitches are written as intervals

# output file header
outputfile.write(FILE_HEADER.format(ppq=DEFAULT_PPQ, tempo=60000000/tempo))

# output piano track header
outputfile.write(TRACK_HEADER.format(track=2, channel=0, track_info="",copyright="",title="piano"))

def breakLength(s):
	return (s.count('_')*4 + s.count('.'))

# main note input loop
while (1==1):
	submeasure = 0
	nextline = inputfile.readline()
	if (nextline == ''): # End of File
		break
	readnotes = nextline.split(" ")
	fillNoteEndings(outputfile, noteoffs, getClockTime(measure_ct, submeasure))
	for next_note in readnotes:
		if use_measure_break and submeasure >= DEFAULT_QUARTER_SUBDIV*4:
			break
		if len(next_note) > 0 and (next_note[0] == '.' or next_note[0] == '_'): # measure subdivision spacer
			submeasure += breakLength(next_note)
			fillNoteEndings(outputfile, noteoffs, getClockTime(measure_ct, submeasure))
		elif len(next_note) > 3:
			# note format is: i@frq!v_dr
			# i: instrument ('p', 'b', 'd')
			# frq: pitch 000..999,
			# v: velocity 0..7,
			# dr: duration in measure subdivisions 00..99
			try:
				instrument = next_note[0]
				if (use_intervals):
					shift = int(next_note[2:next_note.find('-')])
					if next_note[1] == '~':
						shift *= -1
					pitch = max(min(last_pitch + shift, 127), 0)
					last_pitch = pitch  # remove this line for fun mess-ups
				else:
					pitch = min(int(next_note[1:4]), 127)
				if use_velocity:
					velocity = min(int(next_note[5])*14+1, 128) # pad with 1 to avoid accidental 0-velocity note_off messages
					if (len(next_note) >= 10):
						duration = int(next_note[7:9])
					else:
						duration = 3
				else:
					velocity = 90
					duration = int(next_note[5:7])
				if instrument == 'p': # if it is a piano note
					# print('{0}-> measure {1:d} note pitch {2} dur {3}'.format(note, measure_ct, int(pitch), int(duration)))
					# print(getCSVNoteOn(measure_ct, submeasure, pitch, instrument, velocity))
					outputfile.write(getCSVNoteOn(measure_ct, submeasure, pitch, instrument, velocity))
					heapq.heappush(noteoffs, (getOffClockTime(measure_ct, submeasure, duration), getCSVNoteOff(measure_ct, submeasure, pitch, instrument, duration)))
					last_time = max(int(DEFAULT_PPQ*(measure_ct*4+(submeasure+duration)/quarter_sub)), last_time)
			except:
				print("error:" + next_note)
	measure_ct += 1

fillNoteEndings(outputfile, noteoffs, last_time)

outputfile.write('2, {0:d}, End_track\n'.format(last_time))
outputfile.write('0, 0, End_of_file')

inputfile.close()
outputfile.close()

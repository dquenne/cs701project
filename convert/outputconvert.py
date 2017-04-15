# outputconvert.py
# converts RNN-produced file to CSV (comma-separated value) to be used with MIDICSV
#
# TODO:
#   - use heap to keep track of note-off messages and insert in proper spot
#   -

import musicdata
import sys
import heapq

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

# get input filename or use default
if len(sys.argv) > 1:
	inputfile = open(sys.argv[1], 'r')
else:
    inputfile = open('output.txt', 'r')

# get output filename or use default
if len(sys.argv) > 2:
	outputfile = open(sys.argv[2], 'w')
else:
    outputfile = open('finaloutput.csv', 'w')


# heap used to store note_off messages to be written (sorted by midi clock time)
noteoffs = []

# read header, scan for tempo
header = inputfile.readline()
tempo = int(header.split(" ")[3])

measure_ct = 0 # current measure
last_time = 0 # time to be used for End_track message (always last note_off time)

# output file header
outputfile.write(FILE_HEADER.format(ppq=DEFAULT_PPQ, tempo=60000000/tempo))

# output piano track header
outputfile.write(TRACK_HEADER.format(track=2, channel=0, track_info="",copyright="",title="piano"))

# main note input loop
while (1==1):
    submeasure = 0
    nextline = inputfile.readline()
    if (nextline == ''): # End of File
        break
    readnotes = nextline.split(" ")
    for next_note in readnotes:
        if next_note[0] == '.': # measure subdivision spacer
            submeasure += 1
            fillNoteEndings(outputfile, noteoffs, getClockTime(measure_ct, submeasure))
        elif len(next_note) > 3:
            # note format is: i@frq!v_dr
            # i: instrument ('p', 'b', 'd')
            # frq: pitch 000..999,
            # v: velocity 0..7,
            # dr: duration in measure subdivisions 00..99
            instrument = next_note[0]
            pitch = int(next_note[2:5])
            velocity = int(next_note[6])*14+1 # pad with 1 to avoid accidental 0-velocity note_off messages
            duration = int(next_note[8:10])
            if instrument == 'p': # if it is a piano note
                # print('{0}-> measure {1:d} note pitch {2} dur {3}'.format(note, measure_ct, int(pitch), int(duration)))
                print(getCSVNoteOn(measure_ct, submeasure, pitch, instrument, velocity))
                outputfile.write(getCSVNoteOn(measure_ct, submeasure, pitch, instrument, velocity))
                heapq.heappush(noteoffs, (getOffClockTime(measure_ct, submeasure, duration), getCSVNoteOff(measure_ct, submeasure, pitch, instrument, duration)))
                last_time = int(DEFAULT_PPQ*(measure_ct*4+(submeasure+duration)/quarter_sub))

    measure_ct += 1

outputfile.write('2, {0:d}, End_track\n'.format(last_time))
outputfile.write('0, 0, End_of_file')

inputfile.close()
outputfile.close()

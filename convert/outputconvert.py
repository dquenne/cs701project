# outputconvert.py
# converts RNN-produced file to CSV (comma-separated value) to be used with MIDICSV
#
# TODO:
#   - use heap to keep track of note-off messages and insert in proper spot
#   -

import musicdata
import sys
import heapq


QUARTER_SUBDIVISION = 12

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


def max(a, b):
    if a > b:
        return a
    else:
        return b

def getClockTime(measure, beat):
    return int(DEFAULT_PPQ*(measure*4+beat/QUARTER_SUBDIVISION))

def getOffClockTime(measure, beat, duration):
    return int(DEFAULT_PPQ*(measure*4+(beat+duration)/QUARTER_SUBDIVISION))

def getCSVNoteOn(measure, beat, pitch, instrument, velocity, duration):
    return '{track}, {time:d}, Note_on_c, {channel}, {pitch:d}, {velocity}\n'.format(
        track=DEFAULT_TRACKS[instrument],
        time=int(DEFAULT_PPQ*(measure*4+beat/QUARTER_SUBDIVISION)),
        channel=DEFAULT_CHANNELS[instrument],
        pitch=pitch,
        velocity=velocity
    )

def getCSVNoteOff(measure, beat, pitch, instrument, duration):
    return '{track}, {time:d}, Note_on_c, {channel}, {pitch:d}, 0\n'.format(
        track=DEFAULT_TRACKS[instrument],
        time=int(DEFAULT_PPQ*(measure*4+(beat+duration)/QUARTER_SUBDIVISION)),
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

outnotes = {'p':[], 'b':[], 'd':[]}
noteoffs = []

header = inputfile.readline()

measure_ct = 0


last_time = 0
outputfile.write(FILE_HEADER.format(ppq=DEFAULT_PPQ, tempo=413793))
outputfile.write(TRACK_HEADER.format(track=2, channel=0, track_info="",copyright="",title="piano"))
while (1==1):
    beat = 0
    nextline = inputfile.readline()
    if (nextline == ''): # End of File
        break
    readnotes = nextline.split(" ")
    for note in readnotes:
        if note[0] == '.': # measure subdivision spacer
            beat += 1
            fillNoteEndings(outputfile, noteoffs, getClockTime(measure_ct, beat))
        elif len(note) > 3:
            # form i@frq!v_dr (i: instrument (p, b, d), frq: pitch 0..999,
            # v: velocity 0..7, dr: duration in measure subdivisions)
            instrument = note[0]
            pitch = int(note[2:5])
            velocity = int(note[6])*14
            duration = int(note[8:10])
            if instrument == 'p':
                # print('{0}-> measure {1:d} note pitch {2} dur {3}'.format(note, measure_ct, int(pitch), int(duration)))
                # outnotes[instrument].append(musicdata.Note(instrument, int(pitch), int(duration), int(measure_ct), int(beat), DEFAULT_PPQ))
                print(getCSVNoteOn(measure_ct, beat, pitch, instrument, velocity, duration))
                outputfile.write(getCSVNoteOn(measure_ct, beat, pitch, instrument, velocity, duration))
                heapq.heappush(noteoffs, (getOffClockTime(measure_ct, beat, duration), getCSVNoteOff(measure_ct, beat, pitch, instrument, duration)))
                last_time = int(DEFAULT_PPQ*(measure_ct*4+(beat+duration)/QUARTER_SUBDIVISION))

    measure_ct += 1

outputfile.write('2, {0:d}, End_track\n'.format(last_time))
outputfile.write('0, 0, End_of_file')

inputfile.close()
outputfile.close()

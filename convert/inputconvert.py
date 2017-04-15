# inputconvert.py
# converts CSV (comma-separated value) file to new format for training RNN
#
# TODO:
#   - need to dynamically assign channels to instruments



import musicdata
import sys

QUARTER_SUBDIVISION = 12


output = {}
max_measure = 0

# def max(a, b):
#     if a > b:
#         return a
#     else:
#         return b

# add Note object to output sublist (indexed by measure)
def addNote(new_note):
    if new_note.measure() in output:
        output[new_note.measure()].append(new_note) # actually, we should insert in order
    else:
        output[new_note.measure()] = [new_note]
        global max_measure
        max_measure = max(new_note.measure(), max_measure)


if len(sys.argv) > 1:
	inputcsv = open(sys.argv[1], 'r')
else:
    inputcsv = open('testcsv.csv', 'r')


unfinishedpitches = {'p':set(), 'b':set(), 'd':set()}
unfinishednotes = {'p':{}, 'b':{}, 'd':{}}
channeltoinstrument = {0:'p',10:'d'}

while (1==1):
    nextline = inputcsv.readline()
    if (nextline == ''): # End of File
        break


    if (nextline.find('Note_on_c') >= 0 and int(nextline.split(", ")[3]) in channeltoinstrument): # either note on or note off
        instr = channeltoinstrument[int(nextline.split(", ")[3])]
        if (int(nextline.split(", ")[5]) > 0): # velocity > 0, i.e. note ON
            pitch = nextline.split(", ")[4]
            unfinishedpitches[instr].add(pitch)
            unfinishednotes[instr][pitch] = musicdata.Note(nextline, ppq)
            unfinishednotes[instr][pitch].instrument = instr
            print('.')
        else:
            pitch = nextline.split(", ")[4]
            if pitch in unfinishedpitches[instr]:
                unfinishedpitches[instr].remove(pitch)
                unfinishednotes[instr][pitch].setEndTime(nextline.split(", ")[1])
                addNote(unfinishednotes[instr][pitch])
                unfinishednotes[instr][pitch] = None

    elif (nextline.find('Program_c') >= 0): # set channel's instrument value
        midi_instrument = int(nextline.split(", ")[4])
        if midi_instrument <= 15:
            channeltoinstrument[int(nextline.split(", ")[3])] = 'p'


    elif (nextline.find('Header') >= 0):
        linedata = nextline.split(", ")
        ppq = int(linedata[5])

    elif (nextline.find('Time_signature,') >= 0):
        timesig = nextline.split(", ")
        num = timesig[3]
        denom = timesig[4]
        clocksperbeat = timesig[5]
    # elif (nextline.find('Key_signature,') >= 0):

inputcsv.close()

print("writing output now")


if len(sys.argv) > 2:
	outputdata = open(sys.argv[2], 'w')
else:
    outputdata = open('output.txt', 'w')

notecount = 0
outputdata.write('newsong timesig{0}.{1}.{2}\n'.format(timesig[3], timesig[4], timesig[5]))
for measure in range(max_measure+1):
    # print(measure)
    if measure in output:
        for spot in range(4*QUARTER_SUBDIVISION):
            for note in output[measure]:
                if note.timeInMeasure() == spot:
                    notecount += 1
                    outputdata.write(note.getTrainingDataNote()+" ")
            outputdata.write(". ")
    else:
        outputdata.write(". . . . . . . . . . . . . . . . . . . . . . . . ")
    outputdata.write("\n")

outputdata.close()

print("wrote", notecount, "notes")
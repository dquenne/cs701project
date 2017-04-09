import musicdata

print("converting from MIDI/CSV to new format:")
print("input: 5, 3040, Note_on_c, 0, 57, 100")
note1 = musicdata.Note("5, 3040, Note_on_c, 0, 57, 100")
note1.instrument = "p"
print(note1.time, "pitch", note1.pitch, "at measure", note1.measure(4, 2, 24))
print(note1.getTrainingDataNote(4, 2, 24))
